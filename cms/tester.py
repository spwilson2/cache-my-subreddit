import os
import re

import imgur
import reddit

CHAR_WHITELIST = r'\w,.\- '

def clean_for_use_as_path(string):
    string = re.sub(r'[^%s]' % CHAR_WHITELIST, '-', string)
    string = re.sub(r'[ ]+', '_', string) # Replace spaces with _
    return string

def get_oauth_info():
    from configparser import ConfigParser
    parser = ConfigParser()
    parser.read('login.ini')
    section = parser['Reddit']

    globals().update(section) # Note: is a security risk, don't be dumb.

    return client_id, client_secret, username, password


def main():
    client_id, client_secret, username, password =\
    get_oauth_info()

    r = reddit.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password)

    friends = r.list_friends()
    for friend in friends:
        print(friend)
        for submission in r.submissions(friend):
            save(submission)

def save(submission, basedir='output'):
    basedir = os.path.dirname(os.path.abspath(__file__)) if basedir is None else basedir

    # subreddit/user/PostName
    clean_title = clean_for_use_as_path(submission.title)
    savedir = os.path.join(basedir, submission.subreddit, submission.redditor, clean_title)
    #print(submission.subreddit)
    #print(submission.redditor)
    #print(submission.title)
    #print(clean_title)

    if not os.path.exists(savedir):
        os.makedirs(savedir)

    if imgur.Imgur.is_link(submission.url):
        imgur.Imgur(submission.url).save(savedir,pfx='Post')

if __name__ == '__main__':
    main()

#reddit = praw.Reddit(user_agent=my_user_agent,
#                     client_id=my_client_id,
#                     client_secret=my_client_secret,
#                     username=my_username,
#                     password=my_password)


#pdb.set_trace()
#printlist(dir(reddit))
#for friend in reddit.user.friends():
#    submissions = friend.submissions.new()
#    submissions.limit = 1000
#    for submission in submissions:
#        #print(submission.url)
#        try:
#            obj = imgur.Imgur(submission.url)
#            obj.save_images('output')
#        except imgur.NotAnImgurAlbumException:
#            pass
#    raise Exception

#print(reddit.read_only)  # Output: False

#subreddit = reddit.subreddit('redditdev')
#
#print(subreddit.display_name) # Output: redditdev
#print(subreddit.title) # Output: reddit Development
#print(subreddit.description) # Output: A subreddit for discussion of ...
