# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter
import markdown as md
from mdx_emoticons import EmoticonsExtension


register = template.Library()


# extra = [
#   'abbr',
#           #[abbr]: Long text
#   'attr_list',
#           {: #id .class key='value' }
#       =>  <tag id="id" class="class" key="value"></tag>
#   'def_list'
#           Term
#           :   defintion
#       =>  <dl><dt>Term</dt><dd>definition</dt></dl>
#   'fenced_code',
#           ```{ .lang .classes }
#           codeblock
#           ```
#       =>  code block wit syntax highlighting
#   'footnotes'
#           [^1]: This is a footnote
#           [^@#$%]: A footnote on the label: "@#$%".
#   'md_in_html'
#           allows markdown in html <div markdown="1"><p>This is a *markdown* paragraph</p></div>
#   'tables',
#           First Header  | Second Header
#           ------------- | -------------
#           Content Cell  | Content Cell
#           Content Cell  | Content Cell
# ]
#
markdown_extensions = [
    'markdown.extensions.extra',        # see above
    'markdown.extensions.codehilite',   # syntax highlighting using pygments
    'markdown.extensions.toc',          # table of contents [TOC]
    EmoticonsExtension(base_url='/media/emoticons/', file_extension='gif')

]

markdown_extension_configs = {
}


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value,
                       extensions=markdown_extensions,
                       extension_configs=markdown_extension_configs)
