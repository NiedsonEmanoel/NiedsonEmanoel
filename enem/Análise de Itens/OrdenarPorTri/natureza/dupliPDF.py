import sys
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter

input_file = 'gab.pdf'
output_file = 'gab_copy.pdf'

with open(input_file, 'rb') as infile:
    with open(output_file, 'wb') as outfile:
        reader = PdfReader(infile)
        writer = PdfWriter()
        
        for i in range(len(reader.pages)):
            page = reader.getPage(i)
            writer.addPage(page)
            
        writer.write(outfile)

def replace_text(old_text, new_text, input_file, output_file):
    with open(input_file, "rb") as f:
        input_pdf = PdfReader(f)
        output_pdf = PdfWriter()
        for page in range(len(input_pdf.pages)):
            page_obj = input_pdf.getPage(page)
            content = page_obj.extractText()
            content = content.replace(old_text, new_text)

            # criar um novo objeto PdfReader a partir do conteúdo extraído
            temp = BytesIO()
            temp.write(content.encode('utf-8'))
            temp.seek(0)
            temp_pdf = PdfReader(temp)

            # mesclar a página original com o novo conteúdo
            page_obj.mergePage(temp_pdf.getPage(0))
            output_pdf.addPage(page_obj)
        with open(output_file, "wb") as output:
            output_pdf.write(output)
        
replace_text("N", "n", 'gab_copy.pdf', '2o.pdf')
