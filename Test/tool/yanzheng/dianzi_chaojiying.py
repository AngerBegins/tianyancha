from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
from selenium.webdriver import ActionChains

from tool.yanzheng.chaojiying import Chaojiying_Client

chaojiying = Chaojiying_Client('18672922327', 'chx1234567', '96001')
logger = logging.getLogger('chaojiying')
def dianzi(url,cookie):
    cookies = cookie
    driver = webdriver.Chrome('chromedriver.exe')
    cookies = cookies.split('; ')
    cookies = [{'name':item.split('=')[0],'value':item.split('=')[1]} for item in cookies]
    driver.get(url)
    driver.delete_all_cookies()
    for cookie in  cookies:
        driver.add_cookie(cookie_dict = cookie)
    driver.save_screenshot('capture_html.png')
    img = driver.find_element_by_id('targetImgie')
    img1 = driver.find_element_by_id('bgImgie')
    x1 = img.location['x']
    y1 = img.location['y']
    x2 = img1.location['x']+img1.size['width']
    y2 = img1.location['y']+img1.size['height']
    im = Image.open('capture_html.png')
    im = im.crop((x1, y1, x2, y2))
    im.save('pic.png')
    #通过超级鹰识别坐标点
    im = open('pic.png', 'rb').read()
    sb_data = chaojiying.PostPic(im, 9004)
    print(sb_data)
    if sb_data['err_no'] == 0:
        points = sb_data['pic_str'].split('|')
        for point in points:
            x,y = [int(i) for i in point.split(',')]
            ActionChains(driver).move_to_element_with_offset(img,x,y).click().perform()
            time.sleep(1)
        driver.find_element_by_id('submitie').click()
        time.sleep(5)
        if driver.title == '天眼查校验':
            logger.info('超级鹰打码失败')
            chaojiying.ReportError(sb_data['pic_id'])
    time.sleep(3)
    print(driver.current_url)
    print(driver.page_source)
    driver.quit()
    logger.info('超级鹰打码完成')
    return True