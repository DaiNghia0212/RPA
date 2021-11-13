
from configparser import ConfigParser
from website import Website
import data

parser = ConfigParser()
parser.read("config.ini")


# Define a main() function that calls the other functions in order:
# 'xpath: //*[@id="node-23"]/div/div/div/div/div/div/div/a'
def main():
    itdash = Website(url='https://itdashboard.gov/',
                     button='//*[@href="#home-dive-in"]',
                     agencies_info='id: agency-tiles-widget')
    try:
        print('FlAG')
        itdash.open()
        itdash.click_dive_in_button()
        itdash.get_agencies_infomation()
        agency = itdash.agencies[int(parser.get("Link", "agency_index"))]
        agencyWebsite = data.Agency(
            agency["link"], agency["name"], 
            table_info='id: investments-table-object')

        agencyWebsite.open()
        agencyWebsite.wait_table()
        agencyWebsite.click_select_all()
        agencyWebsite.wait_table_load_all()
        agencyWebsite.get_table_info()
    finally:
        print('Done')


if __name__ == "__main__":
    main()
