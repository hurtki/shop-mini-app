from PIL import Image
from django.core.exceptions import ValidationError


# валидация расширения загружаемого изображения
def validate_jpg_image(image):
    try:
        img = Image.open(image)
        if img.format != 'JPEG':
            raise ValidationError('Файл должен быть в формате JPG.')
    except Exception:
        raise ValidationError('Недопустимое изображение.')

