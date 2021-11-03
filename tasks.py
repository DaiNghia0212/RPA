from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
import random

import time

browser_lib = Selenium()
excel_lib = Files()

def open_the_website(url):
    browser_lib.open_available_browser(url)
def click_dive_in(xpath):
    browser_lib.click_element_when_visible(xpath)
def store_screenshot(filename):
    browser_lib.screenshot(filename=filename)

# Define a main() function that calls the other functions in order:
def main():
    try:
        open_the_website("https://itdashboard.gov/")
        click_dive_in('xpath: //*[@id="node-23"]/div/div/div/div/div/div/div/a')

        while browser_lib.is_element_visible('id: agency-tiles-widget')==False:
            continue
        

        container = browser_lib.find_element('id: agency-tiles-widget')

        items = container.find_elements_by_class_name('noUnderline')
        agencies = []
        row_number = 1
        excel_lib.create_workbook("output/Agencies.xlsx")
        excel_lib.rename_worksheet("Sheet","Agencies")

        for item in items:
            link = item.find_element_by_class_name('btn-sm').get_attribute('href')
            name = item.find_element_by_class_name('w200').text
            amounts = item.find_element_by_class_name('w900').text
            agencies.append({"link": link, "name": name, "amounts": amounts})
            excel_lib.set_cell_value(row_number,"A",amounts)           
            row_number += 1

        browser_lib.close_browser()
        agency = random.choice(agencies)
        open_the_website(agency["link"])
        excel_lib.create_worksheet(agency["name"])
        
        while browser_lib.is_element_visible('id: investments-table-object')==False:
            continue

     
        oldInfo = browser_lib.find_element('id:investments-table-object_info').text
        click_dive_in('name:investments-table-object_length')
        while browser_lib.is_element_visible('//*[@id="investments-table-object_length"]/label/select/option[1]')==False:
              continue
        store_screenshot('output/screenshot.png')
        click_dive_in('//*[@id="investments-table-object_length"]/label/select/option[4]')
        time.sleep(3)
        store_screenshot('output/screensho.png')
        newInfo = browser_lib.find_element('id:investments-table-object_info').text
        count = 0
        while newInfo == oldInfo:
             newInfo = browser_lib.find_element('id:investments-table-object_info').text
        print(newInfo)
        table = browser_lib.find_element('id: investments-table-object').find_element_by_tag_name('tbody')
        rows = table.find_elements_by_tag_name('tr')
        
        row_number = 2

        for row in rows:
            values = row.find_elements_by_tag_name('td')
            column_number = 1
            for value in values:       
                excel_lib.set_cell_value(row_number, column_number, value.text)
                column_number += 1
            row_number += 1
      
    finally:
        excel_lib.save_workbook()
        excel_lib.open_workbook("output/Agencies.xlsx")
        browser_lib.close_all_browsers()

# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()