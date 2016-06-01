from ChromeDB import ChromeDB
from pprint import pprint
from getpass import getpass

db = ChromeDB()

print 'After you enter your password twice, all domain using that password will be displayed:'
password = getpass(prompt='Enter password: ')
password2 = getpass(prompt='Confirm password: ')

if password != password2:
    print "Error: passwords do not match!"
    exit(1)

domains = [x['root_domain'] for x in db.database if x['password'] == password]

clean_domains = [];
for domain in domains:
    if domain == '':
        continue

    if domain not in clean_domains:
        clean_domains.append(domain)

clean_domains = sorted(clean_domains)

for domain in clean_domains:
    print domain
