#!/usr/bin/env python3
"""Generate GuideBook PDF using fpdf2."""
import re, os
from fpdf import FPDF

md_path = os.path.expanduser('~/Desktop/workshop-pintu/docs/guidebook-combined.md')
pdf_path = os.path.expanduser('~/Desktop/workshop-pintu/FROM-ZERO-TO-TRADING-BOTS-GuideBook.pdf')

with open(md_path, 'r', encoding='utf-8') as f:
    raw = f.read()

replacements = {
    '\u2014': '--', '\u2013': '-', '\u2018': "'", '\u2019': "'",
    '\u201c': '"', '\u201d': '"', '\u2026': '...',
    '\u2600': '*', '\u2601': '*', '\u2602': '*', '\u2603': '*',
}
for k, v in replacements.items():
    raw = raw.replace(k, v)

# Strip all emoji and non-latin-1 characters
raw = re.sub(r'[\U0001F000-\U0001FFFF]', '', raw)
raw = re.sub(r'[\u2000-\u206F]', '', raw)
raw = re.sub(r'[\u2100-\u27BF]', '', raw)
raw = re.sub(r'[\uFE00-\uFE0F]', '', raw)
raw = re.sub(r'[\u200D]', '', raw)
raw = re.sub(r'[\u2934-\u2935]', '', raw)
raw = re.sub(r'[\u2B05-\u2B55]', '', raw)

# Force latin-1 safe
raw = raw.encode('latin-1', errors='replace').decode('latin-1')

lines = raw.split('\n')


class GuideBookPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.code_bg = (245, 247, 250)
        self.code_border = (26, 58, 92)
        self.header_color = (26, 58, 92)

    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 7)
            self.set_text_color(150, 150, 150)
            self.cell(0, 8, 'FROM ZERO TO TRADING BOTS - GuideBook', align='R')
            self.ln(4)
            self.set_draw_color(200, 200, 200)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def cover_page(self):
        self.add_page()
        self.set_draw_color(26, 58, 92)
        self.rect(10, 10, 190, 277, 'D')
        self.ln(50)
        self.set_font('Helvetica', 'B', 28)
        self.set_text_color(26, 58, 92)
        self.cell(0, 15, 'FROM ZERO', align='C')
        self.ln(16)
        self.cell(0, 15, 'TO TRADING BOTS', align='C')
        self.ln(25)
        self.set_font('Helvetica', '', 14)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, 'Workshop PINTU x Web3 Dev Bandung', align='C')
        self.ln(10)
        self.cell(0, 10, '25 Juli 2026 - Parla Cafe, Bandung', align='C')
        self.ln(20)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, 'Ga perlu jadi programmer. Cukup prompt, download, cron, jalan.', align='C')
        self.ln(40)
        self.set_font('Helvetica', '', 10)
        self.cell(0, 8, 'Instructor: Putra', align='C')

    def section_title(self, title):
        self.ln(6)
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(*self.header_color)
        self.set_draw_color(*self.header_color)
        self.set_line_width(0.8)
        self.cell(0, 10, title)
        self.ln(11)
        self.line(10, self.get_y() - 2, 200, self.get_y() - 2)
        self.ln(4)

    def sub_title(self, title):
        self.ln(4)
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(42, 90, 140)
        self.cell(0, 8, title)
        self.ln(10)

    def sub_sub_title(self, title):
        self.ln(3)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 7, title)
        self.ln(8)

    def body_text(self, text):
        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(40, 40, 40)
        # Ensure we have room — reset x if needed
        if self.get_x() < 10 or self.get_x() > 100:
            self.set_x(15)
        self.multi_cell(175, 5.2, text)
        self.ln(2)

    def code_block(self, code):
        self.ln(2)
        x = self.get_x()
        y = self.get_y()
        lines_code = code.split('\n')
        line_h = 4.5
        h = len(lines_code) * line_h + 6
        self.set_fill_color(*self.code_bg)
        self.set_draw_color(*self.code_border)
        self.rect(x + 5, y, 180, h, 'DF')
        self.set_fill_color(*self.code_border)
        self.rect(x + 5, y, 3, h, 'F')
        self.set_xy(x + 11, y + 3)
        self.set_font('Courier', '', 7)
        self.set_text_color(30, 30, 30)
        for cline in lines_code:
            self.cell(0, line_h, cline.replace('\t', '    '))
            self.ln(line_h)
        self.set_xy(x, y + h + 2)
        self.ln(3)

    def bullet(self, text, indent=15):
        self.set_x(indent)
        self.set_font('Helvetica', '', 9.5)
        self.set_text_color(40, 40, 40)
        self.multi_cell(175, 5.5, text)

    def bullet_check(self, text, indent=15, checked=True):
        self.set_x(indent)
        self.set_font('Helvetica', '', 9.5)
        mark = '[X]' if checked else '[ ]'
        self.set_text_color(40, 40, 40)
        self.cell(10, 5.5, mark)
        self.multi_cell(165, 5.5, text)

    def note_box(self, text):
        self.ln(2)
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(60, 60, 60)
        self.set_fill_color(240, 244, 248)
        self.set_x(10)
        self.multi_cell(180, 5.5, text)
        self.ln(2)


