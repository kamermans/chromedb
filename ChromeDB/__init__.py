import os
import sqlite3
import win32crypt
import sys
import re
from urlparse import urlparse

class ChromeDB:
    db_path = ''
    database = []

    def __init__(self):
        self.db_path = self.getDbPath()
        self.parseDb(self.db_path)

    def getDbPath(self):
        try:
            return sys.argv[1]
        except IndexError:
            return os.getenv('USERPROFILE')+'\AppData\Local\Google\Chrome\User Data\Default\Login Data'

    def parseDb(self, db_path):
        
        # Connect to the Database
        try:
            print '[+] Opening ' + db_path
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
        except Exception, e:
            print '[-] %s' % (e) 
            sys.exit(1)

        # Get the results
        try:
            result = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        except Exception, e:
            print '[-] %s' % (e)
            sys.exit(1)

        for row in result:
            # Decrypt the Password
            try:
                password = win32crypt.CryptUnprotectData(row[2], None, None, None, 0)[1]
            except Exception, e:
                print '[-] %s' % (e)
                pass
            
            if password:
                try:
                    domain = urlparse(row[0]).netloc
                    root_domain = re.sub('^(www\.|m\.)', '', domain)
                except:
                    domain = ''
                    root_domain = ''

                self.database.append({
                    'url': row[0],
                    'domain': domain,
                    'root_domain': root_domain,
                    'username': row[1],
                    'password': password
                })

        conn.close()
        if len(self.database) < 1:
            print '[-] No results returned from query'
            sys.exit(0)
        else:
            print "Found %s results" % (len(self.database))
