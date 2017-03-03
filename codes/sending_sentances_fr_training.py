# -*- coding: utf-8 -*-

import os.path
import sys
import re
import time
import json
import pandas as pd

try:
	import apiai
except ImportError:
	sys.path.append(
		os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
	)
	import apiai

CLIENT_ACCESS_TOKEN = '8f98e831118844ed84c7772121708a5d'

def main():
	ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
	count = 0

	f = open('/home/karan/Nexchange/api_ai_whatsapp/textfiles/test.txt')

	for sent in f.readlines():
		sent = sent.strip()
		request = ai.text_request()

		if re.findall('^[0-9]+/[0-9]+/[0-9]+.',sent):
			print sent
			count = count + 1
			request.session_id = count
			request.query = sent
			response = request.getresponse().read()

			print response

if __name__ == '__main__':
	main()          