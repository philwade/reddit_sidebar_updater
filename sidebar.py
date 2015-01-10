import sys
import praw
import HTMLParser
import requests
import json
from dateutil import parser
import datetime
import time as clock
import pytz
import bitly_api
import calendar

class HSideBar():
    def __init__(self, config):
        self.username = config['name'] or raw_input('Reddit Username: ')
        self.password = config['password'] or raw_input('Reddit Password: ')
        self.bitly = config['bitly']
        self.subreddit = config['subreddit'] or 'PbzcrgvgvirUF'
        self.matchString = '\n* Upcoming Events\n'
        self.matches = []
        self.matchTemplate = '* [%(time)s %(name)s](%(url)s)  \n\n'
        self.footnote = '* [Event data by HearthstoneCalendar.com](http://www.hearthstonecalendar.com)\n'
        self.redditagent = None
        self.shortener = None
        self.matchLimit = 10

    def parseTime(self, timeString):
        timeString = timeString.replace('(All day)', '01:00-23:00')
        dt = parser.parse(timeString).astimezone(pytz.timezone('GMT'))
        diff = dt - datetime.datetime.now(pytz.timezone('GMT'))
        time = self.printableDate(diff)
        timeStamp = int(dt.strftime('%s'))

        return time, timeStamp, diff

    def grabMatches(self):
        r = requests.get('http://hearthstonecalendar.com/events/json')
        data = json.loads(r.text)

        if len(data['events']) > 0:
            for event in data['events']:
                time, timeStamp, diff = self.parseTime(event['startDateTime'])

                self.matches.append( \
                {
                    'url': self.shorten(event['url']),
                    'name': event['title'],
                    'time': time,
                    'timestamp': timeStamp,
                })

    def printableDate(self, diff):
        days, minutes, seconds = ('','','')
        if diff.days < 0:
            time = 'LIVE - '
        else:
            if diff.days:
                days = str(diff.days) + 'd '
            if (diff.seconds / 60 / 60) > 0:
                minutes = str(diff.seconds / 60 / 60) + 'h '
            time = days + minutes + str((diff.seconds / 60) % 60) + 'm - '
        return time

    def writeMatchString(self):
        matchCount = 0
        if len(self.matches) > 0:
            sortedMatches = sorted(self.matches, lambda x,y: cmp(x['timestamp'], y['timestamp']))
            for match in sortedMatches:
                matchCount +=1
                self.matchString += self.matchTemplate % match

                if matchCount >= self.matchLimit:
                    break
            self.matchString += self.footnote
        else:
            self.matchString += '* No Upcoming Events'

    def getWikiMatches(self):
        page = self.getWiki('tournaments')
        list = page.split('\n')

        for match in list[2:]:
            time, title, matchup, url = match.split('|')
            url = url.strip()

            time, timeStamp, diff = self.parseTime(time)

            if diff.total_seconds() < -14400:
                continue

            self.matches.append( \
            {
                'url': self.shorten(url),
                'name': title,
                'matchup': matchup,
                'time': time,
                'timestamp': timeStamp
            })

    def getRedditAgent(self):
        if self.redditagent == None:
            r = praw.Reddit(user_agent='HSidebar 0.0.1')
            r.login(self.username,self.password)
            self.redditagent = r
        return self.redditagent

    def getShortener(self):
        if self.shortener == None:
            self.shortener = bitly_api.Connection(access_token=self.bitly)
        return self.shortener

    def shorten(self, url):
        s = self.getShortener()
        short = s.shorten(url)
        return short['url']

    def getWiki(self, wikiPage):
        r = self.getRedditAgent()
        sidebar = r.get_subreddit(self.subreddit).get_wiki_page(wikiPage).content_md
        return sidebar

    def writeSidebar(self):
        h = HTMLParser.HTMLParser()
        r = self.getRedditAgent()
        sidebar = self.getWiki('sidebar')
        settings = r.get_subreddit(self.subreddit).get_settings()

        self.writeMatchString()

        #Update the sidebar
        sidebar = sidebar.replace('%%MATCHES%%', self.matchString)
        settings['description'] = h.unescape(sidebar)
        settings = r.get_subreddit(self.subreddit).update_settings(description=settings['description'])

try:
    configFile = sys.argv[1]
except IndexError:
    print 'No configuration given'
    sys.exit()

f = open(configFile)
configString = f.read()
config = json.loads(configString)

sidebar = HSideBar(config)
sidebar.grabMatches()
sidebar.writeSidebar()
