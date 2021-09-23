import itertools
import pathlib
from textwrap import dedent

import yaml
from truncatehtml import truncate


def _tag_in_item(item, tag_str=None):
    if tag_str is None:
        return True
    all_tags = sorted(itertools.chain(*item['tags'].values()))
    return tag_str in all_tags


def _generate_sorted_tag_keys(all_items):

    key_set = set(itertools.chain(*[item['tags'].keys() for item in all_items]))
    return sorted(key_set)


def _generate_tag_set(all_items, tag_key=None):

    tag_set = set()
    for item in all_items:
        for k, e in item['tags'].items():
            if tag_key and k != tag_key:
                continue
            for t in e:
                tag_set.add(t)

    return tag_set


def _generate_tag_menu(all_items, tag_key):

    tag_set = _generate_tag_set(all_items, tag_key)
    tag_list = sorted(tag_set)

    options = ''.join(
        f'<li><a class="dropdown-item" href="/gallery/{tag.replace(" ", "-")}.html">{tag.title()}</a></li>\n'
        for tag in tag_list
    )

    return f"""
<div class="dropdown">
<button class="btn btn-sm btn-outline-primary mx-1 dropdown-toggle" type="button" id="{tag_key}Dropdown" data-bs-toggle="dropdown" aria-expanded="false">
{tag_key.title()}
</button>
<ul class="dropdown-menu" aria-labelledby="{tag_key}Dropdown">
{options}
</ul>
</div>
"""


def _generate_menu(all_items, flt=None):

    key_list = _generate_sorted_tag_keys(all_items)

    menu_html = '<div class="d-sm-flex mt-3 mb-4">\n'
    menu_html += '<div class="d-flex gallery-menu">\n'
    menu_html += '<div><a role="button" class="btn btn-primary btn-sm mx-1" href="https://github.com/ProjectPythia/projectpythia.github.io/issues/new?assignees=&labels=external-links-gallery-submission&template=update-external-links-gallery.md&title=">Submit a new resource</a></div>\n'
    if flt:
        menu_html += '<div><a role="button" class="btn btn-link btn-sm text-decoration-none" href="/gallery.html">Return to Full Gallery</a></div>\n'
    menu_html += '</div>\n'
    menu_html += '<div class="ms-auto d-flex">\n'
    for tag_key in key_list:
        menu_html += _generate_tag_menu(all_items, tag_key) + '\n'
    menu_html += '</div>\n'
    menu_html += '</div>\n'
    menu_html += '<script>$(document).on("click",function(){$(".collapse").collapse("hide");}); </script>\n'
    return menu_html


def build_from_items(items, filename, title='Gallery', subtitle=None, menu_html='', max_descr_len=300):

    # Build the gallery file
    panels_body = []
    for item in items:
        if not item.get('thumbnail'):
            item['thumbnail'] = '/_static/images/ebp-logo.png'
        thumbnail = item['thumbnail']
        tag_list = sorted((itertools.chain(*item['tags'].values())))
        tags = [
            f'<a href="/gallery/{tag.replace(" ", "-")}.html" class="badge bg-primary link-light">{tag}</a>'
            for tag in tag_list
        ]
        tags = '\n'.join(tags)

        author_strs = set()
        affiliation_strs = set()
        for a in item['authors']:
            author_name = a.get('name', 'Anonymous')
            author_email = a.get('email', None)
            if author_email:
                _str = f'<a href="mailto:{author_email}">{author_name}</a>'
            else:
                _str = author_name
            author_strs.add(_str)

            affiliation_name = a.get('affiliation', None)
            if affiliation_name:
                affiliation_url = a.get('affiliation_url', None)
                if affiliation_url:
                    _str = f'<a href="{affiliation_url}">{affiliation_name}</a>'
                else:
                    _str = affiliation_name
                affiliation_strs.add(_str)

        authors_str = f"<strong>Author:</strong> {', '.join(author_strs)}"
        if affiliation_strs:
            affiliations_str = f"<strong>Affiliation:</strong> {' '.join(affiliation_strs)}"
        else:
            affiliations_str = ''

        if len(item['description']) < max_descr_len:
            short_description = item['description']
            modal_str = ''
        else:
            short_description = truncate(
                item['description'], max_descr_len, ellipsis='<a class="modal-btn"> ...more</a>'
            )
            modal_str = f"""
<div class="modal">
<div class="content">
<img src="{thumbnail}" class="modal-img" />
<h3 class="display-3">{item["title"]}</h3>
{authors_str}
<br/>
{affiliations_str}
<p class="my-2">{item['description']}</p>
<p class="my-2">{tags}</p>
<p class="mt-3 mb-0"><a href="{item["url"]}" class="btn btn-outline-primary btn-block">Visit Website</a></p>
</div>
</div>
"""

        panels_body.append(
            f"""\
---

<div class="d-flex gallery-card">
<img src="{thumbnail}" class="gallery-thumbnail" />
<div class="container">
<a href="{item["url"]}" class="text-decoration-none"><h4 class="display-4 p-0">{item["title"]}</h4></a>
<p class="card-subtitle">{authors_str}<br/>{affiliations_str}</p>
<p class="my-2">{short_description}</p>
</div>
</div>
{modal_str}

+++

{tags}

"""
        )

    panels_body = '\n'.join(panels_body)

    if subtitle:
        stitle = f'<span class="display-3">Displaying "{subtitle}" tags</span>'
    else:
        stitle = ''

    panels = f"""
# {title}

{stitle}

{menu_html}

````{{panels}}
:column: col-12
:card: +mb-4 w-100
:header: d-none
:body: p-3 m-0
:footer: p-1

{dedent(panels_body)}
````

<div class="modal-backdrop"></div>
<script src="/_static/custom.js"></script>
"""

    pathlib.Path(f'{filename}.md').write_text(panels)


def main(app):

    with open('gallery.yaml') as fid:
        all_items = yaml.safe_load(fid)

    title = 'Pythia Resource Gallery'
    menu_html = _generate_menu(all_items)
    build_from_items(all_items, 'gallery', title=title, menu_html=menu_html)

    menu_html_flt = _generate_menu(all_items, flt=True)
    tag_set = _generate_tag_set(all_items)

    for tag in tag_set:
        items = [item for item in all_items if _tag_in_item(item, tag)]
        build_from_items(items, f'gallery/{tag.replace(" ", "-")}', title=title, subtitle=tag, menu_html=menu_html_flt)


def setup(app):
    app.connect('builder-inited', main)
