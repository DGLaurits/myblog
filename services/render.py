import markdown

MARKDOWN_EXTENSIONS = ['fenced_code', 'tables', 'nl2br']


def render_markdown(text: str) -> str:
    """Convert Markdown source to HTML. Used for published posts and editor preview."""
    if not text:
        return ''
    return markdown.markdown(text, extensions=MARKDOWN_EXTENSIONS)
