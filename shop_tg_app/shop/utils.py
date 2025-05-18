import io
from django.core.files.base import ContentFile
from PIL import Image
from django.db.models.fields.files import FieldFile
from django.conf import settings

def convert_image_to_webp(image_field: FieldFile) -> ContentFile:
    """
    Конвертирует изображение в формат webp и возвращает его как Django ContentFile.
    Принимает только JPG.
    """
    try:
        image_field.open()
        image_field.seek(0)

        img = Image.open(image_field)
        if (img.format or '').upper() not in ['JPEG', 'JPG']:
            raise ValueError('Разрешены только JPG изображения.')

        img = img.convert('RGB')

        buffer = io.BytesIO()
        quality = getattr(settings, 'WEBP_QUALITY', 80)
        img.save(buffer, format='WEBP', quality=quality)

        image_name = image_field.name.rsplit('.', 1)[0] + '.webp'
        return ContentFile(buffer.getvalue(), name=image_name)

    except Exception as e:
        raise ValueError(f"Ошибка при конвертации изображения: {e}")
