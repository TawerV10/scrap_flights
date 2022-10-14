import csv
from time import sleep
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By

PAX = [
        {'ADULT': {'NO': 1, 'DOB': '01/01/1997'},  'CHILD': {'NO': 0, 'DOB': '0'}},
        {'ADULT': {'NO': 2, 'DOB': '01/01/1997'},  'CHILD': {'NO': 0, 'DOB': '0'}},
        {'ADULT': {'NO': 2, 'DOB': '01/01/1997'},  'CHILD': {'NO': 1, 'DOB': '01/01/2011'}}
        ]

WEBSITE_AGE_LIMIT = 17
START_DATE = "20221101"
TRIP_DAYS = 30
ORIGIN = "DXB"
DESTINATION = ["IST", "JNB"]

def main():
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'

        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        url_template = "https://flights2.flydubai.com/en/results/rt/{}/{}_{}/{}_{}?cabinClass=Economy&isOriginMetro=true&isDestMetro=true&pm=cash"

        for dest in DESTINATION:

            filename = 'fly_to_' + dest.lower().replace(' ', '_') + '.csv'
            with open(filename, 'w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    'Start Date', 'End Date', 'Duration', 'Fly From', 'Fly To', 'No Of People', 'All Price', 'Insurance Price'
                ])

            for day in range(1, TRIP_DAYS + 1):
                for px in PAX:
                    try:
                        sd = START_DATE
                        fd = datetime.strftime(datetime.strptime(START_DATE, "%Y%m%d") + timedelta(days=day), "%Y%m%d")

                        count = ''
                        if px['ADULT']['NO'] == 1:
                            count = 'a1'

                        if px['ADULT']['NO'] == 2:
                            count = 'a2'

                        if px['CHILD']['NO'] == 1:
                            count = count+'c1'

                        url = url_template.format(count, ORIGIN, dest, sd, fd)
                        print(url)
                        driver.get(url)

                        driver.find_element(By.XPATH, '/html/body/fz-root/div[1]/div[1]/fz-availability/fz-desktop-availability/div/div[2]/div[1]/div[1]/fz-desktop-availability-list/div/div/div/div[1]/fz-desktop-flight-availability-list-item/div/div/div/div').click()
                        sleep(3)
                        driver.find_element(By.XPATH, '/html/body/fz-root/div[1]/div[1]/fz-availability/fz-desktop-availability/div/div[2]/div[1]/div[1]/fz-desktop-availability-list/div/div/div/div[1]/div[1]/div/div/div/div[3]/div[1]/div/fz-fare-brand-column/div/div[31]/fz-button/div/button').click()
                        sleep(3)
                        driver.find_element(By.XPATH, '/html/body/fz-root/div[1]/div[1]/fz-availability/fz-desktop-availability/div/div/div[1]/div[2]/div/div[1]/fz-desktop-availability-list/div/div/div/div[1]/fz-desktop-flight-availability-list-item/div/div/div/div').click()
                        sleep(3)
                        driver.find_element(By.XPATH, '/html/body/fz-root/div[1]/div[1]/fz-availability/fz-desktop-availability/div/div/div[1]/div[2]/div/div[1]/fz-desktop-availability-list/div/div/div/div[1]/div[1]/div/div/div/div[3]/div[1]/div/fz-fare-brand-column/div/div[30]/fz-button/div/button').click()
                        sleep(3)

                        driver.find_element(By.ID, 'lblBtnrouteMsgNoticeAgree').click()
                        sleep(3)
                        driver.find_element(By.ID, 'lblBtnrouteMsgNoticeAgree').click()
                        sleep(3)

                        cur = driver.find_element(By.XPATH,'/html/body/fz-root/div[1]/div[2]/fz-trip-summary-desktop/mat-card/mat-card-content/div[1]/div[2]/div[4]/div[2]/fz-currency-amount/div/fz-static-label[1]/label').get_attribute("innerText")
                        price = driver.find_element(By.XPATH,'/html/body/fz-root/div[1]/div[2]/fz-trip-summary-desktop/mat-card/mat-card-content/div[1]/div[2]/div[4]/div[2]/fz-currency-amount/div/fz-static-label[2]/label').get_attribute("innerText")
                        ins_cur = driver.find_element(By.XPATH,'/html/body/fz-root/div[1]/div[1]/fz-optional-extras/fz-optional-extras-page/div/div[2]/div/div/div/div/div[3]/div[4]/div/fz-insurance-desktop/div/div[2]/div[2]/fz-currency-amount/div/fz-static-label[1]/label').get_attribute("innerText")
                        ins_price = driver.find_element(By.XPATH,'/html/body/fz-root/div[1]/div[1]/fz-optional-extras/fz-optional-extras-page/div/div[2]/div/div/div/div/div[3]/div[4]/div/fz-insurance-desktop/div/div[2]/div[2]/fz-currency-amount/div/fz-static-label[2]/label').get_attribute("innerText")

                        print(cur + " " + price)
                        print(ins_cur + " " + ins_price)

                        priceAll = price + ' ' + cur
                        insprireAll = ins_price + ' ' + ins_cur

                        with open(filename, 'a', newline='', encoding="utf-8") as file:
                            writer = csv.writer(file)
                            writer.writerow([sd, fd, day,  ORIGIN, dest, str(px['ADULT']['NO']) + '+' + str(px['CHILD']['NO']), priceAll, insprireAll])


                    except Exception as ex:
                        print(ex)

    except Exception as ex:
        print(ex)
    finally:
        driver.stop_client()
        driver.close()
        driver.quit()

if __name__ == '__main__':
    main()
