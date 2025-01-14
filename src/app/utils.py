from io import BytesIO
from typing import Optional, Union

from flask_login import current_user
from PIL import Image
from werkzeug.datastructures import FileStorage

from app.models import Post


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


def get_post(json_req: Optional[dict]) -> tuple[int, Union[Post, str]]:
    if json_req is None or 'post_id' not in json_req:
        return 400, 'Invalid request'

    try:
        post_id = int(json_req['post_id'])
    except (ValueError, TypeError):
        return 400, 'Invalid post ID'

    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return 404, 'Post not found'

    post.liked = True if current_user.id in [
        like.user_id for like in post.likes] else False

    return 200, post
