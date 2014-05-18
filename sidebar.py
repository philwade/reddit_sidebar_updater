import praw
import HTMLParser
import requests
import json
from dateutil import parser
import datetime
import pytz
import bitly_api

class HSideBar():
    def __init__(self, config):
        self.username = config['name'] or raw_input('Reddit Username: ')
        self.password = config['password'] or raw_input('Reddit Password: ')
        self.bitly = config['bitly']
        self.subreddit = 'CompetitiveHS'
        self.matches = '\n* Upcoming Matches\n'
        self.matchTemplate = '* [%(time)s %(name)s](%(url)s)  \n%(team_name1)s vs %(team_name2)s\n\n'
        self.redditagent = None
        self.shortener = None

    def grabMatches(self):
        r = requests.get('http://www.gosugamers.net/hearthstone/api/matches?apiKey=764b0c830d59b8eae8079f2482ac7461')
        data = json.loads(r.text)

        if len(data['matches']) > 0:
            for match in data['matches']:
                if match['isLive']:
                    time = 'LIVE - '
                else:
                    days, minutes, seconds = ('','','')
                    diff = parser.parse(match['datetime']) - datetime.datetime.now(pytz.timezone('GMT'))
                    if diff.days < 0:
                        time = 'LIVE - '
                    else:
                        if diff.days:
                            days = str(diff.days) + 'd '
                        if (diff.seconds / 60 / 60) > 0:
                            minutes = str(diff.seconds / 60 / 60) + 'h '
                        time = days + minutes + str((diff.seconds / 60) % 60) + 'm - '

                self.matches += self.matchTemplate % \
                {
                    'url': self.shorten(match['tournament']['pageUrl']),
                    'name': match['tournament']['name'],
                    'team_name1': match['firstOpponent']['shortName'],
                    'team_name2': match['secondOpponent']['shortName'],
                    'time': time,
                }
        else:
            self.matches += '* No Upcoming Matches'

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

    def getWiki(self):
        r = self.getRedditAgent()
        sidebar = r.get_subreddit(self.subreddit).get_wiki_page('sidebar').content_md
        return sidebar

    def writeSidebar(self):
        h = HTMLParser.HTMLParser()
        r = self.getRedditAgent()
        sidebar = self.getWiki()
        settings = r.get_subreddit(self.subreddit).get_settings()

        #Update the sidebar
        sidebar = sidebar.replace('%%MATCHES%%', self.matches)
        settings['description'] = h.unescape(sidebar)
        settings = r.get_subreddit(self.subreddit).update_settings(description=settings['description'])

f = open('/home/pwade/reddit_sidebar_updater/config')
line = f.readline()
name = line.split(':')[0]
password = line.split(':')[1].strip()
bitly = f.readline().strip()
config = {
    'name': name,
    'password': password,
    'bitly': bitly,
}
sidebar = HSideBar(config)
sidebar.grabMatches()
sidebar.writeSidebar()
