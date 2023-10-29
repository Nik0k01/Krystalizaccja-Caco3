import xlwings as xw

def eksport_danych(sol):
    book = xw.Book('template.xltx')
    sheet = book.sheets[0]
    sheet['B3'].options(transpose=True).value = sol.t
    sheet['C3'].options(transpose=True).value = sol.y[0]
    sheet['D3'].options(transpose=True).value = sol.y[1]
    sheet['E3'].options(transpose=True).value = sol.y[2]
    sheet['F3'].options(transpose=True).value = sol.y[3]
    sheet['G3'].options(transpose=True).value = sol.y[4]
    book.save('Tabele_pliki_txt/Nukleacja.xlsx')
    book.close()