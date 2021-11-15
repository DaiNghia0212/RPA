from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files


browser = Selenium()
excel = Files()


class Website:
    agencies = []

    def __init__(self, url):
        self.url = url

    def open(self):
        browser.open_available_browser(self.url)

    def wait(locator):
        while not browser.is_element_visible(locator):
            continue

    def click(self, locator):
        self.wait(locator)
        browser.click_element(locator)
    
    def wait_table_load_all(self):
        old_info = browser.find_element(
            'id: investments-table-object_info').text
        new_info = browser.find_element(
            'id: investments-table-object_info').text
        while new_info == old_info:
            new_info = browser.find_element(
                'id: investments-table-object_info').text

    def get_agencies_infomation(self):
        self.wait_until_element_visible(self.agencies_info)
        container = browser.find_element(self.agencies_info)
        items = container.find_elements_by_class_name('noUnderline')
        row_number = 1
        excel.create_workbook("output/Agencies.xlsx")
        excel.rename_worksheet("Sheet", "Agencies")
        for item in items:
            link = item.find_element_by_class_name(
                'btn-sm').get_attribute('href')
            name = item.find_element_by_class_name('w200').text
            amounts = item.find_element_by_class_name('w900').text
            self.agencies.append(
                {"link": link, "name": name, "amounts": amounts})
            excel.set_cell_value(row_number, "A", amounts)
            row_number += 1
        excel.save_workbook()
