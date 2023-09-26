import io
from PIL import Image


def generate_thumbnail(image_path, thumbnail_height):
    """generates a thumbnail"""
    try:
        image = Image.open(image_path)

        width, height = image.size
        proportions = width/height
        thumbnail_width = proportions * thumbnail_height

        thumbnail = image.resize((thumbnail_width, thumbnail_height),
                                 Image.ANTIALIAS)
        thumbnail_bytes = io.BytesIO()
        thumbnail.save(thumbnail_bytes, format='JPEG')
        thumbnail_bytes.seek(0)
        return thumbnail_bytes.getvalue()
    except Exception as e:
        print(f'Error: {str(e)}')
