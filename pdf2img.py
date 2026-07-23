import fitz
import os

pdf_path = os.path.expanduser('~/Downloads/Telegram Desktop/From Zero to Trading Bots.pdf')
doc = fitz.open(pdf_path)

for i in range(min(4, len(doc))):
    page = doc[i]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img_path = os.path.expanduser(f'~/Desktop/workshop-pintu/template_page{i}.png')
    pix.save(img_path)
    print(f'Saved page {i}: {img_path} {pix.width}x{pix.height}')

doc.close()
