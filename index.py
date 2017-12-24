# coding: UTF-8

import requests
from bs4 import BeautifulSoup

def lambda_handler(event, context):
	url = "https://www.tokyu-hands.co.jp/list/"
	html = requests.get(url)
	soup = BeautifulSoup(html, "html.parser")
	print("soup:" + str(soup))





	return





