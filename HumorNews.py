import yagmail
import requests
from bs4 import BeautifulSoup

all_posts = [[], []]  # [0] = post_title, [1] = post_link


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


get_content('https://www.today.com/news/good-news', 'h2', 'tease-card__headline tease-card__title tease-card__title--today relative')
get_content('https://www.goodnewsnetwork.org/category/news/inspiring/', 'h3', 'entry-title td-module-title')
get_content('https://www.ladbible.com/weird', 'div', 'css-32xpko-cardText-padding-padding-padding-padding-padding-padding-padding')
get_content('https://www.theweek.co.uk/odd-news-0', 'div', 'polaris__article-card -layout-default -default polaris__article-group--single')

all_posts = set(zip(all_posts[0], all_posts[1]))  # randomize posts & filter duplicates 🥴
html_template = ''

for index, (title, link) in enumerate(all_posts):
    html_title = f'<h2><a href="{link}" style="text-decoration: none; color: royalblue;">{(index + 1)}. {title}</a></h2>'
    html_template += html_title

html_template = f'''
    <h1 style="text-align: center;font-family: 'Courier New', Courier, monospace;">The Humor News 🙈</h1>
    <h3 style="text-align: center;font-family: 'Courier New', Courier, monospace;">❤️ By Tolu Joel</h3>
    <div style="display: flex;justify-content: center;align-items: center;"> <a href="https://github.com/tolu-joel"><button style="border: none;color: white;padding: 16px 32px;text-align: center;text-decoration: none;display: inline-block;font-size: 16px;margin: 4px 2px;transition-duration: 0.4s;cursor: pointer;background-color: white;color: black;border: 2px solid #4CAF50;">Github</button></a>
    <a href="https://twitter.com/tolu_joel_"><button style="border: none;color: white;padding: 16px 32px;text-align: center;text-decoration: none;display: inline-block;font-size: 16px;margin: 4px 2px;transition-duration: 0.4s;cursor: pointer;background-color: white;color: black;border: 2px solid #4CAF50;">Twitter</button></a>
    <a href="https://linkedin.com/in/tolujoel"><button style="border: none;color: white;padding: 16px 32px;text-align: center;text-decoration: none;display: inline-block;font-size: 16px;margin: 4px 2px;transition-duration: 0.4s;cursor: pointer;background-color: white;color: black;border: 2px solid #4CAF50;">LinkedIn</button></a>
    <a href="https://instagram.com/tolu_joel_"><button style="border: none;color: white;padding: 16px 32px;text-align: center;text-decoration: none;display: inline-block;font-size: 16px;margin: 4px 2px;transition-duration: 0.4s;cursor: pointer;background-color: white;color: black;border: 2px solid #4CAF50;">Instagram</button></a></div>
    <div style="margin: auto;width: 60%;border: 2px solid #4CAF50;padding: 50px;border-radius: 20px;margin-top: 100px;">{html_template}</div>
'''

email = yagmail.SMTP('programmerlaptop@gmail.com', input('Email Password: '))
email.send('toluisjoel@gmail.com', 'TheHumorNews', html_template)
