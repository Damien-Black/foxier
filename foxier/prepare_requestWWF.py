import simplejson
import re
import base64
import time
from hashlib import sha256  # Verification of Outh response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import *
from selenium.common.exceptions import TimeoutException
import logging
# import hmac

SIGNED_REQUEST_REGEX = r'[^.]+\\.([^\"]+)'


def accessFactory(username, password):
    # Validation username is an email
    pattern = r'[^@]+@[^@]+\.[^@]+'
    match = re.search(pattern, username)
    if not match:
        raise InvalidEmailException('Invalid Email address')
    # TODO validate password

    class AccessTokenRetriever(object):
        """Go to WWF app and get Access token the app uses.  Store in Class"""
        def __init__(self, useremail, pw):
            self.useremail = useremail
            self.pw = pw
            self.AccTokenJSON = dict()  # AccessToken prop to be used(it will expire)
            self.driver = webdriver.Firefox()

        def setTokenWWF(self):
            if not self.loginFB():
                raise('login failed, check username and password')
            else:
                self.driver.get('https://apps.facebook.com/wordswithfriends/')
                codedToken = self.find_by_xpath(self.driver, '//input[@name = "signed_request"]').get_attribute('value')
                with open('temp.txt', 'w') as f:
                    f.write(codedToken)
                dataJSON = self.parseToken(codedToken)
                self.AccTokenJSON = dataJSON

        def getAccessToken(self):  # Untested
            """Gets access token.  Return a new one if current one is expired"""
            if not self.AccTokenJSON.get('oauth_token'):
                self.setTokenWWF()
                return self.AccTokenJSON.get('oauth_token')
            elif self.AccTokenJSON.get('expires') <= int(time.time()):
                logging.info('Outh expired getting a new one')
                self.setTokenWWF()
                return self.AccTokenJSON.get('oauth_token')
            else:
                logging.debug(
                    'OuthExpires: %s Current time: %s', self.AccTokenJSON.get(
                        'expires'), time.time())
                return self.AccTokenJSON.get('oauth_token')

        # Helpers #
        def loginFB(self):  # HTML-GET request to FB page (form=input tag HTML)
            self.driver.get('https://www.facebook.com/')
            self.find_by_xpath(
                self.driver, '//input[@name = "email"]').send_keys(
                self.useremail)
            self.find_by_xpath(
                self.driver, '//input[@name = "pass"]').send_keys(
                self.pw)
            self.find_by_xpath(
                self.driver, '//input[@value = "Log In"]').click()
            # TODO confirm login, this current impl below seems poor
            try:
                self.find_by_xpath(self.driver, '//input[@name = "pass"]')
            except TimeoutException:
                return True
            return False

        def parseToken(self, tokenCoded):
                resultCoded = tokenCoded.split('.', 2)
                encoded_sig = resultCoded[0]
                payload = resultCoded[1]
                sig = self.base64_url_decode(encoded_sig)  # Any need for this?
                data = simplejson.loads(self.base64_url_decode(payload))
                if data.get('algorithm').upper() != 'HMAC-SHA256':
                    log.error('Unknown algorithm')
                    return None
                else:
                    return data

        def base64_url_decode(self, inp):
            padding_factor = (4 - len(inp) % 4) % 4
            inp += "="*padding_factor
            return base64.b64decode(inp.translate(dict(zip(map(ord, u'-_'), u'+/'))))

        def find_by_xpath(self, driver, locator):
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, locator)))
            return element

    return AccessTokenRetriever(username, password)


class InvalidEmailException(Exception):
    pass
