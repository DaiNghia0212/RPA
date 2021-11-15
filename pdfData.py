from RPA.PDF import PDF

pdf = PDF()


class pdfFiles:
    def __init__(self, data_table):
        self.data_table = data_table

    def get_data(self):
        for data in self.data_table:
            print(data["UII"])
        for data in self.data_table:
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
            print()
            pdf.close_pdf(link_file)
