import praw

class HSideBar():
    def __init__(self):
        self.username = raw_input('Reddit Username: ')
        self.password = raw_input('Reddit Password: ')
        self.subreddit = 'PbzcrgvgvirUF'

        r = praw.Reddit(user_agent='HSidebar 0.0.1')
        r.login(self.username,self.password)
        settings = r.get_subreddit(self.subreddit).get_settings()
        #Update the sidebar
        settings['description'] = 'this is a test'
        settings = r.get_subreddit(self.subreddit).update_settings(description=settings['description'])

HSideBar()
