# economic-events-webscraper

This is a sample project that will only scrape today's economic events from investing.com. The full project will webscrape historical and future economic events.

Currently the script is designed to install all requirements (pandas, arrow, bs4, etc) and will do so each time it is run. This code can be commented out if you do not wish to schedule the script.

When run, the outputted .csv file will be in the same location as the economicevents.py file and the naming convention is 'events' + today() '.csv'
