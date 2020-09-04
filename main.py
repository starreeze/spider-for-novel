#coding=utf-8
from bs4 import BeautifulSoup as bs
from getproxy2 import get1proxy
import requests, re, random, os
UserAgents = [
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50 ',
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
# 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
# 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
# 'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
]
proxy = get1proxy()
head = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
}


class Session:
    pageNum = 1
    bookNum = 1

    def __init__(self, p=1, b=1):
        self.pageNum = p
        self.bookNum = b

    def load(self, fileName):
        sessionFile = open(fileName, 'r')
        self.pageNum = int(sessionFile.readline())
        self.bookNum = int(sessionFile.readline())
        sessionFile.close()

    def save(self, fileName):
        sessionFile = open(fileName, 'w')
        sessionFile.write(str(self.pageNum) + '\n' + str(self.bookNum) + '\n')
        sessionFile.close()

def get(url):
    global proxy
    #time.sleep(random.uniform(0.1, 0.3))
    head['User-Agent'] = random.choice(UserAgents)
    r: bs
    def successful():
        nonlocal r
        try:
            r = bs(requests.get(url, headers=head, proxies={proxy[0]: proxy[1]}, timeout=6).content, 'lxml')
            return True
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError, requests.exceptions.TooManyRedirects):
            return False
    while not successful():
        proxy = get1proxy(proxy[0], proxy[1])
    return r


def get_chapter(url):
    title: None
    chapterSoup: bs
    global proxy
    def successful():
        nonlocal title, chapterSoup
        try:
            chapterSoup = get(url)
            title = chapterSoup.find_all('div', class_="title_txtbox")[0].string
            return True
        except (IndexError, requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError, requests.exceptions.TooManyRedirects):
            return False
    while not successful():
        proxy = get1proxy(proxy[0], proxy[1])
    content = ''
    contentDiv = chapterSoup.find_all('div', class_="content", itemprop="acticleBody")[0]
    for pTag in contentDiv.children:
        content += pTag.string + '\n'
    return title, content


if __name__ == '__main__':
    session = Session()
    if os.path.exists('session'):
        session.load('session')
    i = j = k = 1
    try:
        for i in range(session.pageNum, 259):
            print('webpage ' + str(i))
            url = 'http://book.zongheng.com/store/c0/c0/b0/u1/p' + str(i) + '/v0/s9/t0/u0/i1/ALL.html'
            j = 1
            soup = get(url)
            # print(soup)
            itList = soup.find_all('div', class_='bookbox fl')
            while len(itList) < 3:
                proxy = get1proxy(proxy[0], proxy[1])
                soup = get(url)
                itList = soup.find_all('div', class_='bookbox fl')
            for item in itList:
                if i == session.pageNum and j < session.bookNum:
                    j += 1
                    continue
                print('book ' + str(j))
                j += 1
                detailTag = item.find('a', href=re.compile(r'http://book.zongheng.com/book/\d*.html'))
                detailSoup = get(detailTag['href'])
                catalogSoup = get(detailSoup.find('a', class_='all-catalog')['href'])
                # get title and author
                titleDiv = catalogSoup.find_all('div', class_='book-meta')[0]
                title = titleDiv.find_all('h1')[0].string + '-' + titleDiv.find_all('a')[0].string
                bookFile = open('Books/' + title + '.txt', 'w')
                # get content
                k = 1
                for chapterTag in catalogSoup.find_all('a', href=re.compile(r'http://book.zongheng.com/chapter/\d*/\d*.html')):
                    if k % 5 == 0:
                        print('chapter ' + str(k))
                    k += 1
                    try:
                        title, content = get_chapter(chapterTag['href'])
                    except IndexError:
                        proxy = get1proxy(proxy[0], proxy[1])
                        title, content = get_chapter(chapterTag['href'])
                    bookFile.write(title + '\n')
                    bookFile.write(content)
                bookFile.close()
                Session(i, j-1).save('session')
    except (KeyboardInterrupt, requests.exceptions.ChunkedEncodingError):
        Session(i, j-1).save('session')
        print('Session saved to "session"')
        exit(-1)
