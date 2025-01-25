from io import BytesIO
from typing import Optional, Sequence, Union

import sqlalchemy as sa
from PIL import Image
from werkzeug.datastructures import FileStorage

from app.extensions import db
from app.models import Like, Post


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

    post: Post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return 404, 'Post not found'

    return 200, post


def get_feed() -> Sequence[Post]:
    query: sa.Select = sa.select(Post, ((
        sa.select(
            sa.func.count())
        .where(Like.post_id == Post.id)
        .scalar_subquery() - 1) / ((
            sa.func.strftime('%s', sa.func.now()) -
            sa.func.strftime('%s', Post.timestamp)
        ) + 1)
    ).label('rank')
    ).order_by(sa.literal_column('rank').desc())

    return db.session.execute(query).scalars().all()


def search_post(pattern: str) -> Sequence[Post]:
    pattern = '%'.join(pattern.split())
    return Post.query.filter(Post.content.like(f'%{pattern}%')).order_by(sa.desc(Post.timestamp)).all()