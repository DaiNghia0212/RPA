from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.PDF import PDF

pdf = PDF()
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
        anchors = table.find_elements_by_tag_name('a')
        links = ""
        for anchor in anchors:
            links = links + " " + anchor.get_attribute('href')
            browser.open_available_browser(anchor.get_attribute('href'))
            wait_until_element_visible("id: business-case-pdf")
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

        for data in self.summaryData:
            print(data["UII"])
        for data in self.summaryData:
            link_file = './output/' + data["UII"] + '.pdf'
            text = pdf.get_text_from_pdf(link_file, '1')[1]
        # get name of this investment
            start = text.find('Name of this Investment') + 25
            end = text.find('Unique Investment Identifier') - 3
            investment_name = text[start:end]
        # get unique investment identifier
            start = end + 39
            end = text.find('Section B')
            uii = text[start:end]
            print(data["investment_title"])
            print('''Compare the value "Name of this Investment" with
the column "Investment Title": ''')
            if data["investment_title"] == investment_name:
                print(True)
            else:
                print(False)
            print('''Compare the value "Unique Investment Identifier (UII)"
with the column "UII": ''')
            if data["UII"] == uii:
                print(True)
            else:
                print(False)
            pdf.close_pdf(link_file)

        excel.save_workbook()
        browser.close_all_browsers()
