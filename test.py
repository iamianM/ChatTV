#!/usr/bin/env python2

import time
import hashlib

#from rovi.tv_listings import TVListings

autocomplete_key = 'twf3ry66pb7stjdjuzzhzwdv'
autocomplete_secret_key = 'TeaCG2TbdN'
search_key = 'jh6b4hqegxr2bwq97kwf7w3s'
search_secret_key = 'f3G8TBfxgk'
tvlistings_key = 'ytbfb5tufg5hdhyratpc6ryr'
sig = hashlib.md5()
line = search_key+search_secret_key+str(int(time.time()))
line = line.encode('utf-8')
sig.update(line)
sig = sig.hexdigest()
#tv_listings = TVListings(api_key=tvlistings_key)

f = open('testOutput', 'w')

#print tv_listings.services(api_key=search_key, country_code='US', locale='en-US', postal_code='32304', sig = sig
#s = tv_listings.services(postal_code='32304', country_code='US')
#f.write(s.text)
#print tv_listings.service_details(service_id='361032')
#print tv_listings.service_details(service_id='361032')
#print tv_listings.grid_schedule(service_id='361032')
#print tv_listings.program_details(program_id='4258917')
#print tv_listings.celebrity_details(name_id='100614')

comcast_serviceID = "61805"

import urllib, json
url1 = "http://api.rovicorp.com/TVlistings/v9/listings/services/postalcode/32304/info?locale=en-US&countrycode=US&apikey="+tvlistings_key+"&sig="+sig
url2 = "http://api.rovicorp.com/TVlistings/v9/listings/gridschedule/"+comcast_serviceID+"/info?apikey="+tvlistings_key+"&sig="+sig+"&locale=en-US&duration=120"
url_service_details = "http://api.rovicorp.com/TVlistings/v9/listings/servicedetails/serviceid/"+comcast_serviceID+"/info?locale=en-US&apikey="+tvlistings_key+"&sig="+sig

#This is for Python 2
#response = urllib.urlopen(url2)
#data = json.loads(response.read())

import urllib.request
with urllib.request.urlopen(url2) as url:
    data = url.read()
data = json.loads(response.read())
#print(data)
grid_channels = data["GridScheduleResult"]
grid_channels = grid_channels["GridChannels"]
import csv
import json
#with open('data1.txt', 'w') as outfile:
 #   json.dump(airings, outfile)

#x = json.loads(airings)
#x = airings
f = csv.writer(open("test.csv", "wb+"))

# Write CSV Header, If you dont need that, remove this line
f.writerow(["Channel", "CallLetters", "Category", "Stereo", "Dolby", "Title", "Color", "HDLevel", "DVS", "AiringTime", "DSS", "CC", "ProgramId", "HD", "Duration", "LetterBox", "SAP", "Sports", "TVRating", "AiringType"])

def myfunction(text):
    try:
        text = unicode(text, 'utf-8')
    except TypeError:
        return text
import sys
reload(sys)
sys.setdefaultencoding('utf8')

i = 0
for airings in grid_channels:
	x = airings["Airings"]
	print i
	print x
	for x in x:
	    f.writerow([airings["Channel"],
	    			airings["CallLetters"],
	    			x["Category"],
					#x["Stereo"],
					#x["Dolby"],
					#x["Subcategory"],
					x["Title"],
					#x["Color"],
					#x["HDLevel"],
					#x["DVS"],
					x["AiringTime"],
					#x["DSS"],
					#x["CC"],
					x["ProgramId"],
					x["HD"],
					x["Duration"],
					x["LetterBox"],
					x["SAP"],
					x["Sports"],
					x["TVRating"],
					x["AiringType"]])
	i = i + 1
'''
import json
from pandas.io.json import json_normalize

json_normalize(data['results'])
'''
#http://api.rovicorp.com/service/version/function/optional parameters/ functionRequest?parameter=value [&parameter=value]...[&parameter=value]
#http://api.rovicorp.com/TVlistings/v9/listings/services/postalcode/32304/info?locale=en-US&countrycode=US&apikey=maf2tnz7f5uspr9kccv8xtju&sig=0f07a77f9cbf4e7b8906b040c44159d7