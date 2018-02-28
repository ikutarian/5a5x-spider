import requests
from lxml import etree


def getHTML(url):
    try:
        user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get(url, headers = user_agent)
        r.raise_for_status()
        r.encoding = 'gbk'
        return r.text
    except:
        return ''


def write_to_file(txt):
    txt = txt.replace(u'\xa0', ' ')
    with open('5a5x.txt', 'a+') as f:        
        f.write(txt)
        f.close()
        
        
def main():
    base_url = 'http://www.5a5x.com/'
    html = getHTML(base_url + 'wode_source/etools/')
    doc = etree.HTML(html)
    total_page = int(doc.xpath('//div[@id="pages"]/b[2]/text()')[0][1:])
    
    for page in range(1, total_page + 1):
        print('正在爬取第{}页'.format(page))
        page_url = base_url + '/wode_source/etools/{}.html'.format(page)
        html = getHTML(page_url)
        doc = etree.HTML(html)
        down_list = doc.xpath('//dl[@class="down_list"]')
        if len(down_list) == 0:
            print('该页没有数据，继续爬取下一页')
            continue
        txt = ''        
        for down in down_list:
            url = base_url + down.xpath('./dt/a/@href')[0]            
            title = down.xpath('./dt/a/text()')[0]           
            desc = down.xpath('./dd[@class="down_txt"]/text()')[0]
            file_size = down.xpath('./dd[@class="down_attribute align_r"]/span[1]/text()')[0]            
            star = down.xpath('./dd[@class="down_attribute align_r"]/span[2]/text()')[0]
            update_time = down.xpath('./dd[@class="down_attribute align_r"]/span[3]/text()')[0]
            txt += '{}\n{}\n{}\n{}\n{}\n{}\n\n'.format(url, title, desc, file_size, star, update_time)
        write_to_file(txt)
    print('网页爬取完毕')

if __name__ == '__main__':
    main()