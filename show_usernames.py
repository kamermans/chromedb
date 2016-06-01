from ChromeDB import ChromeDB
from pprint import pprint

db = ChromeDB()

usernames = {}
passwords = {}
for item in db.database:
    if item['username'] not in usernames:
        usernames[item['username']] = 1
    else:
        usernames[item['username']] += 1

pprint(usernames)
