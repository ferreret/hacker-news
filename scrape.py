from os import link
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs

res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = bs(res.text, 'html.parser')
soup2 = bs(res2.text, 'html.parser')

links = soup.select('.titlelink')
subtexts = soup.select('.subtext')
links2 = soup2.select('.titlelink')
subtexts2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtexts = subtexts + subtexts2


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtexts):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtexts[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(
                ' points', '').replace(' point', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})

    return sort_stories_by_votes(hn)


pprint(create_custom_hn(mega_links, mega_subtexts))
