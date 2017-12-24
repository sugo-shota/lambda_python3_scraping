# coding: UTF-8

import requests
from bs4 import BeautifulSoup

def lambda_handler(event, context):

	#please replace "your_alexa_app_id"
	if (event['session']['application']['applicationId'] != "your_alexa_app_id"):
		raise ValueError("Invalid Application ID")

	if(event['request']['type'] == "IntentRequest"):
		speak_alexa = on_intent(event['request'], event['session'])
		return speak_alexa

	return

def on_intent(intent_request, session):
	intent = intent_request['intent']
	intent_name = intent_request['intent']['name']

	#please replace "your_intent_name"
	if intent_name == "your_intent_name":
		return intents_flow(intent, session)
	else:
		raise ValueError("Invalid intent")

def intents_flow(intent, session):
	card_title = intent['name']
	session_attributes = {}
	should_end_session = True

	#please replace "your_slot_name"
	if 'your_slot_name' in intent['slots']:
		input_store = intent['slots']['your_slot_name']['value']

		#please replace "url"
		listurl = "url"
		listhtml = requests.get(listurl)
		listsoup = BeautifulSoup(listhtml.text, "html.parser")

		#目的に応じて処理するhtmlを変更
		#h3配下のaを全て取得
		h3select = listsoup.select('h3 > a')
		v = []
		search = False
		for val in h3select:
			if input_store in val.string:
				search = True
				v.append({
					"s" : val.string,
					"url" : val.attrs['href']
				})

		#目的のものを見つけられなかった時のreturn
		if(search == False):
			output_text = "sorry..."
			return resp_text_message(output_text)

		output_text = ""
		for t in v:
			#------------目的に応じて処理を変更------------
			print(str(t))
			tablehtml = requests.get(t['url'])
			tablesoup = BeautifulSoup(tablehtml.text, "html.parser")

			storename = ""
			timeinfo = ""

			if(t['url'].find("handscafe") != -1):
				storename = t['store']
				timeinfo = tablesoup.select('section.box-2 > dl > dd')[2].string.strip()
				timeinfo = timeinfo.replace("～", "から")
			elif(t['url'].find("expo") != -1):
				continue
			elif(t['url'].find("be.") != -1):
				storename = t['store']
				timeinfo = tablesoup.select('table.shop-info-table > tr > td')[3].string.strip()
				timeinfo = timeinfo.replace("～", "から")
			else:
				storename = t['store']
				timeinfo = tablesoup.select('table.p-simple-table--03 > tr > td')[1].string.strip()
				timeinfo = timeinfo.replace("～", "から")
				
			output_text += storename + "は" + timeinfo + "、"
			#------------目的に応じて処理を変更------------


		if(output_text == ""):
			output_text = "うまく見つけられなかったよ、ごめん。"
		else:
			output_text += "です。"

		return resp_text_message(output_text)


def resp_text_message(speech_message):
	return {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
			'outputSpeech': {
				'type': 'PlainText',
				'text': speech_message
			},
			'card': {
				'type': 'Simple',
				"content": "カードの内容：" + speech_message,
				"title": "デバッグ"
			},
			'reprompt': {
				'outputSpeech': {
					'type': 'PlainText',
					'text': speech_message
				}
			},
			'shouldEndSession': True
		}
	}