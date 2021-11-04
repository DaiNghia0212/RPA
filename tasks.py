from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from configparser import ConfigParser
import random, time

parser = ConfigParser()
parser.read("config.ini")

browser = Selenium()
excel = Files()
agencies = []

def open_the_website(url):
    browser.open_available_browser(url)

def click(locator):
    browser.click_element_when_visible(locator)

# def store_screenshot(filename):
#     browser_lib.screenshot(filename=filename)

def wait_until_infomation_visible(locator):
    while browser.is_element_visible(locator)==False:
        continue

def get_agencies_infomation():
    container = browser.find_element('id: agency-tiles-widget')
    items = container.find_elements_by_class_name('noUnderline')
    row_number = 1

    for item in items:
        link = item.find_element_by_class_name('btn-sm').get_attribute('href')
        name = item.find_element_by_class_name('w200').text
        amounts = item.find_element_by_class_name('w900').text
        agencies.append({"link": link, "name": name, "amounts": amounts})            
        excel.set_cell_value(row_number,"A",amounts)           
        row_number += 1

def get_table_infomation():
    oldInfo = browser.find_element('id: investments-table-object_info').text
    click('name: investments-table-object_length')
    #wait_until_infomation_visible('//*[@id="investments-table-object_length"]/label/select/option[1]')
    click('//*[@id="investments-table-object_length"]/label/select/option[4]')
    newInfo = browser.find_element('id: investments-table-object_info').text
    while newInfo == oldInfo:
        newInfo = browser.find_element('id: investments-table-object_info').text
    table = browser.find_element('id: investments-table-object').find_element_by_tag_name('tbody')
    links = table.find_elements_by_tag_name('a')

    for link in links:
        open_the_website(link.get_attribute('href'))
        wait_until_infomation_visible("id: business-case-pdf")
        click("id: business-case-pdf")
    time.sleep(10)
    print(table)
    rows = table.find_elements_by_tag_name('tr')     
    row_number = 2

    for row in rows:
        values = row.find_elements_by_tag_name('td')
        column_number = 1
        for value in values:       
            excel.set_cell_value(row_number, column_number, value.text)   
            column_number += 1
        row_number += 1

dive_in_button = 'xpath: //*[@id="node-23"]/div/div/div/div/div/div/div/a'
agencies_info = 'id: agency-tiles-widget'
table_info = 'id: investments-table-object'

# Define a main() function that calls the other functions in order:
def main():
    try:
        browser.set_download_directory("output/", True)
        open_the_website("https://itdashboard.gov/")
        wait_until_infomation_visible(dive_in_button)
        click(dive_in_button)
        wait_until_infomation_visible(agencies_info)
        

        excel.create_workbook("output/Agencies.xlsx")
        excel.rename_worksheet("Sheet","Agencies") 
        get_agencies_infomation()

       # agency = random.choice(agencies)
        print(type(parser.get("Link", "agency_index")))
        agency = agencies[int(parser.get("Link", "agency_index"))]
       
        open_the_website(agency["link"])
        wait_until_infomation_visible(table_info)

        excel.create_worksheet(agency["name"])
        get_table_infomation()

    finally:
        excel.save_workbook()
        browser.close_all_browsers()

# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()