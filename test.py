import praw
import requests
import json

class HSideBar():
    def __init__(self, config):
        self.username = config['name'] or raw_input('Reddit Username: ')
        self.password = config['password'] or raw_input('Reddit Password: ')
        self.subreddit = 'PbzcrgvgvirUF'
        self.matches = { 'upcoming': '>> Upcoming Matches', 'live': '>> Live Matches' }
        self.matchTemplate = '*\n\
            [%(url)s](%(name)s)\n\
            [%(team_url1)s](%(team_name1)s) vs [%(team_url2)s](%(team_name2)s)\n'

    def grabMatches(self):
        r = requests.get('http://www.gosugamers.net/hearthstone/api/matches?apiKey=764b0c830d59b8eae8079f2482ac7461')
        data = json.loads(r.text)

        for match in data['matches']:
            if match['isLive']:
                container = 'live'
            else:
                container = 'upcoming'
            self.matches[container] += self.matchTemplate % \
                {
                    'url': match['tournament']['pageUrl'],
                    'name': match['tournament']['name'],
                    'team_url1': match['firstOpponent']['pageUrl'],
                    'team_name1': match['firstOpponent']['shortName'],
                    'team_url2': match['secondOpponent']['pageUrl'],
                    'team_name2': match['secondOpponent']['shortName'],
                }

    def writeSidebar(self):
        r = praw.Reddit(user_agent='HSidebar 0.0.1')
        r.login(self.username,self.password)
        settings = r.get_subreddit(self.subreddit).get_settings()
        #Update the sidebar
        settings['description'] = self.matches['live'], self.matches['upcoming']
        settings = r.get_subreddit(self.subreddit).update_settings(description=settings['description'])

f = open('config')
line = f.readline()
name = line.split(':')[0]
password = line.split(':')[1].strip()
print name
print password
config = {
    'name': name,
    'password': password,
}
sidebar = HSideBar(config)
sidebar.grabMatches()
sidebar.writeSidebar()

