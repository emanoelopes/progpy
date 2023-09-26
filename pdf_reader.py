#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from PyPDF2 import PdfReader
import codecs

filename = 'oficiio_8_2023_progep.pdf'
pdf = codecs.open(filename, "rb", encoding='utf-8')
for page in pdf:
    print page.encode('utf-8')

