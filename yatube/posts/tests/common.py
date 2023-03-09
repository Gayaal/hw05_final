from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def create_image(name: str = 'giffy.gif') -> SimpleUploadedFile:
    file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file, 'gif')
    return SimpleUploadedFile(
        name=name,
        content=image,
        content_type='image/gif',
    )