# ---- Build PDF ----
pdf = GuideBookPDF()
pdf.alias_nb_pages()
pdf.cover_page()

i = 0
in_code = False
code_buffer = []

while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # Code blocks
    if stripped.startswith('```'):
        if in_code:
            pdf.code_block('\n'.join(code_buffer))
            code_buffer = []
            in_code = False
        else:
            in_code = True
        i += 1
        continue

    if in_code:
        code_buffer.append(line)
        i += 1
        continue

    # Skip
    if stripped == '' or stripped == '---' or stripped.startswith('1. [') or stripped.startswith('2. [') or stripped.startswith('3. [') or stripped.startswith('4. [') or stripped.startswith('5. [') or stripped.startswith('6. [') or stripped.startswith('7. ['):
        i += 1
        continue

    if 'Daftar Isi' in stripped:
        i += 1
        continue

    # Main title
    if stripped.startswith('# FROM ZERO'):
        i += 1
        continue

    # h1
    if stripped.startswith('# '):
        txt = stripped[2:]
        if 'Daftar' not in txt:
            pdf.section_title(txt)
        i += 1
        continue

    # h2
    if stripped.startswith('## '):
        txt = stripped[3:]
        if not any(x in txt for x in ['Daftar', 'Persiapan', 'Panduan', 'Trading', 'Cheatsheet', 'Cron', 'Troubleshooting', 'Bonus', 'Alur', 'Tips', 'Resources']):
            pdf.sub_title(txt)
        i += 1
        continue

    # h3
    if stripped.startswith('### '):
        pdf.sub_sub_title(stripped[4:])
        i += 1
        continue

    # Checklist
    if stripped.startswith('- [') and '] ' in stripped:
        checked = '[X]' in stripped
        txt = stripped.split('] ', 1)[1] if '] ' in stripped else ''
        pdf.bullet_check(txt, checked=checked)
        i += 1
        continue

    # Bullets
    if stripped.startswith('- ') or stripped.startswith('* '):
        txt = re.sub(r'^[\s]*[-*]\s+', '', stripped)
        txt = re.sub(r'\*\*(.*?)\*\*', r'\1', txt)
        pdf.bullet(txt)
        i += 1
        continue

    # Numbered
    if re.match(r'^\s*\d+\.\s', stripped):
        txt = re.sub(r'^\s*\d+\.\s+', '', stripped)
        txt = re.sub(r'\*\*(.*?)\*\*', r'\1', txt)
        pdf.bullet(txt)
        i += 1
        continue

    # Blockquote
    if stripped.startswith('> ') or stripped.startswith('>'):
        txt = stripped.lstrip('> ')
        while i + 1 < len(lines) and (lines[i + 1].strip().startswith('> ') or lines[i + 1].strip().startswith('>')):
            i += 1
            txt += '\n' + lines[i].strip().lstrip('> ')
        pdf.note_box(txt)
        i += 1
        continue

    # Body text
    txt = stripped
    txt = re.sub(r'\*\*(.*?)\*\*', r'\1', txt)
    if txt:
        pdf.body_text(txt)
    i += 1

pdf.output(pdf_path)
print(f'PDF saved: {pdf_path}')
print(f'Size: {os.path.getsize(pdf_path)} bytes')
print(f'Pages: {pdf.page_no()}')
