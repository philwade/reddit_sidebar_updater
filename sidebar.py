import praw
import HTMLParser
import requests
import json
from dateutil import parser
import datetime

class HSideBar():
    def __init__(self, config):
        self.username = config['name'] or raw_input('Reddit Username: ')
        self.password = config['password'] or raw_input('Reddit Password: ')
        self.subreddit = 'PbzcrgvgvirUF'
        self.matches = { 'upcoming': '\n* Upcoming Matches\n', 'live': '\n* Live Matches\n' }
        self.matchTemplate = '* [%(time)s %(name)s](%(url)s)  \n%(team_name1)s vs %(team_name2)s\n\n'
        self.redditagent = None

    def grabMatches(self):
        r = requests.get('http://www.gosugamers.net/hearthstone/api/matches?apiKey=764b0c830d59b8eae8079f2482ac7461')
        data = json.loads(r.text)
        liveCount = 0
        upcomingCount = 0

        for match in data['matches']:
            if match['isLive']:
                container = 'live'
                time = 'LIVE'
                liveCount += 1
            else:
                container = 'upcoming'
                diff = parser.parse(match['datetime'].split('+')[0]) - datetime.datetime.now()
                time = str(diff.days) + 'd ' + str(diff.seconds / 60 / 60) + 'h '+ str(diff.seconds % 60) + 'm'
                upcomingCount += 1

            self.matches[container] += self.matchTemplate % \
            {
                'url': match['tournament']['pageUrl'],
                'name': match['tournament']['name'],
                'team_url1': match['firstOpponent']['pageUrl'],
                'team_name1': match['firstOpponent']['shortName'],
                'team_url2': match['secondOpponent']['pageUrl'],
                'team_name2': match['secondOpponent']['shortName'],
                'time': time,
            }

        if liveCount == 0:
            self.matches['live'] += '* No Matches Currently Live\n\n'
        if upcomingCount == 0:
            self.matches['upcoming'] += '* No Upcoming Matches\n\n'

    def getRedditAgent(self):
        if self.redditagent == None:
            r = praw.Reddit(user_agent='HSidebar 0.0.1')
            r.login(self.username,self.password)
            self.redditagent = r
        return self.redditagent


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
        sidebar = sidebar.replace('%%MATCHES%%', self.matches['live'] + self.matches['upcoming'])
        settings['description'] = h.unescape(sidebar)
        settings = r.get_subreddit(self.subreddit).update_settings(description=settings['description'])

f = open('config')
line = f.readline()
name = line.split(':')[0]
password = line.split(':')[1].strip()
config = {
    'name': name,
    'password': password,
}
sidebar = HSideBar(config)
sidebar.grabMatches()
sidebar.writeSidebar()
print sidebar.matches['live']
print sidebar.matches['upcoming']
