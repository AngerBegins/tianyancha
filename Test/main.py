import json
import re
import requests
import random
import logging
from setting import UA
import os
from scrapy.selector import Selector

from tool.db.database import mysql, mongo
from tool.yanzheng.dianzi_chaojiying import dianzi
# from tool.yanzheng.yanzheng import crack


# headers ={
# "User-Agent":random.choice(UA),
# "Cookie": cookie
# }

logger = logging.getLogger('tanyancha')
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("spider.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)
with open('start.txt', 'r') as fr:
    start_url = fr.read()
class tanyancha(object):
    def __init__(self):
        self.state = False
        self.start_url = re.sub('/p\d','',start_url)
        self.config = json.load(open('config.json', 'r'))
        # self.cookie = crack.crack()
        self.cookie = 'ssuid=6527741260; TYCID=babafd80752411e99e230f9352d83617; undefined=babafd80752411e99e230f9352d83617; _ga=GA1.2.1816938050.1557713623; _gid=GA1.2.2138863130.1557713623; RTYCID=69687c75cc83418f94647feb8570ae32; CT_TYCID=508db29cb9ad47dfa439ca8d038c484c; aliyungf_tc=AQAAAL8umgDP1gcAku+tO0QE+OaE6anD; bannerFlag=undefined; csrfToken=7lCAXGhvgHGVQ-48oA2Vj0M1; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1557973793,1557990897,1558054785,1558141807; cloud_token=5636cd06046d4024ba067ac5ba141114; _gat_gtag_UA_123487620_1=1; token=df170614b231452cbccc61970b7c3302; _utm=76c292887fe74cb38a490990a794a79c; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%25AD%2599%25E8%2586%2591%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzk3MTI3NDc5MyIsImlhdCI6MTU1ODE2MjMwMiwiZXhwIjoxNTg5Njk4MzAyfQ.KMMftRsexPfvFL19l97XZJtDGDSN4lSiYiEoogn5BFeZTWtKMbsIf4yfVZz3QebhK5QH3Fjae86CEeY_0RvZ_Q%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213971274793%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzk3MTI3NDc5MyIsImlhdCI6MTU1ODE2MjMwMiwiZXhwIjoxNTg5Njk4MzAyfQ.KMMftRsexPfvFL19l97XZJtDGDSN4lSiYiEoogn5BFeZTWtKMbsIf4yfVZz3QebhK5QH3Fjae86CEeY_0RvZ_Q; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1558162306'
        self.UA = random.choice(UA)

    def main(self):
        self.run_provice()

    def run_provice(self):
        for i in self.config['Province'].keys():
            province = self.config['Province'][i]
            if province['city'] == {}:
                response = self.make_request(province['url'])
                #请求出错跳过当前页
                if isinstance(response, str):
                    logger.info('%s数据获取失败'%response)
                    self.run_Industry(response)
                else:
                    state = self.click_num(response)
                    # 列表页没有数据
                    if state == 1:
                        continue
                    # 列表页数据大于200
                    if state == 2:
                        self.run_Industry(response.url)
                    # 列表数据少于200
                    if state == 3:
                        self.get_company(response)
                        continue
            else:
                #遍例市
                for j in province['city'].keys():
                    city = province['city'][j]
                    if city['county'] == None or city['county'] == 'None':
                        response = self.make_request(city['url'])
                        if isinstance(response, str):
                            self.run_Industry(response)
                        else:
                            state = self.click_num(response)
                            # 列表页没有数据
                            if state == 1:
                                continue
                            # 列表页数据大于200
                            if state == 2:
                                self.run_Industry(response.url)
                            # 列表数据少于200
                            if state == 3:
                                self.get_company(response)
                                continue
                    else:
                        for k in city['county'].keys():
                            county = city['county'][k]
                            response = self.make_request(county['url'])
                            if isinstance(response, str):
                                self.run_Industry(response)
                            else:
                                state = self.click_num(response)
                                # 列表页没有数据
                                if state == 1:
                                    continue
                                # 列表页数据大于200
                                if state == 2:
                                    self.run_Industry(response.url)
                                # 列表数据少于200
                                if state == 3:
                                    self.get_company(response)
                                    continue


    def run_Industry(self,base_url):
        for i in self.config['Industry'].keys():
            Industry = self.config['Industry'][i]
            if Industry['Industry2'] == {}:
                code = Industry['code']
                url = re.sub('\?', '/{}?'.format(code), base_url)
                response = self.make_request(url)
                if isinstance(response, str):
                    self.run_age(response)
                else:
                    state = self.click_num(response)
                    # 列表页没有数据
                    if state == 1:
                        continue
                    # 列表页数据大于200
                    if state == 2:
                        self.run_age(response.url)
                    # 列表数据少于200
                    if state == 3:
                        self.get_company(response)
                        continue
            else:
                #遍例市
                for j in Industry['Industry2'].keys():
                    Industry2 = Industry['Industry2'][j]
                    if Industry2['Industry3'] == None or Industry2['Industry3'] == 'None':
                        code = Industry2['code']
                        url = re.sub('\?', '/{}?'.format(code), base_url)
                        response = self.make_request(url)
                        if isinstance(response, str):
                            self.run_age(response.url)
                        else:
                            state = self.click_num(response)
                            # 列表页没有数据
                            if state == 1:
                                continue
                            # 列表页数据大于200
                            if state == 2:
                                self.run_age(response.url)
                            # 列表数据少于200
                            if state == 3:
                                self.get_company(response)
                                continue
                    else:
                        for k in Industry2['Industry3'].keys():
                            Industry3 = Industry2['Industry3'][k]
                            code = Industry3['code']
                            url = re.sub('\?', '/{}?'.format(code), base_url)
                            response = self.make_request(url)
                            if isinstance(response, str):
                                self.run_age(response)
                            else:
                                state = self.click_num(response)
                                # 列表页没有数据
                                if state == 1:
                                    continue
                                # 列表页数据大于200
                                if state == 2:
                                    self.run_age(response.url)
                                # 列表数据少于200
                                if state == 3:
                                    self.get_company(response)
                                    continue


    def run_age(self,base_url):
        age_code = ['e01','e015','e510','e1015','e15']
        for i in age_code:
            url = re.sub('\?', '-{}?'.format(i),base_url)
            response = self.make_request(url)
            if isinstance(response, str):
                self.run_money(response)
            else:
                state = self.click_num(response)
                # 列表页没有数据
                if state == 1:
                    continue
                # 列表页数据大于200
                if state == 2:
                    self.run_money(response.url)
                # 列表数据少于200
                if state == 3:
                    self.get_company(response)
                    continue


    def run_money(self,base_url):
        money_code = ['r0100', 'r100200', 'r200500', 'r5001000', '-r1000']
        for i in money_code:
            url = re.sub('-', '-{}-'.format(i), base_url)
            response = self.make_request(url)
            if isinstance(response, str):
                continue
            else:
                state = self.click_num(response)
                # 列表页没有数据
                if state == 1:
                    continue
                # 列表页数据大于200
                if state == 2:
                    self.get_company(response)
                # 列表数据少于200
                if state == 3:
                    self.get_company(response)
                    continue

    def get_company(self,response):
        company_name_url = self.get_company_url(response)
        for company in company_name_url:
            name = company.split('_')[0]
            url = company.split('_')[1]
            #插入mysql
            id = re.search('company/(\d+)', url).group(1)
            sql = 'insert into company values ("{}","{}","{}")'
            mysql.insert(sql.format(id,name,url))
            #插入mongodb
            mongo.insert({'_id':id,'name':name,'url':url})



    def next_page(self,url):
        response = self.make_request(url)
        if isinstance(response, str):
            return []
        company_name_url = self.get_company_url(response)
        return company_name_url

    def sort_time(self,url):
        response = self.make_request(url)
        if isinstance(response, str):
            return []
        company_urls = self.get_company_url(response)
        return company_urls

    def get_company_url(self,response):
        selector = Selector(text=response.text)
        num = int(selector.xpath('//span[@class="tips-num"]/text()').extract_first())
        sort = selector.xpath('//a[contains(@class,"selected")]/text()').extract_first()
        next_url = selector.xpath('//a[@class="num -next"]/@href').extract_first()
        if num <= 100:
            company_urls = selector.xpath('//div[@class="content"]/div[@class="header"]/a/@href').extract()
            company_names = selector.xpath('//div[@class="content"]/div[@class="header"]/a/text()').extract()
            company_name_url = [name + '_' + url for name, url in zip(company_names, company_urls)]
            if next_url == None or next_url == '':
                return company_name_url
            company_name_url.extend(self.next_page(next_url))
            return company_name_url
        elif num <=200 and sort == '默认排序':
            #成立日期从早到晚
            date_url_one = selector.xpath('//div[@class="content search-sort-content"]/div[4]/a/@href').extract_first()
            #成立日期从晚到早
            date_url_two = selector.xpath('//div[@class="content search-sort-content"]/div[5]/a/@href').extract_first()
            company_urls_one = self.sort_time(date_url_one)
            company_urls_two = self.sort_time(date_url_two)
            company_urls_one.extend(company_urls_two)
            return list(set(company_urls_one))
        elif num > 200 and sort == '默认排序':
            # 成立日期从早到晚
            date_url_one = selector.xpath('//div[@class="content search-sort-content"]/div[2]/a/@href').extract_first()
            # 成立日期从晚到早
            date_url_two = selector.xpath('//div[@class="content search-sort-content"]/div[3]/a/@href').extract_first()
            company_urls_one = self.get_company_url(date_url_one)
            company_urls_two = self.get_company_url(date_url_two)
            logger.info('%s只爬取200条数据没有爬完整'%response.url)

            company_urls_one.extend(company_urls_two)
            return company_urls_one
        elif sort != '默认排序':
            company_urls = selector.xpath('//div[@class="content"]/div[@class="header"]/a/@href').extract()
            company_names = selector.xpath('//div[@class="content"]/div[@class="header"]/a/text()').extract()
            company_name_url = [name + '_' + url for name, url in zip(company_names, company_urls)]
            if 'p6?' not in next_url:
                company_name_url.extend(self.next_page(next_url))
            return company_name_url


    def click_num(self,response):
        selector = Selector(text = response.text)
        num = selector.xpath('//span[@class="tips-num"]/text()').extract_first()
        if num == None:
            logger.info('当前{}没有数据'.format(response.url))
            return 1
        if num == '100000+':
            logger.info('当前{}页有100000+条数据要细分'.format(response.url))
            return 2
        else:
            if int(num) < 200:
                return 3
            else:
                return 2

    def make_request(self,url):
        if self.start_url == url:
            self.state = True
        if self.state:
            with open('start.txt', 'w') as f:
                f.write(url)
            try:
                response = requests.get(url, headers={"User-Agent":self.UA,"Cookie":self.cookie}, verify=False)
            except:
                logger.error('%s请求失败')
            else:
                if response.url.startswith('https://www.tianyancha.com/login'):
                    logger.info("cookie失效,重新模拟登录获取cookie")
                    # self.cookie = crack.crack()
                    return self.make_request(url)
                if response.url.startswith('https://antirobot.tianyancha.com/captcha/verify'):
                    logger.info("出现点字验证吗")
                    state = dianzi(response.url,self.cookie)
                    if state:
                        return self.make_request(url)
                if url == response.url:
                    return response
            logger.info('%s数据获取失败' % url)
            return url
        print(self.start_url)
        logger.info('%s数据已经获取' % url)
        return url


if __name__ == '__main__':
    t =tanyancha()
    t.main()
    print(t.config)

