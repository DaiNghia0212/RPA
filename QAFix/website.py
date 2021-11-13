from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files


browser = Selenium()
excel = Files()


def wait_until_element_visible(locator):
    while not browser.is_element_visible(locator):
        continue


class Website:
    agencies = []

    def __init__(self, url, button, agencies_info):
        self.url = url
        self.button = button
        self.agencies_info = agencies_info

    def open(self):
        browser.open_available_browser(self.url)

    def click_dive_in_button(self):
        wait_until_element_visible(self.button)
        browser.click_element(self.button)

    def get_agencies_infomation(self):
        wait_until_element_visible(self.agencies_info)
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
