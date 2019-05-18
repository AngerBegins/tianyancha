import requests
import re
import json
from scrapy.selector import Selector
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
cookie = 'ssuid=6527741260; TYCID=babafd80752411e99e230f9352d83617; undefined=babafd80752411e99e230f9352d83617; _ga=GA1.2.1816938050.1557713623; _gid=GA1.2.2138863130.1557713623; aliyungf_tc=AQAAALMXliNBjwcAku+tO1Y++10CYqGz; bannerFlag=undefined; csrfToken=envhn2m9ApAiqcEHj-Zsz6Jz; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1557714344,1557796332,1557801183,1557885471; RTYCID=9dcf7b0e16cd4b77bedbc31e56e09bc9; CT_TYCID=c7622262a0ba47dab156e60815c8d72e; cloud_token=3e23423119d849f8b70fc5b50aa57a68; token=86503244d66c4a5abe6f5801ed99dcb2; _utm=9983c3b5f136454387cb0420a7ae6130; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%25AD%2599%25E8%2586%2591%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzk3MTI3NDc5MyIsImlhdCI6MTU1NzkwMzAzOSwiZXhwIjoxNTg5NDM5MDM5fQ.kr5bzqFIIBOcxrwZKXJwiz5iyYFKQ8w5S2CNpSNvChumH1lULxu2kAbiEGULHxrxq87Cv5sdJTiNsropTv5Umg%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213971274793%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzk3MTI3NDc5MyIsImlhdCI6MTU1NzkwMzAzOSwiZXhwIjoxNTg5NDM5MDM5fQ.kr5bzqFIIBOcxrwZKXJwiz5iyYFKQ8w5S2CNpSNvChumH1lULxu2kAbiEGULHxrxq87Cv5sdJTiNsropTv5Umg; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1557903051'
url = "https://www.tianyancha.com/search?key="
headers ={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
"Cookie": cookie
}
def a(list1,list2):
    d = {}
    for i, j in zip(list1,list2):
        d[i] = j
    return d
def b(url,xpath1,xpath2):
    selector = Selector(text=requests.get(url,headers,verify=False))
    selector.xpath(xpath1).extract()
    selector.xpath(xpath2)

def fun(names,codes,urls):
    d={}
    for name,code,url in zip(names,codes,urls):
        d[name] = {}
        d[name]['code'] = code
        d[name]['url'] = url
    return d
if __name__ == '__main__':
    req = requests.get(url, headers=headers, verify=False)
    s = Selector(text=req.text)
    # #机构类型
    # organization_name = s.xpath('//div[@class="folder-body"]/div[1]/div/a/text()').extract()
    # organization_url = s.xpath('//div[@class="folder-body"]/div[1]/div/a/@href').extract()
    # organization_code = [re.search('companyType=(.*)',i).group(1) for i in organization_url]
    # organization = fun(organization_name,organization_code,organization_url)
    # config = {'organization': organization}
    # json.dump(config, open("config.json", "w"), ensure_ascii=False)
    # #省份
    # Province={}
    # Provinces_name = s.xpath('//div[@class="folder-body"]/div[2]/div/a/text()').extract()
    # Province_url = s.xpath('//div[@class="folder-body"]/div[2]/div/a/@href').extract()
    # Province_code = [re.search('base=(.*)',i).group(1) for i in Province_url]
    # Province = fun(Provinces_name,Province_code,Province_url)
    # config = {'organization': organization,'Province':Province}
    # json.dump(config, open("config.json", "w"), ensure_ascii=False)
    # #市
    #
    # for i in Province.keys():
    #     selector = Selector(text=requests.get(Province[i]['url'], headers=headers, verify=False).text)
    #     city_name = selector.xpath('//div[@class="filter-scope -expand"][1]/div/a/text()').extract()
    #     city_url = selector.xpath('//div[@class="filter-scope -expand"][1]/div/a/@href').extract()
    #     city_code = [re.search('base=(.*)', i).group(1) for i in city_url]
    #     Province[i]['city'] = fun(city_name,city_code,city_url)
    # config = {'organization': organization,'Province':Province}
    # json.dump(config, open("config.json", "w"), ensure_ascii=False)
    # config = json.load(open('config.json', 'r'))
    # Province = config['Province']
    # organization = config['organization']
    # #县
    # for i in Province.keys():
    #     if Province[i]['city'] != {}:
    #         for j in Province[i]['city'].keys():
    #             if Province[i]['city'][j]['county'] == {}:
    #                 response = requests.get(Province[i]['city'][j]['url'], headers=headers, verify=False)
    #                 if response.url == Province[i]['city'][j]['url']:
    #                     selector = Selector(text=response.text)
    #                     county_name = selector.xpath('//div[@class="filter-scope -expand"][1]/div/a/text()').extract()
    #                     county_url = selector.xpath('//div[@class="filter-scope -expand"][1]/div/a/@href').extract()
    #                     county_code = [re.search('areaCode=(.*)', i).group(1) for i in county_url]
    #                     if county_name == []:
    #                         Province[i]['city'][j]['county'] = None
    #                     else:
    #                         Province[i]['city'][j]['county'] = fun(county_name,county_code ,county_url)
    #                 else:
    #                     Province[i]['city'][j]['county'] = {}
    # config = {'organization': organization, 'Province': Province}
    # json.dump(config, open("config.json", "w"), ensure_ascii=False)

    #资本
    # Registered_capital = {}
    # #成立时间
    # Establishment_time = {}
    # #行业分类
    config = json.load(open('config.json', 'r'))
    Province = config['Province']
    organization = config['organization']
    Industry = config['Industry']
    # Industry_name = s.xpath('//div[@class="folder-body"]/div[5]/div/a/text()').extract()
    # Industry_url = s.xpath('//div[@class="folder-body"]/div[5]/div/a/@href').extract()
    # Industry_code = [re.search('search/(.*)',i).group(1) for i in Industry_url]
    # Industry = fun(Industry_name,Industry_code,Industry_url)
    # for i in Industry.keys():
    #     if Industry[i] != {}:
    #         selector = Selector(text=requests.get(Industry[i]['url'], headers=headers, verify=False).text)
    #         Industry2_name = selector.xpath('//div[@class="folder-body"]/div[5]/div/a/text()').extract()
    #         Industry2_url = selector.xpath('//div[@class="folder-body"]/div[5]/div/a/@href').extract()
    #         Industry2_code = [re.search('search/(.*)',i).group(1) for i in Industry2_url]
    #         Industry[i]['Industry2'] = fun(Industry2_name,Industry2_code,Industry2_url)

    for i in Industry.keys():
        for j in Industry[i]['Industry2'].keys():
            if Industry[i]['Industry2'][j]['Industry3'] == None:
                response = requests.get(Industry[i]['Industry2'][j]['url'], headers=headers, verify=False)
                if response.url == Industry[i]['Industry2'][j]['url']:
                    selector = Selector(text=response.text)
                    Industry3_name = selector.xpath('//div[@class="filter-scope -expand"]/div/a/text()').extract()
                    Industry3_url = selector.xpath('//div[@class="filter-scope -expand"]/div/a/@href').extract()
                    Industry3_code = [re.search('search/(.*)', i).group(1) for i in Industry3_url]
                    Industry[i]['Industry2'][j]['Industry3'] = fun(Industry3_name, Industry3_code,Industry3_url)
                else:
                    Industry[i]['Industry2'][j]['Industry3'] = None
    #
    # #企业描述
    # description ={}
    config = {'organization':organization,'Province':Province,'Industry':Industry}
    json.dump(config,open("config.json","w"), ensure_ascii=False)

