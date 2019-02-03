import os
import csv
import requests
from bs4 import BeautifulSoup

BASE_URL = os.environ['URL'] #?computers_grid%5Bperpage%5D=100'

def autorization(url):
    session = requests.Session()
    data = {'login': os.environ['LOGIN'], 'password': os.environ['PASSWORD']}
    session.post(url, data=data)
    return session.get(url).content


# def get_html(url):
#     response = autorization(url)
#     return response.content

def get_page_count(html):
    soup = BeautifulSoup(html, features='lxml')
    pagination = soup.find('div', class_='pagination')
    return int(pagination.find_all('a')[-2].text)

def parse(html):
    soup = BeautifulSoup(html, features='lxml')
    table = soup.find('table', class_='table table-striped')

    ips = []

    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        
        ips.append({
            'id': cols[0].text,
            'type': cols[1].text,
            'ip': cols[2].a.text.split(),
            'description': cols[3].a.text.replace('\n', ''),
        })

    return ips

def save(ips, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('id', 'type', 'ip', 'description'))

        for ip in ips:
            writer.writerow((ip['id'], ip['type'], ip['ip'], ip['description']))



def main():

    page_count = get_page_count(autorization(BASE_URL))
    
    print(f'Всего найден остраниц {page_count}')

    ips = []

    for page in range(1, page_count + 1):
        print(page)
        print('парсинг %d%%' % (page / page_count * 100))
        ips.extend(parse(autorization(f'{BASE_URL}&computers_grid%5Bpage%5D={page}')))

    
    for ip in ips:
       print(ip)
    
    print(len(ips))

    save(ips, 'ips.csv')

if __name__ == '__main__':
    main()