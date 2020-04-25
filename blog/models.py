from django.db import models
from datetime import datetime

from django.utils.safestring import mark_safe
from markdown import markdown

import houdini as h
import misaka as m
from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name

class HighlighterRenderer(m.HtmlRenderer):
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None

        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)
        # default
        return '\n<pre><code>{}</code></pre>\n'.format(
                            h.escape_html(text.strip()))

class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    quote = models.CharField(max_length=500)
    author = models.CharField(max_length=50)
    img = models.ImageField(upload_to="gallery", default = '')
    published = models.DateTimeField('date published', default=datetime.now)
    content = models.TextField()

    def __str__(self):
        return self.title

    def toMarkDown(self):
        renderer = HighlighterRenderer()
        md = m.Markdown(renderer, extensions=('fenced-code','tables', 'footnotes', 
        'autolink', 'strikethrough', 'underline', 'highlight', 'quote', 'superscript'))
        return mark_safe(md(self.content))
