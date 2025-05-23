import os
from django.core.files.uploadedfile import TemporaryUploadedFile
import qrcode
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styledpil import StyledPilImage
from PIL import Image, ImageOps, ImageDraw
from django.http import HttpResponse
from core import settings
from rest_framework import views, response

from rest_framework import status
from .models import Restaurant
from urllib.parse import quote
import asyncio
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
import zipfile



class GenerateQR(views.APIView):

    def process_image(self, input_path):
        im = Image.open(input_path)
        size = (200, 200)

        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        im = im.resize(size, Image.BICUBIC)

        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.thumbnail(size)
        outpu_path = f"{input_path}_output.png"
        output.save(outpu_path)
        return outpu_path


    def post(self, request):
        user = request.user
        queryset: str = Restaurant.objects.filter(user=user).first()
        output_folder = os.path.join(settings.MEDIA_ROOT, f"{str(queryset).lower()}/qrcodes")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        qr = qrcode.QRCode(
                version=7,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=50,
                border=8,
            )

        data = f"https://aurora-app.uz/vendor/{quote(str(queryset))}"
        qr.add_data(data)
        qr.make(fit=True)
        image = qr.make_image(
            fill_color="black",
            back_color="white",
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),

        )
        output_path = os.path.join(output_folder, f"qr_{str(queryset).lower()}.png")
        image.save(output_path)
        if os.path.exists(output_path):
            with open(output_path, 'rb') as file:
                result = HttpResponse(file.read(), content_type="image/png")
                result["Content-Disposition"] = f"attachment; filename=qr_{str(queryset).lower()}.png"
                return result
        else:
            return response.Response({"message": "Такой файл не сушествует", "code": "4"})
        return response.Response({"detail": "QR Code успешно сгенерирован"}, status=status.HTTP_201_CREATED)
    
class DownloadQR(views.APIView):
    def get(self, request):
        user = request.user
        queryset = Restaurant.objects.filter(user=user).first()
        qr_image_path = os.path.join(settings.MEDIA_ROOT, f"{queryset}/qrcodes", f"qr_{str(queryset).lower()}.png")
        
        if os.path.exists(qr_image_path):
            with open(qr_image_path, 'rb') as file:
                result = HttpResponse(file.read(), content_type="image/png")
                result["Content-Disposition"] = f"attachment; filename=qr_{str(queryset).lower()}.png"
                return result
        else:
            return response.Response({"message": "Такой файл не сушествует", "code": "4"})



def image_resize(image):
    res_width = 1920 
    img = Image.open(image)
    image_format = "png" if img.mode == "RGBA" else "jpeg"
    wpercent = (res_width / float(img.size[0])) 
    hsize = int((float(img.size[1]) * float(wpercent))) 
    img = img.resize((res_width, hsize), Image.Resampling.LANCZOS)
    temp_file = TemporaryUploadedFile(name=f"resized_image.{image_format}", size=1, content_type=f'image/{image_format}', charset=None)
    img.save(temp_file, format=f'{image_format}')
    return temp_file

async def image_resize_asyc(image):
    res_width = 1920
    loop = asyncio.get_event_loop() 
    img = await loop.run_in_executor(None, Image.open, image)
    image_format = "png" if img.mode == "RGBA" else "jpeg"
    wpercent = (res_width / float(img.size[0])) 
    hsize = int((float(img.size[1]) * float(wpercent))) 
    img = img.resize((res_width, hsize), Image.Resampling.LANCZOS)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format=f'{image_format}')
    temp_file = InMemoryUploadedFile(img_buffer, None, f"resized_image.{image_format}", f'image/{image_format}', img_buffer.getbuffer().nbytes, None)
    return temp_file


def crop_image_by_percentage(
    image_path, x, y, width, height, scaleX=1, scaleY=1, rotate=0
):
    if image_path == None:
        return
    res_width = 1920
    with Image.open(image_path) as image:

        if scaleX != 1 or scaleY != 1:
            image = image.resize(
                (int(image.width * scaleX), int(image.height * scaleY)), Image.ANTIALIAS
            )
        if rotate:
            image = image.rotate(-rotate, expand=True)
        cropped_image = image.crop((x, y, x + width, y + height))        
        wpercent = res_width / float(cropped_image.size[0])
        hsize = int((float(cropped_image.size[1]) * float(wpercent)))
        cropped_image = cropped_image.resize((res_width, hsize), Image.Resampling.LANCZOS)
        
        image_format = "png" if image.mode == "RGBA" else "jpeg"

        img_byte_arr = io.BytesIO()
        cropped_image.save(img_byte_arr, format=f"{image_format}")
        img_byte_arr.seek(0)
        img_tmp = TemporaryUploadedFile(
            name=f'cropped_image.{image_format}',
            size=img_byte_arr.getbuffer().nbytes,
            content_type=f'image/{image_format}',
            charset=None,
        )
        img_tmp.write(img_byte_arr.read())
        img_tmp.seek(0)
        
        return img_tmp  



"""
class DownloadQR(APIView):
    def get(self, request):
        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=qrcodes.zip"

        user = request.user
        queryset = Restaurant.objects.filter(user=user)
        restaurant_names = queryset.values_list("name", flat=True)
        name_rest = ", ".join(restaurant_names)
        qr_image_path = os.path.join(
            settings.MEDIA_ROOT, f"{name_rest}/qrcodes")

        if os.path.exists(qr_image_path):

            with zipfile.ZipFile(response, "w") as zf:
                for filename in os.listdir(os.path.join(settings.MEDIA_ROOT, qr_image_path)):
                    zf.write(os.path.join(qr_image_path, filename), filename)
            return response
        else:
            return HttpResponse(status=404)

            
print("######################")
print("######################")
print()
print("######################")
print("######################")

"""