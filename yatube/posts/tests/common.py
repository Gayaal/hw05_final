from io import BytesIO

from PIL import Image


def create_image():
    file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file, 'gif')
    file.name = 'test.gif'
    file.seek(0)
    return file