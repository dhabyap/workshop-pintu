#!/usr/bin/env python3
"""Convert guidebook-combined.md to PDF using weasyprint."""
import markdown
from weasyprint import HTML
import os

md_path = os.path.expanduser('~/Desktop/workshop-pintu/docs/guidebook-combined.md')
pdf_path = os.path.expanduser('~/Desktop/workshop-pintu/FROM-ZERO-TO-TRADING-BOTS-GuideBook.pdf')

with open(md_path, 'r', encoding='utf-8') as f:
    md = f.read()

html_content = markdown.markdown(md, extensions=['fenced_code', 'tables', 'codehilite'])

css_style = '''
body {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #222;
}
h1 {
    color: #1a3a5c;
    border-bottom: 3px solid #1a3a5c;
    padding-bottom: 8px;
    font-size: 22pt;
}
h2 {
    color: #1a3a5c;
    border-bottom: 1px solid #ccc;
    padding-bottom: 5px;
    font-size: 16pt;
    margin-top: 30px;
}
h3 {
    color: #2a5a8c;
    font-size: 13pt;
    margin-top: 20px;
}
code {
    background: #f0f4f8;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9.5pt;
}
pre {
    background: #f5f7fa;
    border: 1px solid #ddd;
    border-left: 4px solid #1a3a5c;
    padding: 12px;
    font-size: 9pt;
    line-height: 1.4;
    overflow-x: auto;
    font-family: 'Consolas', 'Courier New', monospace;
}
pre code {
    background: none;
    padding: 0;
    font-size: 9pt;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
    font-size: 10pt;
}
th {
    background: #1a3a5c;
    color: white;
    padding: 8px 12px;
    text-align: left;
}
td {
    border: 1px solid #ddd;
    padding: 6px 12px;
}
hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 20px 0;
}
blockquote {
    border-left: 4px solid #1a3a5c;
    background: #f0f4f8;
    margin: 10px 0;
    padding: 10px 15px;
}
'''

html_template = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{css_style}
</style>
</head>
<body>
{html_content}
</body>
</html>'''

HTML(string=html_template).write_pdf(pdf_path)
print(f'PDF created: {pdf_path}')
print(f'Size: {os.path.getsize(pdf_path)} bytes')
