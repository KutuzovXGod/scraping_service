import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('work',)

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]


def work(url,  city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://hh.ru'
    # url = 'https://podolsk.hh.ru/search/vacancy?text=Python+django&from=suggest_post&area=1'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            table = soup.find('div', id='a11y-main-content')
            if table:
                div_lst = table.find_all('div', attrs={'class': 'serp-item'})
                company_list = table.find_all('div', attrs={'class': 'vacancy-serp-item__info'})
                for div in zip(div_lst, company_list):
                    title = div[0].find('h3')
                    href = title.a['href']
                    company = 'No name'
                    logo = div[0].find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append(
                        {
                            'title': title.text,
                            'url': href,
                            'description': div[-1].text,
                            'company': company, 'city_id': city, 'language_id': language
                        },
                    )
            else:
                errors.append({'url': url, 'title': 'table doesnt  exist'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://podolsk.hh.ru/search/vacancy?text=Python+django&from=suggest_post&area=1'
    jobs, errors = work(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
