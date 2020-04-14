# WHAPI

The MediaWiki API is complicated and arcane, and can require esoteric knowledge of the MediaWiki software to use it effectively. Worse still, it's mostly obscured on WikiHow, and it's likely they'd rather you didn't know it was there altogether. WikiHow API (WHAPI) aims to simplify this to some degree, providing a Python-based interface to perform some useful functions, such as retrieving article intros, steps, and info. One can use the resulting data to build an app on top of WikiHow, or just to find random useful (or useless, more likely) information on how to do things.

Obviously for a lot of these functions you could just go to the website, but what if you need to do weird stuff with the data and don't want to write your own webscraper?

- [Installation](#install)
- [Usage](#usage)
  * [Article ID](#article-id)
  * [Random HowTo](#random-howto)
  * [Article Details](#article-details)
  * [Images](#images)
  * [Search](#search)
  * [Parsing](#parsing)
    - [HTML](#html)
    - [Intro](#intro)
    - [Steps](#steps)
- [ToDo](#todo)


## Installation
```bash
pip install whapi
```

## Usage

### Article ID

Everything useful relies on a numeric article ID. You don't have to see this, but be aware that it's important. If you only have a URL, you can use get_id() to convert it to an article ID that can be passed to other functions.

```python
from whapi import get_id

article_id = get_id('https://www.wikihow.com/Chug-Water')
```

### Random HowTo

Learn random stuff! Retuns a random WikiHow article. Sometimes they're weird. Sometimes they're really weird. random_article() returns a randomized article ID that can then be passed to other functions.

```python
from whapi import random_article

random_howto = random_article()
```

### Article Details

Uses the article ID to return a URL and title for an article. In addition, it returns whether an article is considered a stub or "low quality".

```python
from whapi import return_details

article_info = return_details(635542)
```

### Images

Retrieves a list of all images included in an article as URLs.

```python
from whapi import get_images

image_list = get_images(1097122)
```

### Search

Searches WikiHow for the a string and returns a list containing dict objects that contain article IDs, titles, and URLs. The default max results is 10, but this can be changed. MediaWiki's limit for this is 500. As for WikiHow, I don't know. You shouldn't need 500 search results anyway.

```python
from whapi import search

search_results = search('goth', 5)
```

### Parsing

#### HTML

All the parsing functions rely on get_html() to obtain some data to parse and package for you. It uses the article ID to retrieve information.

```python
from whapi import get_html

html = get_html(1632)
```

#### Intro

Every WikiHow article has an introductory paragraph or two. If you want this, use the parse_intro() function.

```python
from whapi import get_html, parse_intro

html = get_html(1946507)
intro_text = parse_intro(html)
```

#### Steps

Every WikiHow article also has a list of steps, and they're chock full of really great stuff. Use parse_steps() to get a dict object that contains dict objects containing the step number, summary, and details.

```python
from whapi import get_html, parse_steps

html = get_html(680027)
steps = parse_steps(html)
```

## ToDo

- Many WikiHow articles also contain "Methods" which break down further into sub-steps. Write a function to parse these additional divisions.
- Add parser for tips
- Add parser for warnings
- I have code to rotate proxies and user agent strings, but since this no longer scrapes pages, this probably isn't necessary
- Unordered lists in steps break the parse_steps() function. For now they're ignored, but it would be nice to have them parsed and inserted into the correct step
