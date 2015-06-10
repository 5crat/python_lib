#!/usr/bin/env python
#-*-coding:utf-8-*-
#-*-author:scrat-*-

import sys
import urllib2
from lxml import etree
from lib.httprequest import HttpRequest, check_proxy


#国内高匿代理
GNGN = 'http://www.xici.net.co/nn/'
#国内普通代理
GNPT = 'http://www.xici.net.co/nt/'
#国外高匿代理
GWGN = 'http://www.xici.net.co/wn/'
#国外普通代理
GWPT = 'http://www.xici.net.co/wt/'



def check_proxy(proxyIp):
    """
    check http proxy status
    :param proxyIp
    :return bool:
    """
    p = proxyIp
    try:
        proxy_handler = urllib2.ProxyHandler(p)
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent',  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)')]
        urllib2.install_opener(opener)
        req = urllib2.Request('http://httpbin.org/ip')  # change the URL to test here
        html = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'Error code: ', e.code
        return e.code
    except Exception, detail:
        print "ERROR:", detail
        return False
    return True

def getProxyByXici(m='gnpt', nums=1):
    '''
    get Proxy Ip By www.xici.net.co
    :param m (value:gngn,gnpt,gwgn,gwpt):
    :param nums:
    :return dict or None:
    '''
    url = {
        'gngn': GNGN,
        'gnpt': GNPT,
        'gwgn': GWGN,
        'gwpt': GWPT
    }
    if url.has_key(m) == False:
        print "[ - ] Error :" + __file__ + " : function" + sys._getframe().f_code.co_name + " parameter 'm' value cann't use "+m
        return None
    if type(nums) != int:
        print "[ - ] Error : " + __file__ + " : function" + sys._getframe().f_code.co_name + " parameter 'nums' must int"
        return None

    proxyList = {'http': [], 'https': []}
    for num in range(1, nums+1):
        t = url[m] + str(num)
        ro = HttpRequest(target=t)
        r = ro.http_request()
        if r['status_code'] == '200':
            dom = etree.HTML(r['html'])
            for ip, port, method in zip(dom.xpath('//tr[@class]/td[3]'), dom.xpath('//tr[@class]/td[4]'), dom.xpath('//tr[@class]/td[7]')):
                proxyIp = {}
                if method.text.lower() == 'http':
                    proxyIp[method.text.lower()] = method.text.lower() + '://' + ip.text + ':' + port.text
                    proxyList['http'].append(proxyIp)
                elif method.text.lower() == 'https':
                    proxyIp[method.text.lower()] = method.text.lower() + '://' + ip.text + ':' + port.text
                    proxyList['https'].append(proxyIp)
        else:
            print url+'----------'+r['status_code']
            return None
    #print proxyList
    return proxyList

if __name__ == '__main__':
    pl = getProxyByXici(m='gnpta', nums=2)
