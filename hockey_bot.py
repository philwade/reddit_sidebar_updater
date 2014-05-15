#HockeyBotS v1.1.0 by /u/TeroTheTerror
import datetime
import time
import urllib2
import HTMLParser
import praw
from bs4 import BeautifulSoup

class Hockey_Bot_S(object):

    def __init__(self):
        #Define divisions in a list
        divisions = ['Atlantic', 'Metropolitan', 'Central', 'Pacific']
        self.username = raw_input('Reddit Username: ')
        self.password = raw_input('Reddit Password: ')
        self.subreddit = raw_input('Subreddit (ex: penguins, not /r/penguins): ')
        self.userAgent = 'Hockey_Bot_S/v1.1.0 by TeroTheTerror'

        while (True):
            print '\nDivisions:'
            y = 1
            #Number divisions and print in list
            for div in divisions:
                print str(y)+': '+div
                y += 1

            self.division = int(raw_input('Select the number of your division: '))

            if self.division < 5 and self.division > 0:
                #Print the divisions that was picked
                print ('\nThank you, you\'ve selected the %s division') % divisions[(self.division - 1)]
                break
            else:
                print '\nThe number you entered is not a choice in the list, please try again.'

        self.fix = (raw_input('\nWould you like the table to be formatted for icons? \n(y/n): ').lower())
    
        
    def scrape(self):
        w = urllib2.urlopen('http://www.nhl.com/ice/standings.htm?type=DIV#&navid=nav-stn-div')
        soup = BeautifulSoup(w.read())

        standings_list = []
        final_list1 = []
        final_list2 = []
        #Find the division table
        if self.division == 1:
            for table in soup.findAll('table', summary="Division Standings.  Each row represents a team in the Atlantic Division. A clickable column header will resort the table results in the most meaningful manner for that column (e.g., by Wins or Last 10 Record). Each column represents a statistical value: wins, total points, home record, etc."):
                rawdata = table
        elif self.division == 2:
            for table in soup.findAll('table', summary="Division Standings.  Each row represents a team in the Metropolitan Division. A clickable column header will resort the table results in the most meaningful manner for that column (e.g., by Wins or Last 10 Record). Each column represents a statistical value: wins, total points, home record, etc."):
                rawdata = table
        elif self.division == 3:
            for table in soup.findAll('table', summary="Division Standings.  Each row represents a team in the Central Division. A clickable column header will resort the table results in the most meaningful manner for that column (e.g., by Wins or Last 10 Record). Each column represents a statistical value: wins, total points, home record, etc."):
                rawdata = table
        elif self.division == 4:
            for table in soup.findAll('table', summary="Division Standings.  Each row represents a team in the Pacific Division. A clickable column header will resort the table results in the most meaningful manner for that column (e.g., by Wins or Last 10 Record). Each column represents a statistical value: wins, total points, home record, etc."):
                rawdata = table
        else:
            print 'An error has occured, please contact TeroTheTerror'

        #Make list of cells within a list of rows
        rawdata_list = [tr.findAll('td') for tr in rawdata.findAll('tr')]
        #Text only version of rawdata_list
        for row in rawdata_list:
            standings_list.append([cell.text for cell in row])
        #Get rid of problematic characters
        for lst in standings_list:
            final_list1.append([val.replace(u'\xa0', u' ') for val in lst])
        
        for lst in final_list1:
            final_list2.append([val.replace(u'\xe9', u'e') for val in lst])
            
        w.close()
        return final_list2

    def generate_tables(self, lst):
        #Time/Date stamp
        updated = datetime.datetime.now().strftime('%b %d, %Y at %I:%M%p')
        if self.division == 1 or self.division == 2:
            #Compiling the table
            standings = "Last Updated: " + updated + "\n"
            standings += "\n|Rank|Team|GP|W|L|OTL|Points|"
            standings += "\n|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[1][0], lst[1][1], lst[1][2], lst[1][3], lst[1][4], lst[1][5], lst[1][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[2][0], lst[2][1], lst[2][2], lst[2][3], lst[2][4], lst[2][5], lst[2][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[3][0], lst[3][1], lst[3][2], lst[3][3], lst[3][4], lst[3][5], lst[3][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[4][0], lst[4][1], lst[4][2], lst[4][3], lst[4][4], lst[4][5], lst[4][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[5][0], lst[5][1], lst[5][2], lst[5][3], lst[5][4], lst[5][5], lst[5][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[6][0], lst[6][1], lst[6][2], lst[6][3], lst[6][4], lst[6][5], lst[6][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[7][0], lst[7][1], lst[7][2], lst[7][3], lst[7][4], lst[7][5], lst[7][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[8][0], lst[8][1], lst[8][2], lst[8][3], lst[8][4], lst[8][5], lst[8][6])
            return standings
    
        else:
            #Compiling the table
            standings = "Last Updated: " + updated + "\n"
            standings += "\n|Rank|Team|GP|W|L|OTL|Points|"
            standings += "\n|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[1][0], lst[1][1], lst[1][2], lst[1][3], lst[1][4], lst[1][5], lst[1][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[2][0], lst[2][1], lst[2][2], lst[2][3], lst[2][4], lst[2][5], lst[2][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[3][0], lst[3][1], lst[3][2], lst[3][3], lst[3][4], lst[3][5], lst[3][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[4][0], lst[4][1], lst[4][2], lst[4][3], lst[4][4], lst[4][5], lst[4][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[5][0], lst[5][1], lst[5][2], lst[5][3], lst[5][4], lst[5][5], lst[5][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[6][0], lst[6][1], lst[6][2], lst[6][3], lst[6][4], lst[6][5], lst[6][6])
            standings += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(lst[7][0], lst[7][1], lst[7][2], lst[7][3], lst[7][4], lst[7][5], lst[7][6])    
            return standings

    def fix_standings(self, text):
        #Use dictionary to replace team names with sub names
        my_dict = {'Columbus': '[](/r/bluejackets)', 'Pittsburgh': '[](/r/penguins)', 'NY Islanders': '[](/r/newyorkislanders)', 'Washington': '[](/r/caps)', 'Philadelphia': '[](/r/flyers)', 'NY Rangers': '[](/r/rangers)', 'New Jersey': '[](/r/devils)', 'Carolina': '[](/r/canes)', 'Boston': '[](/r/bostonbruins)', 'Tampa Bay': '[](/r/tampabaylightning)', 'Montreal': '[](/r/habs)', 'Detroit': '[](/r/detroitredwings)', 'Toronto': '[](/r/leafs)', 'Ottawa': '[](/r/ottawasenators)', 'Florida': '[](/r/floridapanthers)', 'Buffalo': '[](/r/sabres)', 'Chicago': '[](/r/hawks)', 'St. Louis': '[](/r/stlouisblues)', 'Colorado': '[](/r/coloradoavalanche)', 'Minnesota': '[](/r/wildhockey)', 'Dallas': '[](/r/dallasstars)', 'Winnipeg': '[](/r/winnipegjets)', 'Nashville': '[](/r/predators)', 'Anaheim': '[](/r/anaheimducks)', 'San Jose': '[](/r/sanjosesharks)', 'Los Angeles': '[](/r/losangeleskings)', 'Vancouver': '[](/r/canucks)', 'Phoenix': '[](/r/coyotes)', 'Calgary': '[](/r/calgaryflames)', 'Edmonton': '[](/r/edmontonoilers)'}

        if self.fix == 'y':
            for i, j in my_dict.iteritems():
                text = text.replace(i, j)
            return text
        else:
            return text

    def create_sidebar(self):
        #To fix character glitch when grabbing the sidebar
        h = HTMLParser.HTMLParser()
        #Initialize PRAW and login
        r = praw.Reddit(user_agent='HocketBotS v1.1 by TeroTheTerror')
        r.login(self.username,self.password)
        #Grab the sidebar template from the wiki
        sidebar = r.get_subreddit(self.subreddit).get_wiki_page('edit_sidebar').content_md
        #Create list from sidebar by splitting at ***
        sidebar_list = sidebar.split('***')
        #Sidebar with updated tables - +lucky_guess+sidebar_list[6]
        sidebar = (sidebar_list[0]+standings_a+sidebar_list[2])
        #Fix characters in sidebar
        sidebar = h.unescape(sidebar)
        
        return sidebar

    def update_reddit(self):
        #Initialize PRAW and login
        r = praw.Reddit(user_agent='HocketBotS v1.1 by TeroTheTerror')
        r.login(self.username,self.password)
        #Grab the current settings
        settings = r.get_subreddit(self.subreddit).get_settings()
        #Update the sidebar
        settings['description'] = sidebar
        settings = r.get_subreddit(self.subreddit).update_settings(description=settings['description'])

hbs = Hockey_Bot_S()

while(True):
    print 'Scraping Standings...'
    final_list = hbs.scrape()
    print 'Generating Table...'
    standings_b = hbs.generate_tables(final_list)
    print 'Fixing Table...'
    standings_a = hbs.fix_standings(standings_b)
    print 'Grabbing Sidebar Template...'
    sidebar = hbs.create_sidebar()
    print 'Updating Sidebar...'
    hbs.update_reddit()
    print 'Sidebar Updated: '+datetime.datetime.now().strftime('%b %d, %Y at %I:%M%p')
    print 'Sleeping... \n'
    time.sleep(600)
