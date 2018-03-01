import requests
from lxml import etree
import os


base_url = 'http://www.5a5x.com/'
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
source_types = {
    'wode_source/etools/': '系统工具源码',
    'wode_source/eimage/': '图形图像源码',
    'wode_source/emedia/': '多媒体类源码',
    'wode_source/egame/': '游戏娱乐源码',
    'wode_source/edata/': '数据库类源码',
    'wode_source/ecom/': '模块控件源码',
    'wode_source/etrade/': '行业软件源码',
    'wode_source/enetwork/': '网络相关源码',
}


def getDoc(url):
    r = requests.get(url, headers = user_agent)
    r.raise_for_status()
    r.encoding = 'gbk'
    return etree.HTML(r.text)


def down_and_save_file(url, filename):
    r = requests.get(url, headers = user_agent)
    with open(filename + '.' + r.headers['Content-Type'], 'wb') as f:        
        f.write(r.content)
        f.close()

        
def main(dir, source_type):
    total_page = int(getDoc(base_url + source_type).xpath('//div[@id="pages"]/b[2]/text()')[0][1:])
    total_page = 1
    for page in range(1, total_page + 1):
        print('正在爬取第{}页'.format(page))
        page_url = base_url + source_type + '{}.html'.format(page)
        down_list = getDoc(page_url).xpath('//dl[@class="down_list"]')
        if len(down_list) == 0:
            print('该页没有数据，继续爬取下一页')
            continue
            
        for down in down_list:
            url = base_url + down.xpath('./dt/a/@href')[0]            
            title = down.xpath('./dt/a/text()')[0]            
            down_url = base_url + getDoc(url).xpath('//div[@id="down_address"]/a/@href')[0]
            file_url = base_url + getDoc(down_url).xpath('//a/@href')[0]
            down_and_save_file(file_url, os.path.join(dir, title))
            
    print('网页爬取完毕')

    
if __name__ == '__main__':
    for url, name in source_types.items():
        dir = os.path.join(os.getcwd(), name)
        if not os.path.exists(dir):
            os.mkdir(dir)
        main(dir, url)