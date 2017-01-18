#! /usr/bin/Rscript

import praw
import pdb
import re
import os
import subprocess

path = "C:/Users/Ian/Dropbox/WatchTV/"
#subprocess.call ("C:/Program Files/R/R-3.2.3/bin/x64/Rscript --vanilla " + path + "WatchTV.r", shell=True)
subprocess.call (["C:/Program Files/R/R-3.2.3/bin/Rscript", "--vanilla", path + "WatchTV.r"])

user_agent = ("ChatTV Bot 0.1")
r = praw.Reddit(user_agent = user_agent)
subreddit = r.get_subreddit("ChatTV")

#call_letters_top = ("WCBS", "WNBC", "WABC", "UNI", "ESPN", "TBS", "USA", "DISNEY", "FNC", "TNT", "DSC", "HIST", "HGTV", "AMC", "TELMUN", "FX", "FOOD", "LIFE", "Syfy", "A&E", "TLC", "HALMRK", "BRAVO", "SPK", "CNN", "ANIMAL", "DISJr", "VH1", "TVLAND", "MTV", "BET", "msnbc", "COMEDY", "E!", "NGC", "OWN", "WE", "truTV", "LMN", "NicJr", "TRAVEL", "GSN", "ESPN2", "FXX", "HMMHD", "FS1", "INSP", "NBCSN", "CNBC", "DISXD", "HLN")

REDDIT_USERNAME = 'freekrabbypatties' 
REDDIT_PASS = 'fgrtyew$'

r.login(REDDIT_USERNAME, REDDIT_PASS,disable_warning=True)


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def add_flair_to_post(subm, channel_name):
    if APPEND_CHANNEL_TO_CSS_CLASS:
        flair_class = LINK_FLAIR_CSS_CLASS + '-' + channel_name
    else:
        flair_class = LINK_FLAIR_CSS_CLASS
    if CHANNEL_NAME_AS_FLAIR_TEXT:
        flair_text = channel_name
    else:
        flair_text = LINK_FLAIR_TEXT
    print('Adding flair...')
    subm.set_flair(flair_css_class=flair_class,
                   flair_text=flair_text)


if not os.path.isfile("posts_submitted.txt"):
    posts_submitted = []
    # If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_submitted.txt", "r") as f:
        posts_submitted = f.read()
        posts_submitted = posts_submitted.split("\n")


import glob
def post_to_reddit(postTitle, text, call_letter):
    subreddit = r.get_subreddit('ChatTV')
    #submission = subreddit.submit(postTitle, text=text, captcha=None)
    #print("Submitting " + submission.title)
    #r.set_flair("ChatTV", submission, flair_text=call_letter)

from datetime import datetime
import sched, time
def main_post_to_reddit():
    starttime=time.time()
    while True:
        print("tick")
        s = sched.scheduler(time.time, time.sleep)
        path = "C:/Users/Ian/Dropbox/WatchTV/Posts/"
        for filename in glob.glob(os.path.join(path, '*.txt')):
            call_letter = find_between(filename,"/Posts\\","sDATE")
            date = find_between(filename,"sDATE","eDATE")
            t = find_between(filename,"sTIME","eTIME")
            hour = int(t[0:2])
            mins = int(t[2:4])
            sec = int(t[4:6])
            t = t[0:2] + ":" + t[2:4] + ":" + t[4:6]
            meridiem = "AM"
            HOUR = hour
            if hour > 12:
                HOUR = hour - 12
                meridiem = "PM"
            postTitle = "[" + call_letter + "] " + str(HOUR)

            if mins != 0 and mins < 10:
                postTitle = postTitle + ":0" + str(mins) + meridiem
            elif mins != 0 and mins >= 10:
                postTitle = postTitle + ":" + str(mins) + meridiem
            else:
                postTitle = postTitle + ":00" + meridiem

            
            if postTitle not in posts_submitted:
                with open(filename, 'r') as myfile:
                    text=myfile.read()
                    title = find_between(text, "T-","\\n")
                    print(text)
                    text.replace("T-"+title+"\\n","")
                    postTitle = postTitle + " " + title
                    #local_time = time.localtime( time.time() )
                    dateTime = date + "T" + t + "Z"
                    dateTime = datetime.strptime(dateTime, '%Y-%m-%dT%H:%M:%SZ')
                    wait = dateTime - datetime.now()
                    print(dateTime, postTitle)
                    if wait.total_seconds() >= 0:
                        print("Waiting: " + str(wait.total_seconds()))
                        s.enter(wait.total_seconds(),1,post_to_reddit, argument=(postTitle,text,call_letter,))
                        posts_submitted.append(postTitle)
        s.run()
        wait_time = 60*120  #time in seconds
        time.sleep(wait_time - ((time.time() - starttime) % wait_time))

#This is where we actually run
main_post_to_reddit()
#s = sched.scheduler(time.time, time.sleep)
#wait = 60*120
#s.enter(wait,1,main_post_to_reddit, (sc,))
#s.run()

# Write our updated list back to the file
with open("posts_submitted.txt", "w") as f:
    for post_title in posts_submitted:
        f.write(post_title + "\n")



#subreddit = r.get_subreddit('ChatTVbot')
#subreddit.submit("Testing bot", text="test")
'''
for submission in subreddit.get_hot(limit=5):
    # print submission.title

    # If we haven't replied to this post before
    if submission.id not in posts_replied_to:

        # Do a case insensitive search
        if re.search("i love python", submission.title, re.IGNORECASE):
            # Reply to the post
            submission.add_comment("Nigerian scammer bot says: It's all about the Bass (and Python)")
            print "Bot replying to : ", submission.title

            # Store the current id into our list
            posts_replied_to.append(submission.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
'''