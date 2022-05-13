import yagmail
import requests
from bs4 import BeautifulSoup

all_posts = [[], []]

web_page_1 = requests.get('https://www.today.com/news/good-news')
soup = BeautifulSoup(web_page_1.text, 'lxml')
posts_source_1 = soup.find_all('h2', class_='tease-card__headline tease-card__title tease-card__title--today relative')
for post in posts_source_1:
    post_title = post.text
    post_link = post.a['href']
    all_posts[0].append(post_title)
    all_posts[1].append(post_link)

web_page_2 = requests.get('https://www.goodnewsnetwork.org/category/news/inspiring/')
soup = BeautifulSoup(web_page_2.text, 'lxml')
posts_source_2 = soup.find_all('h3', class_='entry-title td-module-title')
for post in posts_source_2:
    if 'EPISODE' not in post.a.text:
        post_title = post.text
        post_link = post.a['href']
        all_posts[0].append(post_title)
        all_posts[1].append(post_link)

html = ''

for index, (title, link) in enumerate(zip(all_posts[0], all_posts[1])):
    print(index, link, title)
    html_title = f'<h2><a href="{link}">{(index + 1)}. {title}</a></h2>'
    html += html_title

html = f'''<h1>The Humor News 🙈</h1>
<h2>By: Tolu Joel</h2>'
{html}
<p><span>Scraped with love by Tolu Joel...hehe ❤️</span>
<span><a href="https://github.com/tolu-joel">Github</a></span>
<span><a href="https://linkedin.com/in/tolujoel">LinkedIn</a></span>
<span><a href="https://twitter.com/tolu_joel_">Twitter</a></span>
<span><a href="https://instagram.com/tolu_joel_">Instagram</a></span></p>
'''
# print(html)
email = yagmail.SMTP('your@gmail.com', input('Email Password: '))
email.send('receiver@gmail.com', 'The Humor News', html)
