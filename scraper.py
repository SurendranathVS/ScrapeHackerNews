from re import sub
from bs4 import BeautifulSoup
import requests

url = 'https://news.ycombinator.com/'

def GetSiteData(url):

    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    titleline = soup.select('.titleline')
    subtext = soup.select('.subtext')
    
    return (titleline,subtext)

def GetImportantArticlesSorted(hn):
    return sorted(hn, key=lambda k:k['vote'], reverse=True)


def GetImportantArticles(url):
    titleline,subtext = GetSiteData(url)
    hn = []
    for idx, item in enumerate(titleline):
        link = item.find('a').get('href')
        article_name = item.find('a').getText()
        vote =subtext[idx].select('.score')         
        if len(vote):
            points = int(vote[0].getText().replace(' points',''))
            if points>99:
                hn.append({'article':article_name, 'link':link, 'vote':points})
    return GetImportantArticlesSorted(hn)

page = 1

articles = GetImportantArticles(url)

while True:
    
    print(articles,len(articles)) 

    require_more_articles = input('Enter Yes if more articles required: ')

    if require_more_articles.upper()=='YES':
        page += 1
        print(url + f'news?p={page}')
        articles.extend(GetImportantArticles(url + f'news?p={page}'))
    else:
        print('Thank you !')
        break

                            

