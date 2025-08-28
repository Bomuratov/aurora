import io
from PIL import Image
from django.core.files.base import ContentFile


def generate_description(self):
    """
    Утилита для модельки DeliveryRules а именно автогенерация полей description и name
    """
    if not self.name:
        self.name = self.get_calculation_type_display()

    distance_part = ""
    if self.min_distance is not None and self.max_distance is not None:
        distance_part = f" \nЭто означает если растояние до адреса клиента от {round(self.min_distance)} км до {round(self.max_distance)} км."
    elif self.min_distance is not None:
        distance_part = f" \nЭто означает если растояние до адреса клиента от {round(self.min_distance)} км."
    elif self.max_distance is not None:
        distance_part = f" \nЭто означает если растояние до адреса клиента до {round(self.max_distance)} км."

    free_delivery_part = ""
    if self.max_order_price_for_free_delivery is not None:
        free_delivery_part = f"\nОбратите внимание, если сумма заказа выше или ровно {self.max_order_price_for_free_delivery} сум то доставка будет бесплатным."
    
    if self.max_order_price_for_free_delivery and self.reverse_calculate:
        free_delivery_part = f"\nОбратите внимание, если сумма заказа ниже или ровно {self.max_order_price_for_free_delivery} сум то доставка будет бесплатным."

    if self.calculation_type == "fixed" and self.fixed_price is not None:
        self.description = (
            f"Доставка стоит фиксированную сумму: {self.fixed_price} сум."
            f"{distance_part}."
            f"{free_delivery_part}"
        )
    elif self.calculation_type == "per_km" and self.price_per_km is not None:
        self.description = (
            f"Доставка рассчитывается по расстоянию: {round(self.price_per_km)} сум за каждый километр."
            f"{free_delivery_part}"
        )
    elif self.calculation_type == "percent" and self.price_per_percent is not None:
        self.description = (
            f"Доставка составит {round(self.price_per_percent)}% от суммы заказа."
            f"{free_delivery_part}"
        )
    else:
        self.description = "Правило доставки не определено."


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