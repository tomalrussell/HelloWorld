import requests
import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
import psycopg2

def recode_cat_name(name):
	# recode by name
	cats = {
		"Film, Media & Entertainment": "Culture & Art",
		"Performing & Visual Arts":    "Culture & Art",
		"Community & Culture":         "Culture & Art",
		"Music":                       "Culture & Art",

		"Religion & Spirituality": "Business & Education",
		"Family & Education":      "Business & Education",
		"Science & Technology":    "Business & Education",
		"Government & Politics":   "Business & Education",
		"Business & Professional": "Business & Education",

		"Seasonal & Holiday": "Sport & Travel",
		"Sports & Fitness":   "Sport & Travel",
		"Travel & Outdoor":   "Sport & Travel",
		"Auto, Boat & Air":   "Sport & Travel",

		"Fashion & Beauty":  "Fashion & Health",
		"Health & Wellness": "Fashion & Health",

		"Food & Drink": "Food & Drink"
	}

	if name in cats:
		return cats[name]
	else:
		return "Other"

def parse_event(event):
	cat_name = recode_cat_name(event['category']['name'])

	prices = []
	any_donation = False
	availability = []

	free = [t['free'] for t in e['ticket_classes']]

	for ticket in event['ticket_classes']:
		if 'on_sale_status' in ticket and (ticket['on_sale_status'] == 'SOLD_OUT' or ticket['on_sale_status'] == 'UNAVAILABLE'):
			availability.append(False)
		else:
			availability.append(True)

			if ticket['free'] or ticket['donation']:
				prices.append(0)
			else:
				prices.append(ticket['cost']['value'])

			if ticket['donation']:
				any_donation = True

	#if no tickets display the prices as none
	if len(prices) > 0:
		min_price = min(prices)
		max_price = max(prices)
	else:
		min_price = None
		max_price = None

	e = {
		"lon":float(event['venue']['address']['longitude']),
		"lat":float(event['venue']['address']['latitude']),
		"category":     cat_name,
		"name":         event['name']['text'],
		"venue":        event['venue']['name'],
		"start":        event['start']['utc'],
		"end":          event['end']['utc'],
		"start_utc":    event['start']['utc'],
		"end_utc":      event['end']['utc'],
		"start_iso":    event['start']['utc'],
		"end_iso":      event['end']['utc'],
		"postcode":     event['venue']['address']['postal_code'],
		"address":      event['venue']['address']['address_1'],
		"min_price":    min_price,
		"max_price":    max_price,
		"free":         any(free),
		"availability": any(availability),
		"donation":     any_donation
	}
	return e


def save_event(event):
	# save to file or db
	return 1

def get_london_events(page,token):
		now = datetime.now()
		then = now + timedelta(days=7)

		format_s = "%Y-%m-%dT%H:%M:%S"
		start_time=datetime.strftime(now,format_s)
		end_time=datetime.strftime(b,format_s)

		data = {
			"expand":"category,ticket_classes,venue",
			"venue.city": "london",
			"start_date.range_start": start_time,
			"start_date.range_end": end_time,
			"sort_by":"date",
			"page": page , # request page from API
		}

		response = requests.get(  #make an http request (insteaf of get =put,post,delete)
			"https://www.eventbriteapi.com/v3/events/search/", # URL
			headers = {  # headers = metadata (ex :cookie)     # header (=object) = KEY + VALUE
				"Authorization": "Bearer "+token,              # "Bearer" is specific to eventbrite API
			},
			params=data,  # question marks = all the infos at the end of the url (everything foldng up into a string)
			verify = True,  # Verify SSL certificate (because our url starts with https = secure url)
		)

		return response.json()

def get_all_pages(token):
	last = False #are we on the last page?
	page = 1     #current page number

	while(not last):
		r = get_london_events(page,token)  #get this page of events
		print str(page) + " of " + str(r['pagination']['page_count'])
		for e in r['events']:
			event - parse_event(e)
			save_event(event)
		last = r['pagination']['page_count'] == page
		page = page + 1


if __name__ == "__main__":
	dotenv_path = join(dirname(__file__), '.env')
	load_dotenv(dotenv_path)

	EVENTBRITE_TOKEN = os.environ.get("EVENTBRITE_TOKEN")
	get_all_pages(EVENTBRITE_TOKEN)