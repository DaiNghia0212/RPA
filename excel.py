from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files

browser = Selenium()
excel = Files()

class getData:
    summaryData = []
    def __init__(self, table_info):
        self.table_info = table_info

    def wait(locator):
        while not browser.is_element_visible(locator):
              continue
    def get_table_info(self):
        browser.set_download_directory("./output", True)
        excel.open_workbook('output/Agencies.xlsx')
        table = browser.find_element(
            'id: investments-table-object').find_element_by_tag_name('tbody')
        anchors = table.find_elements_by_tag_name('a')
        links = ""
        for anchor in anchors:
            links = links + " " + anchor.get_attribute('href')
            browser.open_available_browser(anchor.get_attribute('href'))
            self.wait("id: business-case-pdf")
            browser.click_element("id: business-case-pdf")
        while browser.is_element_attribute_equal_to(
            '//*[@id="business-case-pdf"]/a',
            'aria-busy',
                'true'):
            continue

        rows = table.find_elements_by_tag_name('tr')
        row_number = 2
        excel.create_worksheet(self.name)

        for row in rows:
            values = row.find_elements_by_tag_name('td')
            column_number = 1
            if links.find(values[0].text) >= 0:
                UIIvalue = values[0].text
                investment_title = values[2].text
                self.summaryData.append(
                 {"UII": UIIvalue, "investment_title": investment_title})
            for value in values:
                excel.set_cell_value(row_number, column_number, value.text)
                column_number += 1
            row_number += 1
        excel.save_workbook()
        browser.close_all_browsers()
        return self.summaryData
