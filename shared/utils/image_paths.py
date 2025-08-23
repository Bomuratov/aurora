import io
from PIL import Image
from django.core.files.base import ContentFile



def thumbnail(image, size=(600, 450)):
    """
    Уменьшает изображение до указанного размера с сохранением пропорций.

    :param image: Загруженный объект файла (models.ImageField).
    :param size: Размер (ширина, высота) thumbnail'а.
    :return: Уменьшенный файл для сохранения в модели.
    """
    img = Image.open(image)
    img.thumbnail(size, Image.Resampling.LANCZOS)  # Уменьшает изображение

    # Сохранение в памяти
    img_io = io.BytesIO()
    img.save(img_io, format=img.format)
    return ContentFile(img_io.getvalue(), name=image.name)


def upload_path_menu(instance, filename):
    file = filename.rfind(".")
    formatt = filename[file:]
    name = instance.name + formatt
    return "{0}/category/{1}/{2}".format(
        instance.restaurant.name, instance.category.name, name
    )


def upload_path_rest(instance, file):
    return "{0}/backgroud/{1}".format(instance.name, file)


def upload_logo_rest(instance, file):
    return "{0}/logo/{1}".format(instance.name, file)


def upload_path_promo(instance, filename):
    file = filename.rfind(".")
    formatt = filename[file:]
    name = instance.name + formatt
    return "{0}/promo/{1}/{2}".format(instance.restaurant.name, instance.name, name)