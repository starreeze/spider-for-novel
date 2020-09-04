'https://ip.jiangxianli.com/api/proxy_ip'
#coding=utf-8
import requests, random, time

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
head = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
}


def test_ip(protocol, ip):
    try:
        head['User-Agent'] = random.choice(UserAgents)
        requests.get('http://book.zongheng.com/store/c0/c0/b0/u1/p1/v0/s9/t0/u0/i1/ALL.html', headers=head, proxies={protocol: ip}, timeout=6)
        return True
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout,
            requests.exceptions.ConnectionError, requests.exceptions.TooManyRedirects):
        return False


def get1proxy(protocol='', proxy=''):
    proxies = {}
    if len(proxy) > 0:
        proxies = {protocol: proxy}
    head['User-Agent'] = random.choice(UserAgents)
    res = requests.get('https://ip.jiangxianli.com/api/proxy_ip', headers=head, proxies=proxies).json()
    print('switch to proxy: ' + res['data']['ip'] + ':' + res['data']['port'])
    while not test_ip(res['data']['protocol'], res['data']['ip'] + ':' + res['data']['port']):
        time.sleep(3)
        res = requests.get('https://ip.jiangxianli.com/api/proxy_ip', headers=head,
                           proxies={res['data']['protocol']: res['data']['ip'] + ':' + res['data']['port']}).json()
        print('switch to proxy: ' + res['data']['ip'] + ':' + res['data']['port'])
    r = (res['data']['protocol'], res['data']['ip'] + ':' + res['data']['port'])
    return r


#print(get1proxy('http', '196.54.47.28:80'))