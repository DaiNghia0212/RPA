from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from configparser import ConfigParser
import time

parser = ConfigParser()
parser.read("config.ini")

browser_lib = Selenium()
excel_file = Files()
departments = []

def open_browser(locator):
     browser_lib.open_available_browser(locator)
def click_element(locator):
    browser_lib.click_element_when_visible(locator)
def wait(locator):
    while browser_lib.is_element_visible(locator)==False:
        continue

diveIn = 'xpath: //*[@id="node-23"]/div/div/div/div/div/div/div/a'
info_agency = 'id: agency-tiles-widget'
table_info = 'id: investments-table-object'

# Define a main() function that calls the other functions in order:
def main():
    try:
         #open website and click the DIVE IN button
        browser_lib.set_download_directory("output/", True)
        open_browser("https://itdashboard.gov/")
        wait(diveIn)
        click_element(diveIn)
        wait(info_agency)
        #create an excel file 
        excel_file.create_workbook("output/Agency.xlsx")
        excel_file.rename_worksheet("Sheet","Agencies") 
        agency_tiles = browser_lib.find_element('id: agency-tiles-widget')
        items =  agency_tiles.find_elements_by_class_name('noUnderline')
        row_index = 1
        #get the amount of money and put it into the excel file 
        for item in items:
            link = item.find_element_by_class_name('btn-sm').get_attribute('href')
            title = item.find_element_by_class_name('w200').text
            total_money = item.find_element_by_class_name('w900').text
            departments.append({"link": link, "title": title, "total_money": total_money})            
            excel_file.set_cell_value(row_index,"A",total_money)           
            row_index += 1
        department = departments[int(parser.get("Link", "index"))]
        #open website of selected agency
        open_browser(department["link"])
        wait(table_info)
        #create another excel file
        excel_file.create_worksheet(department["title"])
       
        initialInfo = browser_lib.find_element('id: investments-table-object_info').text
        
        click_element('name: investments-table-object_length')
        click_element('//*[@id="investments-table-object_length"]/label/select/option[4]')
        
        finalInfo = browser_lib.find_element('id: investments-table-object_info').text
        while initialInfo == finalInfo:
            initialInfo = browser_lib.find_element('id: investments-table-object_info').text
        table = browser_lib.find_element('id: investments-table-object').find_element_by_tag_name('tbody')
        links = table.find_elements_by_tag_name('a')
        #dowload PDF files
        for link in links:
            open_browser(link.get_attribute('href'))
            wait("id: business-case-pdf")
            click_element("id: business-case-pdf")
        time.sleep(10)
        rows = table.find_elements_by_tag_name('tr')     
        row_index = 2
        #get data from the table
        for row in rows:
            values = row.find_elements_by_tag_name('td')
            column_index = 1
            for value in values:       
                excel_file.set_cell_value(row_index, column_index, value.text)   
                column_index += 1
            row_index += 1

    finally:
        excel_file.save_workbook()
        browser_lib.close_all_browsers()

# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()