import sys
import subprocess
from datetime import date


def install_requirements():
    try:
        # implement pip as a subprocess:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'arrow'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
        print('Requirements are installed')
    except ImportError:
        raise RuntimeError('RuntimeError')


def economic_calendar(url):

    import arrow
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    # Process of requesting data from the url -->

    url = url  # the URL we are scraping, actual URL in the function call

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.76 Safari/537.36'}  # the URL only accepts browser access

    request = requests.get(url, headers=header)  # requesting access to the URL

    # Process of requesting data from the url <--

    # HTML handling -->

    soup = BeautifulSoup(request.text, 'html.parser')  # BeautifulSoup treatment of the HTML

    table = soup.find('table', {'id': 'economicCalendarData'})  # Finding the table of data that we need

    body = table.find('tbody')  # Selecting only the body of the table

    rows = body.findAll('tr', {'class': 'js-event-item'})  # Selecting only the table rows

    cal_time = []  # Lists where we will append the data for each economic event
    cal_flag = []
    cal_impact = []
    cal_url = []
    cal_event = []
    cal_current = []
    cal_estimate = []
    cal_last = []

    # 'tr' = table rows
    # 'td' = table columns

    for tr in rows:
        event_time = tr.attrs['data-event-datetime']  # selecting the event time tag 'data-event-datetime'
        event_time = arrow.get(event_time,
                               'YYYY/MM/DD HH:mm:ss')  # converting time to a python supported date format
        event_time = event_time.strftime('%D %H:%M')
        cal_time.append(event_time)

        column = tr.find('td', {'class': 'flagCur'})  # selecting the country tag 'flagCur'
        flag = column.find('span')
        cal_flag.append(flag.get('title'))

        event_impact = tr.find('td', {'class': 'sentiment'})
        event_impact = event_impact.findAll('i', {
            'class': 'grayFullBullishIcon'})  # selecting the impact tag 'grayFullBullishIcon'
        cal_impact.append(len(event_impact))

        event = tr.find('td', {'class': 'event'})
        a = event.find('a')  # selecting the name of the economic event and URL

        cal_url.append('{}{}'.format(url, a['href']))  # appending only the URL

        cal_event.append(a.text.strip())  # appending only the name of the economic event

        current = tr.find('td', {'class': 'event'}).find_next_sibling().text  # selecting the actual number
        cal_current.append(current)

        estimate = tr.find('td', {'class': 'prev'}).find_previous_sibling().text  # selecting the forecasted number
        cal_estimate.append(estimate)

        last = tr.find('td', {'class': 'prev'})  # selecting the previous number
        last = last.find('span').text
        cal_last.append(last)

    # HTML handling <--

    # converting lists to lists of lists then pandas dataframe -->

    cal_data = {'Datetime': cal_time,
                'Country': cal_flag,
                'Impact': cal_impact,
                'Event': cal_event,
                'Actual': cal_current,
                'Forecast': cal_estimate,
                'Previous': cal_last,
                'Link': cal_url}

    cal_df = pd.DataFrame(cal_data, columns=['Datetime',
                                             'Country',
                                             'Impact',
                                             'Event',
                                             'Actual',
                                             'Forecast',
                                             'Previous',
                                             'Link'])

    # converting lists to lists of lists then pandas dataframe <--

    return cal_df  # return the list of economic events


def main():

    install_requirements()  # calling our programs requirements to be installed

    data = economic_calendar('https://investing.com/economic-calendar/')  # calling the URL to be crawled through

    # exporting our data to the same directory as the this .py file -->

    filename = f'events{date.today()}.csv'

    data.to_csv(filename, index=False)

    # exporting our data to the same directory as the this .py file <--


if __name__ == '__main__':
    main()
