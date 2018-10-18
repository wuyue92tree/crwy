#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: IntelliJ IDEA
@file: selenium_api.py
@create at: 2018-10-15 11:51

这一行开始写关于本文件的说明与解释
"""

import os
import re
import time
import uuid

from PIL import Image
from crwy.spider import Spider
from crwy.exceptions import CrwyImportException

try:
    from selenium import webdriver
except ImportError:
    raise CrwyImportException(
        "You should install selenium first! suggestion: pip install "
        "selenium==3.6.0")
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class SeleniumApi(Spider):
    def __init__(self, driver_type='chrome',
                 hub_url='http://127.0.0.1:4444/wd/hub',
                 proxy=None, user_agent=None, use_hub=True,
                 logger=None):
        super(SeleniumApi, self).__init__(logger=logger)
        """
        :param driver_type: driver类型
        :param hub_url: hub server地址
        :param proxy: 代理地址
        :param user_agent: user_agent
        :param use_hub: 是否启用hub，为False时使用本地driver
        """
        self.driver_type = driver_type
        self.hub_url = hub_url
        self.proxy = proxy
        self.use_hub = use_hub
        self.user_agent = user_agent
        # device_pixel_ratio 用于处理高分屏dpi抠图
        self.device_pixel_ratio = 1
        self.driver = self.init_driver()
        self.driver.set_window_size(1280, 960)

    def _init_chrome_driver(self):
        chrome_options = webdriver.ChromeOptions()
        if self.proxy:
            chrome_options.add_argument('--proxy-server=%s' % self.proxy)
        if self.user_agent:
            chrome_options.add_argument('--user-agent=%s' % self.user_agent)
        desired_capabilities = chrome_options.to_capabilities()
        if self.use_hub:
            driver = webdriver.Remote(
                command_executor=self.hub_url,
                desired_capabilities=desired_capabilities
            )
        else:
            driver = webdriver.Chrome(
                chrome_options=chrome_options
            )
        return driver

    def _init_firefox_driver(self):
        firefox_profile = webdriver.FirefoxProfile()
        if self.proxy:
            ip, port = self.proxy.split(':')
            firefox_profile.set_preference('network.proxy.type', 1)
            firefox_profile.set_preference('network.proxy.http', ip)
            firefox_profile.set_preference('network.proxy.http_port', port)
            firefox_profile.set_preference('network.proxy.ssl', ip)
            firefox_profile.set_preference('network.proxy.ssl_port', port)
        if self.user_agent:
            firefox_profile.set_preference(
                'general.useragent.override', self.user_agent)
        firefox_profile.update_preferences()
        desired_capabilities = DesiredCapabilities.FIREFOX
        if self.use_hub:
            driver = webdriver.Remote(
                command_executor=self.hub_url,
                desired_capabilities=desired_capabilities,
                browser_profile=firefox_profile
            )
        else:
            driver = webdriver.Firefox(
                firefox_profile=firefox_profile,
                capabilities=desired_capabilities
            )
        return driver

    def init_driver(self):
        if self.driver_type.upper() == 'CHROME':
            return self._init_chrome_driver()
        elif self.driver_type.upper() == 'FIREFOX':
            return self._init_firefox_driver()
        raise Exception('No supported driver: %s' % self.driver_type)

    def get_img(self, screenshot, xpath):
        """
        获取验证码图片

        :param screenshot: 页面截图
        :param xpath: 验证码图片xpath
        :return: img对象
        """
        self.device_pixel_ratio = self.driver.execute_script(
            "return window.devicePixelRatio;")
        element = self.driver.find_element_by_xpath(xpath)
        left = int(element.location['x']) * self.device_pixel_ratio
        top = int(element.location['y']) * self.device_pixel_ratio
        right = int(element.location['x'] +
                    element.size['width']) * self.device_pixel_ratio
        bottom = int(element.location['y'] +
                     element.size['height']) * self.device_pixel_ratio
        img = Image.open(screenshot)
        img = img.crop((left, top, right, bottom))
        return img

    def click_img(self, answer, height, identify_img_xpath1=None,
                  identify_button_xpath=None):
        """
        根据打码返回的坐标进行点击操作
        仅适用与点击型验证码

        :param answer: 打码返回结果
        :param height: 答案高度
        :param identify_img_xpath1: 题目xpath
        :param identify_button_xpath: 验证按钮
        :return:
        """
        actions = ActionChains(self.driver)
        img = self.driver.find_element_by_xpath(identify_img_xpath1)
        points = answer.split('|')
        for point in points:
            x, y = eval(point)
            actions.move_to_element_with_offset(
                img, x, y - int((height / self.device_pixel_ratio)))
            actions.click()
        actions.perform()
        time.sleep(2)
        if not identify_button_xpath:
            return
        self.driver.find_element_by_xpath(identify_button_xpath).click()

    def deal_normal_verification_code(
            self, captcha_obj, captcha_code, identify_img_xpath):
        uuid_str = str(uuid.uuid1())
        screenshot_path = './data/img/screenshot_%s.png' % uuid_str
        check_img_path = './data/img/check_image-%s.png' % uuid_str
        self.driver.save_screenshot(screenshot_path)
        img = self.get_img(screenshot_path, xpath=identify_img_xpath)
        img.save(check_img_path)
        answer = captcha_obj.decode(check_img_path, captcha_code)
        self.logger.info('get normal captcha code : %s' % answer)
        os.remove(screenshot_path)
        os.remove(check_img_path)
        return answer

    def deal_click_verification_code(
            self, captcha_obj, captcha_code,
            identify_img_xpath, identify_img_xpath1,
            identify_button_xpath):
        """
        处理点击型验证码

        :param captcha_obj:
        :param captcha_code:
        :param identify_img_xpath:
        :param identify_img_xpath1:
        :param identify_button_xpath:
        :return:
        """
        uuid_str = str(uuid.uuid1())
        screenshot_path = './data/img/screenshot_%s.png' % uuid_str
        check_img_path = './data/img/check_image-%s.png' % uuid_str
        self.driver.save_screenshot(screenshot_path)
        img1 = self.get_img(screenshot_path, xpath=identify_img_xpath)
        img2 = self.get_img(screenshot_path, xpath=identify_img_xpath1)
        to_image = Image.new('RGBA', (img2.width, img1.height + img2.height))
        to_image.paste(img1, (0, 0))
        to_image.paste(img2, (0, img1.height))
        if self.device_pixel_ratio > 1:
            to_image = to_image.resize(
                (int(to_image.width / self.device_pixel_ratio),
                 int(to_image.height / self.device_pixel_ratio))
            )
        to_image.save(check_img_path)
        answer = captcha_obj.decode(check_img_path, captcha_code)
        self.logger.info('get click captcha code : %s' % answer)
        self.click_img(answer, img1.height,
                       identify_img_xpath1=identify_img_xpath1,
                       identify_button_xpath=identify_button_xpath)
        os.remove(screenshot_path)
        os.remove(check_img_path)

    def get_mobile_code(self, phone_obj, phone, phone_token,
                        check_str='智联招聘', regexp='\d+',
                        retry_times=20, sleep_time=5):
        while retry_times > 0:
            msg = phone_obj.get_message(token=phone_token, phone=phone)
            if check_str in msg:
                code = re.findall(regexp, msg)[0]
                self.logger.info(
                    '{}: get mobile code success. code is: {}'.format(
                        phone, code))
                return code

            self.logger.info(
                '{}: no more message received. sleep {}s'.format(
                    phone, sleep_time))
            time.sleep(sleep_time)
            retry_times -= 1

    def is_element_visible(self, element):
        """
        判断元素是否存在
        :param element:
        :return:
        """
        driver = self.driver
        try:
            the_element = EC.visibility_of_element_located(element)
            assert the_element(driver)
            flag = True
        except AssertionError:
            self.logger.warning('the element is not visible.')
            flag = False
        except Exception as e:
            self.logger.exception(e)
            flag = False
        return flag

    def wait_element(self, by, by_value, timeout=5):
        try:
            WebDriverWait(
                self.driver, timeout).until(
                EC.presence_of_element_located((by, by_value)))
        except TimeoutException as e:
            self.logger.exception(e)

    @staticmethod
    def cookies2dict(cookies):
        """
        trans cookies
        :param cookies: driver.get_cookies()
        :return:
        """
        cookie_dict = {}
        for item in cookies:
            cookie_dict[item['name']] = item['value']
        return cookie_dict

    def release(self):
        try:
            self.driver.quit()
            self.driver.close()
        except:
            pass
