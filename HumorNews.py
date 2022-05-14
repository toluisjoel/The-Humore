import yagmail
import requests
from bs4 import BeautifulSoup

all_posts = [[], []]


def parse(post_source):
    for post in post_source:
        post_title = post.text
        if "https" not in (post_link := post.a['href']):
            post_link = 'https://www.ladbible.com' + post_link
        all_posts[0].append(post_title)
        all_posts[1].append(post_link)


web_page_1 = requests.get('https://www.today.com/news/good-news')
soup = BeautifulSoup(web_page_1.text, 'lxml')
posts_source_1 = soup.find_all('h2', class_='tease-card__headline tease-card__title tease-card__title--today relative')
parse(posts_source_1)

web_page_2 = requests.get('https://www.goodnewsnetwork.org/category/news/inspiring/')
soup = BeautifulSoup(web_page_2.text, 'lxml')
posts_source_2 = soup.find_all('h3', class_='entry-title td-module-title')
parse(posts_source_2)

web_page_3 = requests.get('https://www.ladbible.com/weird')
soup = BeautifulSoup(web_page_3.text, 'lxml')
posts_source_3 = soup.find_all('div', class_='css-32xpko-cardText-padding-padding-padding-padding-padding-padding-padding')
parse(posts_source_3)

web_page_4 = requests.get('https://www.theweek.co.uk/odd-news-0')
soup = BeautifulSoup(web_page_4.text, 'lxml')
posts_source_4 = soup.find_all('div', class_='polaris__article-card -layout-default -default polaris__article-group--single')
parse(posts_source_4)

all_posts = set(zip(all_posts[0], all_posts[1]))  # randomize posts
html = ''

for index, (title, link) in enumerate(all_posts):
    html_title = f'<h2><a href="{link}">{(index + 1)}. {title}</a></h2>'
    html += html_title

with open('template.html', 'r') as template:
    data = template.readlines()
    data[65] = html + '\n'  # passing the html posts to the template

with open('template.html', 'w') as template:
    template.writelines(data)

with open('template.html', 'r') as template:
    email = yagmail.SMTP('your@gmail.com', input('Email Password: '))
    email.send('receiver@gmail.com', 'The Humor News', template)
