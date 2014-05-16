import praw
import requests
from bs4 import BeautifulSoup

class HSideBar():
    def __init__(self, config):
        self.username = config['name'] or raw_input('Reddit Username: ')
        self.password = config['password'] or raw_input('Reddit Password: ')
        self.subreddit = 'PbzcrgvgvirUF'

    def grabMatches(self):
        r = requests.get('http://www.gosugamers.net/hearthstone/gosubet')
        soup = BeautifulSoup(r.text)
        upcoming = soup.findAll(id='col1')[0].findAll('div', 'box')[1]
        print upcoming.span

    def writeSidebar(self):
        r = praw.Reddit(user_agent='HSidebar 0.0.1')
        r.login(self.username,self.password)
        settings = r.get_subreddit(self.subreddit).get_settings()
        #Update the sidebar
        settings['description'] = 'no wait still a test'
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
HSideBar(config)
