

import json
import requests

def search_product(searches):
	key = 'MengyiSh-chatbotb-PRD-579658d5d-89c973ba'
	# searches = []
	# with open("searches.txt", "r") as searchfile:
	# 	searches = searchfile.readlines()
	for item in searches:
		search = item.split(',')[0]
		print(search)
		MinPrice = item.split(',')[1]
		url = ("""http://svcs.ebay.com/services/search/FindingService/v1"""
		"""?OPERATION-NAME=findItemsByKeywords"""
		"""&sortOrder=PricePlusShippingLowest"""
		"""&buyerPostalCode=92128&SERVICE-VERSION=1.13.0"""
		"""&SECURITY-APPNAME=""" + key +
		"""&RESPONSE-DATA-FORMAT=JSON"""
		"""&REST-PAYLOAD"""
		"""&itemFilter(0).name=Condition"""
		"""&itemFilter(0).value=New"""
		"""&itemFilter(1).name=MinPrice"""
		"""&itemFilter(1).value=""" + MinPrice+
		"""&itemFilter(1).paramName=Currency"""
		"""&itemFilter(1).paramValue=USD"""
		"""&keywords=""" + search)
		print('URL')
		print(url)
		url = url.replace(" ", "%20")
		apiResult = requests.get(url)
		# print(apiResult)
		parseddoc = apiResult.json()
		# print(parseddoc)
		for item in (parseddoc["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]):
			title = item["title"][0]
			condition = item['condition'][0]['conditionDisplayName'][0]
			price = item['sellingStatus'][0]["convertedCurrentPrice"][0]['__value__']
			data = {'titile':titile, 'price':price, 'condition': condition}
			return data
			print(data)

if __name__ == "__main__":
	search_product(['laptop,1000'])
