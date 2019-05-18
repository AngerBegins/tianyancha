import requests
import re
from scrapy.selector import Selector
import json

from setting import UA
from tool.db.database import mongo
from tool.yanzheng.dianzi_chaojiying import dianzi
import random

import logging

from tool.yanzheng.yanzheng import crack

logger = logging.getLogger('companyDetial')
class CompanyDetial:
    def __init__(self):
        self.config = json.load(open('config.json', 'r'))
        self.cookie = crack.crack()
        # self.cookie = 'ssuid=6527741260; TYCID=babafd80752411e99e230f9352d83617; undefined=babafd80752411e99e230f9352d83617; _ga=GA1.2.1816938050.1557713623; _gid=GA1.2.2138863130.1557713623; aliyungf_tc=AQAAAETyoRpkUAQAku+tO2bgaQg0rNQl; bannerFlag=undefined; csrfToken=Q--epo-AQB8sWNYEL0Ei4hj2; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1557971963,1557973793,1557990897,1558054785; RTYCID=69687c75cc83418f94647feb8570ae32; CT_TYCID=508db29cb9ad47dfa439ca8d038c484c; cloud_token=10ae24fda59e4b78a1b32353a96f4a60; token=38594753dece4d1c925a606e437e6d24; _utm=a859332691af4dca837be85631cab4f6; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%25AD%2599%25E8%2586%2591%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzk3MTI3NDc5MyIsImlhdCI6MTU1ODA4MDg1NiwiZXhwIjoxNTg5NjE2ODU2fQ.bQljYJgdU64anjGLTAeUtw41woSLSfYnF-SF9woYqCnDvULLmC83s-36T0Zn7_xgyykzPfonpAPklfKshqt6Vg%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213971274793%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzk3MTI3NDc5MyIsImlhdCI6MTU1ODA4MDg1NiwiZXhwIjoxNTg5NjE2ODU2fQ.bQljYJgdU64anjGLTAeUtw41woSLSfYnF-SF9woYqCnDvULLmC83s-36T0Zn7_xgyykzPfonpAPklfKshqt6Vg; _gat_gtag_UA_123487620_1=1; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1558080862'
        self.UA = random.choice(UA)


    def make_request(self, url):
        try:
            response = requests.get(url, headers={'Referer': 'https://www.tianyancha.com/search?base=shenyang',"User-Agent": self.UA, "Cookie": self.cookie}, verify=False)
        except:
            logger.error('%s请求失败' % url)
        else:
            if response.url.startswith('https://www.tianyancha.com/login'):
                logger.info("cookie失效,重新模拟登录获取cookie")
                self.cookie = crack.crack()
                return self.make_request(url)
            if response.url.startswith('https://antirobot.tianyancha.com/captcha/verify'):
                logger.info("出现点字验证吗")
                return self.make_request(url)
            if url == response.url:
                return response
        logger.info('%s请求不成功' % url)
        return url


    def get_company_message(self,url):
        response = self.make_request(url)
        if isinstance(response, str):
            print(response)
            logger.info('%获取信息失败')
        else:
            selector = Selector(text=response.text)
            company = {}

            company['daibiaoren'] = selector.xpath('//div[@class="humancompany"]/div[@class="name"]/a/@title').extract_first()
            company['name'] = selector.xpath('//h1[@class="name"]/text()').extract_first()
            company['zt'] = selector.xpath('//div[@class="tag-common -normal"]/text()').extract_first()
            company['phone'] = selector.xpath('//span[text()="电话："]/following-sibling::span[1]/text()').extract_first()
            company['web'] = selector.xpath('//span[text()="网址："]/following-sibling::span[1]/text()').extract_first()
            company['introduct'] = selector.xpath('//span[text()="简介："]/following-sibling::span[1]/text()').extract_first()
            company['email'] = selector.xpath('//span[text()="邮箱："]/following-sibling::span[1]/text()').extract_first()
            company['address'] = selector.xpath('//span[text()="地址："]/following-sibling::div[1]/div/text()').extract_first()
            company['message_update'] = selector.xpath('//span[@class="updatetimeComBox"]/text()').extract_first

            #公司基本信息
            company['rg_money'] = selector.xpath('//td[text()="注册资本"]/following-sibling::td[1]/div/text()').extract_first()
            company['date'] = selector.xpath('//td[text()="成立日期"]/following-sibling::td[1]/div/text()').extract_first()
            company['registration_number'] = selector.xpath('//td[text()="工商注册号"]/following-sibling::td[1]/text()').extract_first()
            company['xinyong_number'] = selector.xpath('//td[text()="统一社会信用代码"]/following-sibling::td[1]/text()').extract_first()
            company['jigou_number'] = selector.xpath('//td[text()="组织机构代码"]/following-sibling::td[1]/text()').extract_first()
            company['nasui_number'] = selector.xpath('//td[text()="纳税人识别号"]/following-sibling::td[1]/text()').extract_first()
            company['company_type'] = selector.xpath('//td[text()="公司类型"]/following-sibling::td[1]/text()').extract_first()
            company['qixian'] = selector.xpath('//td[text()="营业期限"]/following-sibling::td[1]/span/text()').extract_first()
            company['hangye'] = selector.xpath('//td[text()="行业"]/following-sibling::td[1]/text()').extract_first()
            company['hz_data'] = selector.xpath('//td[text()="核准日期"]/following-sibling::td[1]/text()').extract_first()
            company['dengji'] = selector.xpath('//td[text()="登记机关"]/following-sibling::td[1]/text()').extract_first()
            company['fanwei'] = selector.xpath('//td[text()="经营范围"]/following-sibling::td[1]//div/text()').extract_first()

            #股东信息
            gudong = {}
            gudong['id'] = selector.xpath('')
            gudong['name'] = selector.xpath('//a[@tyc-event-ch="CompangyDetail.gudong.ziranren"]/text()').extract()
            gudong['proportion'] =selector.xpath('//*[@id="_container_holder"]/table/tbody/tr/td[3]/div/div/span/text()').extract()
            gudong['money'] =selector.xpath('//*[@id="_container_holder"]/table/tbody/tr/td[4]/div/span/text()').extract()
            gudong['date'] =selector.xpath('//*[@id="_container_holder"]/table/tbody/tr/td[5]/div/span/text()').extract()


            #主要人员
            person = {}
            person['id'] = selector.xpath('//*[@id="_container_staff"]/div/table/tbody/tr/td[2]/div/div[2]/a/@href').extract()
            person['name'] = selector.xpath('//*[@id="_container_staff"]/div/table/tbody/tr/td[2]/div/div[2]/a/text()').extract()
            person['position'] = selector.xpath('//*[@id="_container_staff"]/div/table/tbody/tr/td[3]/span/text()').extract()


        return company, gudong

    def insert_db(self):
        mongo.insert()

if __name__ == '__main__':
    company =CompanyDetial()
    count=0
    d= 0
    while True:
        d = company.get_company_message('https://www.tianyancha.com/company/3090180824')
        count +=1
        print(d)
        print(count)


