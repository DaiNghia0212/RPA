
from configparser import ConfigParser
from website import Website
import data
from pdfData import pdfFiles

parser = ConfigParser()
parser.read("config.ini")


# Define a main() function that calls the other functions in order:
# 'xpath: //*[@id="node-23"]/div/div/div/div/div/div/div/a'
def main():
    itdash_website = Website(url='https://itdashboard.gov/',
                             button='//*[@href="#home-dive-in"]',
                             agencies_info='id: agency-tiles-widget')
    try:
        print('FlAG')
        itdash_website.open()
        itdash_website.click(button='//*[@href="#home-dive-in"]')
        itdash_website.get_agencies_infomation()
        agency = itdash_website.agencies[int(parser.get("Link",
                                                        "agency_index"))]
        agencyWebsite = data.Agency(
            agency["link"], agency["name"],
            table_info='id: investments-table-object')
       
        agency_website = Website(url=agency["link"])
        agency_website.open()
        agency_website.wait(table='id: investments-table-object')
        agency_website.click(selector='name: investments-table-object_length')
        agency_website.click(all_seletor='''//*[@name="investments-table-object_length"]
                                             /option[4]''')

        agencyWebsite.open()
        agencyWebsite.wait_table()
        agencyWebsite.click_select_all()
        agencyWebsite.wait_table_load_all()
        data_table = agencyWebsite.get_table_info()
        pdf = pdfFiles(data_table)
        pdf.get_data()

    finally:
        print('Done')


if __name__ == "__main__":
    main()
