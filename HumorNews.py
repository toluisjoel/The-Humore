import yagmail
import requests
from bs4 import BeautifulSoup

all_posts = [[], []]


def get_content(web_page, tag, tag_class):
    web_page = requests.get(web_page)
    soup = BeautifulSoup(web_page.text, 'lxml')
    source = soup.find_all(tag, class_=tag_class)

    def parse(post_source):
        for post in post_source:
            post_title = post.text
            if "https" not in (post_link := post.a['href']):
                post_link = 'https://www.ladbible.com' + post_link
            all_posts[0].append(post_title)
            all_posts[1].append(post_link)

    parse(source)


all_posts = set(zip(all_posts[0], all_posts[1]))  # randomize posts
html = ''

for index, (title, link) in enumerate(all_posts):
    html_title = f'<h2><a href="{link}">{(index + 1)}. {title}</a></h2>'
    html += html_title

with open('template.html', 'r') as template:
    data = template.readlines()
    data[62] = html + '\n'  # passing the html posts to the template

with open('template.html', 'w') as template:
    template.writelines(data)

with open('template.html', 'r') as template:
    email = yagmail.SMTP('your@gmail.com', input('Email Password: '))
    email.send('receiver@gmail.com', 'The Humor News', template)

get_content('https://www.today.com/news/good-news', 'h2', 'tease-card__headline tease-card__title tease-card__title--today relative')
get_content('https://www.goodnewsnetwork.org/category/news/inspiring/', 'h3', 'entry-title td-module-title')
get_content('https://www.ladbible.com/weird', 'div', 'css-32xpko-cardText-padding-padding-padding-padding-padding-padding-padding')
get_content('https://www.theweek.co.uk/odd-news-0', 'div', 'polaris__article-card -layout-default -default polaris__article-group--single')
