#!/usr/bin/env python
#-*-coding:utf-8-*-
#-*-author:scrat-*-
######################################################################
###
###     Need python-requests and chardet model
###
######################################################################
import re
import chardet
import requests

#超时
timeout = 10
UserAgent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)'

class HttpRequest(object):
    """
        HTTP Request class
    """
    def __init__(
            self,
            target='',
            web_method='GET',
            data='',
            proxies={},
            timeout=10,
            useragent=UserAgent,
    ):
        self.target = target
        self.web_method = web_method
        self.data = data
        self.proxies = proxies
        self.timeout = timeout
        self.UserAgent = useragent
        self.headers = {
            'User-Agent': self.UserAgent,
            'Referer': self.target
        }

    def http_request(self):
        """
        http request method
        :return list {'status_code <str>':...,'header <dict>':....,'content <str>':...}
        """
        try:
            if not self.target:
                return
            methods = ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE']
            if self.web_method.upper() not in methods:
                print 'HTTP请求的方式错误,无法识别该方式： '+ self.web_method

            r = requests.request(
                self.web_method.upper(),
                self.target,
                data=self.data,
                headers=self.headers,
                proxies=self.proxies,
                timeout=self.timeout)
            check_jump_payloads = [
                'window.location\s?=\s?(.*);',
                'window.location.href\s?=\s?(.*);',
                '<meta http-equiv=\"refresh\".*url=(.*)\s?/>']

            for i in check_jump_payloads:
                check_jump = re.findall(i, r.content.lower())
                if check_jump:
                    addr = check_jump[0].strip('"')
                    if 'http' in addr:
                        self.target = addr
                    else:
                        r = requests.request(
                            self.web_method.upper(),
                            self.target + addr,
                            data=self.data,
                            headers=self.headers,
                            proxies=self.proxies,
                            timeout=self.timeout,
                        )
                    break
            html = r.content
            charset = chardet.detect(html)['encoding'].lower()

            if charset != 'utf8':
                html = html.decode(charset).encode('utf8')
            return {'status_code': str(r.status_code), 'header': r.headers, 'html':  html}
        except Exception as e:
            print 'error :  ' + str(e)
            return None

if __name__ == '__main__':
    proxy = {'http': 'http://122.96.59.106:80'}
    a = HttpRequest(target='http://www.baidu.com', proxies=proxy)
    b = a.http_request()
    for i in b:
        print b[i]