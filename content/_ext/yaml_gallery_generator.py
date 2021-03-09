import yaml
from textwrap import dedent
import pathlib

def build_from_yaml(filename, display_name):

    with open(f'{filename}.yaml') as fid:
        items = yaml.safe_load(fid)

    # Build the gallery file
    panels_body = []
    for item in items:
        if not item.get('thumbnail'):
            item['thumbnail'] = '../_static/images/ebp-logo.png'
        tags = [f'{{badge}}`{tag},badge-primary badge-pill`' for tag in item['tags']]
        tags = '\n'.join(tags)

        authors = [a.get("name", "anonymous") for a in item['authors']]

        if len(authors) == 1:
            authors_str = f'Created by: {authors[0]}'
        elif len(authors) == 2:
            authors_str = f'Created by: {authors[0]} and {authors[1]}'

        email = [a.get("email", None) for a in item['authors']][0]
        email_str = '' if email == None else f'Email: {email}'

        affiliation = [a.get("affiliation", None) for a in item['authors']][0]
        affiliation_str = '' if affiliation == None else f'Affiliation: {affiliation}'

        affiliation_url = [a.get("affiliation_url", None) for a in item['authors']][0]
        affiliation_url_str = '' if affiliation_url == None else f'{affiliation} Site: {affiliation_url}'

        panels_body.append(
            f"""\
---
:img-top: {item["thumbnail"]}
+++
**{item["title"]}**

{authors_str}

{email_str}

{affiliation_str}

{affiliation_url_str}
 
```{{dropdown}} {item['description'][0:100]} ... <br> **See Full Description:**
{item['description']}
```

```{{link-button}} {item["url"]}
:type: url
:text: Visit Website
:classes: btn-outline-primary btn-block
```

categories: {tags}
"""
        )
    panels_body = '\n'.join(panels_body)

    panels = f"""
# {display_name} Gallery
````{{panels}}
:container: full-width
:column: text-left col-6 col-lg-4
:card: +my-2
:img-top-cls: w-75 m-auto p-2
:body: d-none
{dedent(panels_body)}
````
"""

    pathlib.Path(f'pages/{filename}.md').write_text(panels)


def main(app):
    for yaml_file, display_name in [('links', 'External Links')]:
        build_from_yaml(yaml_file, display_name)


def setup(app):
    app.connect('builder-inited', main)