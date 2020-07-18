import os
import openpyxl

for archivo in os.listdir('.'):
    if archivo.endswith("xlsx"):
        wb = openpyxl.load_workbook(archivo, data_only=True)
        main = wb.sheetnames[0]
        sheet = wb[main]
        print(sheet["C2"].value)