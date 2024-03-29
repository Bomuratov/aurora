import os
import qrcode
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styledpil import StyledPilImage
from PIL import Image, ImageOps, ImageDraw
from django.http import HttpResponse
from core import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Restaurant
from urllib.parse import quote


class GenerateQR(APIView):

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
        queryset = Restaurant.objects.filter(user=user)
        restaurant_names = queryset.values_list("name", flat=True)
        restaurant_logo = queryset.values_list("logo", flat=True)

        name_rest = ", ".join(restaurant_names)
        logo = restaurant_logo.first()
        path1 = os.path.join(settings.MEDIA_ROOT, logo)

        if logo:
            logo_round = self.process_image(path1)

        output_folder = os.path.join(settings.MEDIA_ROOT, f"{name_rest}/qrcodes")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        qr = qrcode.QRCode(
            version=7,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=50,
            border=8,
        )

        data = f"https://www.aurora-app.uz/vendor/{quote(name_rest)}/"
        qr.add_data(data)
        qr.make(fit=True)
        image = qr.make_image(
            fill_color="black",
            back_color="white",
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            embeded_image_path=(
                os.path.join(settings.MEDIA_ROOT, f"{logo_round}")
                if logo_round
                else None
            ),
        )

        output_path = os.path.join(output_folder, f"menu_qr1.png")
        image.save(output_path)
        img_path = f"{name_rest}/qrcodes/menu_qr1.png"
        img_url = f"https://aurora-api.uz/media/{quote(img_path)}"
        return Response({"image_path": img_url}, status=status.HTTP_201_CREATED)

class DownloadQR(APIView):
    def get(self, request):
        user = request.user
        queryset = Restaurant.objects.filter(user=user)
        restaurant_names = queryset.values_list("name", flat=True)
        name_rest = ", ".join(restaurant_names)
        qr_image_path = os.path.join(
            settings.MEDIA_ROOT, f"{name_rest}/qrcodes", "menu_qr1.png"
        )

        if os.path.exists(qr_image_path):

            with open(qr_image_path, "rb") as file:
                response = HttpResponse(file.read(), content_type="image/png")
                response["Content-Disposition"] = "attachment; filename=menu_qr1.png"
                return response
        else:
            return HttpResponse(status=404)

        """ 
        print("######################")
        print("######################")
        print()
        print("######################")
        print("######################")
        """
