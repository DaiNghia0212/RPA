from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files

import time

browser_lib = Selenium()
excel_lib = Files()


def open_the_website(url):
    browser_lib.open_available_browser(url)
def click_dive_in(xpath):
    browser_lib.click_element_when_visible(xpath)

# def search_for(term):
#     input_field = "css:input"
#     browser_lib.input_text(input_field, term)
#     browser_lib.press_keys(input_field, "ENTER")


def store_screenshot(filename):
    browser_lib.screenshot(filename=filename)

# Define a main() function that calls the other functions in order:
def main():
    try:
        open_the_website("https://itdashboard.gov/")
        click_dive_in('xpath: //*[@id="node-23"]/div/div/div/div/div/div/div/a')
        # search_for("python")
        time.sleep(2)
        store_screenshot("output/screenshot.png")
        rows = browser_lib.find_element('id: agency-tiles-widget')
        items = rows.find_elements_by_class_name('noUnderline')
        links=[]
        for item in items:
            link = item.find_element_by_class_name('btn-sm').get_attribute('href')
            print(link)
            links.append(link)
        # while (count < number) and ():         
        #     link = browser_lib.get_element_attribute('xpath: //*[@id="agency-tiles-widget"]/div/div[1]/div[{}]/div/div/div/a'.format(count),'href')
        #     print(link)
        #     count += 1
        # excel_lib.create_workbook("output/test.xlsx")
        # excel_lib.save_workbook()
        # excel_lib.create_workbook("output/test.xlsx")
        # excel_lib.save_workbook()
    finally:
        browser_lib.close_all_browsers()

# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()
