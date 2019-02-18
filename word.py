#!/usr/bin/env python
"""
	Generating a square wordcloud from the US constitution using default arguments.
"""

import os
import textract
import matplotlib.pyplot as plt

from os import path
from wordcloud import WordCloud

def post(payload):

	file_path = payload['file_path']
	max_words = int(payload['max_words'])
	max_font_size = int(payload['max_font_size'])

	d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
	print(d)
	# file_path = "../data/data.pdf" #filename of your PDF/directory where your PDF is stored
	text = textract.process(file_path)

	wordcloud = WordCloud().generate(str(text))

	wordcloud = WordCloud(max_font_size=max_font_size, max_words=max_words, background_color='white').generate(str(text))
	image = wordcloud.to_image()
	image.save('wordcloud.png')
	return {
		"json given" : payload,
		"File saved" : "wordcloud.png"
	}