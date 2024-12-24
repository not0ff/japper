from io import BytesIO

from PIL import Image
from werkzeug.datastructures import FileStorage


def optimize_img(image: FileStorage, resize: bool = False) -> FileStorage:
    img: Image.Image = Image.open(image)

    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    if resize:
        img = img.resize((512, 512))

    output: BytesIO = BytesIO()
    img.save(output, format='WEBP', optimize=True, quality=60)
    output.seek(0)

    return FileStorage(
        stream=output,
        filename='filename.webp',
        content_type="image/webp"
    )
