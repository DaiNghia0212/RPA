from os import link
from re import A
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from configparser import ConfigParser
import time

parser = ConfigParser()
parser.read("config.ini")

browser_lib = Selenium()
excel_lib = Files()
agencies = []

def open_the_website(url):
    browser_lib.open_available_browser(url)

def click(locator):
    browser_lib.click_element_when_visible(locator)

def wait_for_content_load(locator):
    while browser_lib.is_element_visible(locator)==False:
        continue

def get_total_spending():
    container = browser_lib.find_element('id: agency-tiles-widget')
    items = container.find_elements_by_class_name('noUnderline')
    row_number = 1

    for item in items:
        link = item.find_element_by_class_name('btn-sm').get_attribute('href')
        name = item.find_element_by_class_name('w200').text
        money = item.find_element_by_class_name('w900').text
        agencies.append({"link": link, "name": name, "amounts": money})            
        excel_lib.set_cell_value(row_number,"A",money)           
        row_number += 1

def download_files(links):
    browser_lib.set_download_directory("output/", True)
    for link in links:
        open_the_website(link.get_attribute('href'))
        wait_for_content_load("id: business-case-pdf")
        click("id: business-case-pdf")
    if len(links) > 0:
        time.sleep(10)
        count = 1
        while count < len(links):
            browser_lib.close_browser()
            count += 1

def get_agency_infomation():
    row_number = 2
    links = []
    while browser_lib.get_element_attribute('id: investments-table-object_next','class').find('disabled') < 0:
        table = browser_lib.find_element('id: investments-table-object').find_element_by_tag_name('tbody')

        #get pdf links
        """ links = browser_lib.find_element('id: investments-table-object_wrapper').find_elements_by_tag_name('a')
        remove_links = browser_lib.find_element('id: investments-table-object_paginate').find_elements_by_tag_name('a')
        for link in remove_links:
            links.remove(link)
         """
        #get infomation in table
        rows = table.find_elements_by_tag_name('tr')
        for row in rows:
            values = row.find_elements_by_tag_name('td')
            column_number = 1
            for value in values:       
                excel_lib.set_cell_value(row_number, column_number, value.text)              
                if column_number == 1:
                    try:
                        links.append(value.get_attribute())
                    except:
                        pass
                column_number += 1
            row_number += 1
        #click next button
        oldState = browser_lib.find_element('id: investments-table-object_info').text
        click('id: investments-table-object_next')
        newState = browser_lib.find_element('id: investments-table-object_info').text
        while newState == oldState:
            newState = browser_lib.find_element('id: investments-table-object_info').text
        download_files(links)

diveIn_button = '//*[@id="node-23"]/div/div/div/div/div/div/div/a'
logo = 'id: agency-tiles-widget'
table = 'id: investments-table-object'

# Define a main() function that calls the other functions in order:
def main():
    try:
        
        open_the_website("https://itdashboard.gov/")
        wait_for_content_load(diveIn_button)
        click(diveIn_button)
        wait_for_content_load(logo)
        
        excel_lib.create_workbook("output/Agencies.xlsx")
        excel_lib.rename_worksheet("Sheet","Agencies") 
        get_total_spending()

        agency = agencies[int(parser.get("Link", "agency_index"))]
        open_the_website(agency["link"])
        wait_for_content_load(table)

        excel_lib.create_worksheet(agency["name"])
        get_agency_infomation()

    finally:
        excel_lib.save_workbook()
        browser_lib.close_all_browsers()

# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()