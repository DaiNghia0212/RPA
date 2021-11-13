from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files


browser = Selenium()
excel = Files()


def wait_until_element_visible(locator):
    while not browser.is_element_visible(locator):
        continue


class Agency:
    oldInfo = ''
    summaryData = []
    def __init__(self, url, name, table_info):
        self.url = url
        self.name = name
        self.table_info = table_info

    def open(self):
        browser.open_available_browser(self.url)

    def wait_table(self):
        wait_until_element_visible(self.table_info)

    def click_select_all(self):
        self.oldInfo = browser.find_element(
            'id: investments-table-object_info').text
        browser.click_element('name: investments-table-object_length')
        browser.click_element(
            '//*[@name="investments-table-object_length"]/option[4]')

    def wait_table_load_all(self):
        newInfo = browser.find_element(
            'id: investments-table-object_info').text
        while newInfo == self.oldInfo:
            newInfo = browser.find_element(
                'id: investments-table-object_info').text

    def get_table_info(self):
        browser.set_download_directory("./output", True)
        excel.open_workbook('output/Agencies.xlsx')
        table = browser.find_element(
            'id: investments-table-object').find_element_by_tag_name('tbody')
        links = table.find_elements_by_tag_name('a')
        for link in links:
            browser.open_available_browser(link.get_attribute('href'))
            wait_until_element_visible("id: business-case-pdf")
            browser.click_element("id: business-case-pdf")
        while browser.is_element_attribute_equal_to(
            '//*[@id="business-case-pdf"]/a',
            'aria-busy',
                'true'):
            continue
        print(table)
        rows = table.find_elements_by_tag_name('tr')
        row_number = 2
        excel.create_worksheet(self.name)
        for row in rows:
            values = row.find_elements_by_tag_name('td')
            column_number = 1
            count = 0
            for index,value in enumerate(values):
                if (index == 0):
                   dataUI = value.text
                elif index == 2:
                   investTitle = value.text
                excel.set_cell_value(row_number, column_number, value.text)
                column_number += 1
            self.summaryData.append({"UI":dataUI,"nameInvest":investTitle})
            row_number += 1
        print(self.summaryData);
        excel.save_workbook()
        browser.close_all_browsers()
