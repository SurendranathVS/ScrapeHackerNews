from bs4 import BeautifulSoup
import requests

url = 'https://news.ycombinator.com/'
res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')

titleline = soup.select('.titleline')
subtext = soup.select('.subtext')

def GetImportantArticlesSorted(hn):
    return sorted(hn, key=lambda k:k['vote'], reverse=True)


def GetImportantArticles(titleline,subtext):
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



print(GetImportantArticles(titleline, subtext))

