from flask import abort

from models import Post
from routes.utils import is_admin


def get_post_for_view(post_id: int) -> Post:
    """Return a post if the current viewer may read it; otherwise 404."""
    post = Post.query.get(post_id)
    if post is None:
        abort(404)
    if not post.public and not is_admin():
        abort(404)
    return post
