
from configparser import ConfigParser
from website import Website
from excel import getData
from pdf import pdfData

parser = ConfigParser()
parser.read("config.ini")


def main():
    itdash_website = Website(url='https://itdashboard.gov/')
    try:
        itdash_website.open()
        itdash_website.click('//*[@href="#home-dive-in"]')
        itdash_website.get_agencies_infomation(
            agencies_info='id: agency-tiles-widget')
        agency = itdash_website.agencies[int(parser.get("Link",
                                                        "agency_index"))]
        agency_website = Website(url=agency["link"])
        agency_website.open()
        agency_website.wait('id: investments-table-object')
        agency_website.click('name: investments-table-object_length')
        agency_website.click('''//*[@name="investments-table-object_length"]
                                             /option[4]''')
        agency_website.wait_for_loading('id:investments-table-object_info')

        excel_files = getData(agency["name"])
        data = excel_files.get_table_info()
        pdf = pdfData(data)
        pdf.get_data()
    finally:
        print('Done')


if __name__ == "__main__":
    main()
