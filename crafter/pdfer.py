import json
from fpdf import FPDF

pdf = FPDF('P', 'mm', 'A4')
w = 210
h = 297

# First Page
pdf.add_page()
pdf.set_font('helvetica', 'B', 30)

pdf.set_xy(((w/2)-(70/2)), 100)
pdf.cell(70, 20, 'MiaBudget', border=1, align='C')

pdf.set_xy(((w/2)-(70/2)), 125)
pdf.set_font('helvetica', 'I', 15)
pdf.cell(70, 12, 'Created by GreenLz', border=0, align='C')

# Second Page
pdf.add_page()
pdf.set_xy(((w/2)-(70/2)), 15)
pdf.set_font('helvetica', 'B', 20)
pdf.cell(70, 15, 'Disclaimer', border=1, align='C')

pdf.set_xy(25, 60)
pdf.set_font('helvetica', '', 15)
pdf.multi_cell(w-50, 7, R"This budget app is a personal project designed to convert bank statements into easy-to-understand budget reports with graphs. While every effort has been made to ensure the accuracy of the generated PDF file, errors may occur in the processing of data. The viewer is advised to double-check the budget details and confirm the accuracy of the information presented. The app creator is not responsible for any financial errors or discrepancies resulting from the use of this tool.", border=1, align='J')

pdf.set_xy(10, 275)
pdf.set_font('helvetica', '', 12)
pdf.cell(0, 1, str('1'), border=0, align='C')

pdf.output('Budget.pdf')