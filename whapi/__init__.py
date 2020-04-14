import requests
import json
import bs4
from whapi.exceptions import ParseError

# Everything relies on the mediawiki API and the numeric article ID
# There are fancier ways to implement the various API parameters but they seem like more work than is necessary
api = 'https://www.wikihow.com/api.php?format=json&action='

# returns ID for an article if the URL is provided
def get_id(url):
    url = url.replace('https://www.wikihow.com/', '')
    r = requests.get(api + 'query&prop=info&titles=' + url)
    data = r.json()
    pages = data['query']['pages']
    for key in pages.keys():
        article_id = pages[key]['pageid']
    return article_id

# retrieves a random article ID or IDs and stores them in a list, unless there's only one
def random_article(limit=1):
    r = requests.get(api + 'query&list=random&rnnamespace=0&rnlimit=' + str(limit))
    data = r.json()
    data = data['query']['random']
    article_ids = [li['id'] for li in data]
    if len(article_ids) == 1:
        article_ids = article_ids[0]
    return article_ids

# returns URL & title for a given article ID in case you need that
def return_details(id):
    article_details = {}
    r = requests.get(api + 'query&prop=info|templates|categories&inprop=url&pageids=' + str(id))
    data = r.json()
    article_details['url'] = data['query']['pages'][str(id)]['fullurl']
    article_details['title'] = data['query']['pages'][str(id)]['title']
    if 'templates' not in data['query']['pages'][str(id)]:
        article_details['is_stub'] = False
    else:
        templates = data['query']['pages'][str(id)]['templates']
        if not any(d['title'] == 'Template:Stub' for d in templates):
            article_details['is_stub'] = False
        else:
            article_details['is_stub'] = True
    if 'categories' not in data['query']['pages'][str(id)]:
        article_details['low_quality'] = True
    else:
        categories = data['query']['pages'][str(id)]['categories']
        if not any (d['title'] == 'Category:Articles in Quality Review' for d in categories):
            article_details['low_quality'] = False
        else:
            article_details['low_quality'] = True
    return article_details

# doesn't really get used in my projects, but it should be included nonetheless
# returns a list of dict items containing article titles, IDs, and URLs
def search(search_term, max_results=10):
    search_results = []
    r = requests.get(api + 'query&format=json&utf8=&list=search&srsearch=' + search_term + "&srlimit=" + str(max_results))
    data = r.json()
    if not data:
        raise ParseError
    else:
        data = data['query']['search']
        for result in data:
            listing = {}
            details = return_details(result['pageid'])
            listing['title'] = result['title']
            listing['article_id'] = result['pageid']
            listing['url'] = details['url']
            search_results.append(listing)
    return search_results

# returns a list of URLs for the images in an article
def get_images(id):
    images = []
    r = requests.get(api + 'parse&prop=images&pageid=' + str(id))
    data = r.json()
    image_list = data['parse']['images']
    if not image_list:
        raise ParseError
    else:
        for i in image_list:
            im_data = requests.get(api + 'query&titles=File:' + i + '&prop=imageinfo&iiprop=url')
            image_info = im_data.json()
            pages = image_info['query']['pages']
            for key in pages.keys():
                 image_url = pages[key]['imageinfo'][0]['url']
            images.append(image_url)
    return images

# returns article html for parsing. Uses the mobile version because that returns more useful CSS classes
def get_html(id):
    r = requests.get(api + 'parse&prop=text&mobileformat&pageid=' + str(id))
    data = r.json()
    html = data['parse']['text']['*']
    return html

# get article intro/summary
def parse_intro(id):
    html = get_html(id)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    intro_html = soup.find("div", {"class": "mf-section-0"})
    if not intro_html:
        raise ParseError
    else:
        super = intro_html.find("sup")
        if super != None:
            for sup in intro_html.findAll("sup"):
                sup.decompose()
                intro = intro_html.text
                intro = intro.strip()
        else:
            intro = intro_html.text
            intro = intro.strip()
    return intro

# cleans junk tags from html and returns a dict of steps
def parse_steps(id):
    html = get_html(id)
    steps = {}
    count = 1
    soup = bs4.BeautifulSoup(html, 'html.parser')
    step_html = soup.find("div", {"class": "mf-section-1"})
    if not step_html:
        raise ParseError
    else:
        super = step_html.find("sup")
        mwimage = step_html.find("div", {"class": "mwimg"})
        ul = step_html.find("ul")
        if super != None:
            for sup in step_html.findAll("sup"):
                sup.decompose()
        if mwimage != None:
            for div in step_html.findAll("div", {"class": "mwimg"}):
                div.decompose()
        # If there's an unordered list in our step it breaks the parser and creates too many steps
        # For now we'll just dispose of them
        if ul != None:
            for ul in step_html.findAll("ul"):
                ul.decompose()
        step_list = step_html.find("ol")
        if not step_list:
            raise ParseError
        else:
            for li in step_list.findAll("li"):
                step_info = {}
                li = li.text
                step = li.split('.', 1)
                summary = step[0]
                summary = summary.strip()
                description = step[1]
                description = description.strip()
                step_info['summary'] = summary
                step_info['description'] = description
                steps.update({'step_' + str(count): step_info})
                count += 1
    return steps

if __name__ == "__main__":
    print('Hey get outta here')
