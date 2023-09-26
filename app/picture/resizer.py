from PIL import Image


def resize_image(picture, height):
    original_image = Image.open(picture.image)
    needed_height = height
    width, height = original_image.size
    new_width = int((width / height) * needed_height)
    new_size = (new_width, needed_height)
    thumbnail = original_image.resize(new_size)
    return thumbnail
