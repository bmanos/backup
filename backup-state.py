# Get Veeam backup email state
# and insert result to database
# Author       : Bairaktaris Emmanuel
# Date         : December 4, 2019
# Modified     : February 28, 2020
# Link         : http://repairmypc.net

# Import libraries
from imapclient import IMAPClient
import uuid
import datetime
import time
import os

# Delete sql files before create the new ones
# endor
if os.path.exists('C:/tools/backup/data/export_backup_state_endor.sql'):
  os.remove('C:/tools/backup/data/export_backup_state_endor.sql')
  print('File deleted')
else:
  print('File does not exist')
# naboo
if os.path.exists('C:/tools/backup/data/export_backup_state_naboo.sql'):
  os.remove('C:/tools/backup/data/export_backup_state_naboo.sql')
  print('File deleted')
else:
  print('File does not exist')

time.sleep(5)

# Get credentials
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')

# Start get mail from endor
# Get yesterday date
today = datetime.date.today()
mydate = today - datetime.timedelta(days = 1)

# Connect to imap mail server
server = IMAPClient('mail.server.gr', ssl=False, port=143)
server.login(db_user, db_pass)

# Select mail folder to be parsed with several options like subject, sender etc..
select_backup = server.select_folder('#Public.#Support.Backup_support')
print('%d messages in Backup folder' % select_backup[b'EXISTS'])

messages = server.search(['SUBJECT', 'endor', 'FROM', 'm@m.gr'])
print("%d messages from our backup system" % len(messages))

# loop through mail folder and display result coresponding to choosen options
for msgid, data in server.fetch(messages, ['ENVELOPE']).items():
     envelope = data[b'ENVELOPE']
     print('ID #%d: "%s" received %s' % (msgid, envelope.subject.decode(), envelope.date))

# Get message subject
endorsubj = envelope.subject.decode()

# Insert results into database by creating sql query file

if '[Success]' in endorsubj:
    f = open('C:/tools/backup/data/' + str(datetime.date.today()) + '_backup_state_endor_' + str(uuid.uuid1()) + '.sql', 'w') # the file name contains the current date of execution and unique id number(uuid)
    f.write('Insert into papback (Day, Result, Reason) VALUES (' + '\'' + str(mydate) + '\'' + ' ,' + '\'' + 'True' + '\'' + ' ,' + '\'' + envelope.subject.decode() +'\'' ')')
    f.close()
    f = open('C:/tools/backup/data/export_backup_state_endor.sql', 'w')
    f.write('Insert into papback (Day, Result, Reason) VALUES (' + '\'' + str(mydate) + '\'' + ' ,' + '\'' + 'True' + '\'' + ' ,' + '\'' + envelope.subject.decode() +'\'' ')')
    f.close()
    print("Success")
elif '[Warning]' in endorsubj:
    f = open('C:/tools/backup/data/' + str(datetime.date.today()) + '_backup_state_endor_' + str(uuid.uuid1()) + '.sql', 'w') # the file name contains the current date of execution and unique id number(uuid)
    f.write('Insert into papback (Day, Result, Reason) VALUES (' + '\'' + str(mydate) + '\'' + ' ,' + '\'' + 'True' + '\'' + ' ,' + '\'' + envelope.subject.decode() +'\'' ')')
    f.close()
    f = open('C:/tools/backup/data/export_backup_state_endor.sql', 'w')
    f.write('Insert into papback (Day, Result, Reason) VALUES (' + '\'' + str(mydate) + '\'' + ' ,' + '\'' + 'True' + '\'' + ' ,' + '\'' + envelope.subject.decode() +'\'' ')')
    f.close()
    print("Warning")
elif '[Failed]' in endorsubj:
    f = open('C:/tools/backup/data/ERROR-export_backup_state_endor.sql', 'a')
    f.write(str(datetime.datetime.now()) + '\n')
    f.write("Backup error" + '\n')
    f.write('%d messages in Backup folder' % select_backup[b'EXISTS'] + '\n')
    f.write("%d messages from our backup system" % len(messages) + '\n')
    f.close()
    f = open('C:/tools/backup/data/export_backup_state_endor.sql', 'w')
    f.write('Insert into papback (Day, Result, Reason) VALUES (' + '\'' + str(mydate) + '\'' + ' ,' + '\'' + 'False' + '\'' + ' ,' + '\'' + envelope.subject.decode() +'\'' ')')
    f.close()
    print("Failed")

# close server connection
server.logout()     
# End getting mail from endor
time.sleep(5)

# Start get mail from naboo
# Get yesterday date
today = datetime.date.today()
mydate = today - datetime.timedelta(days = 1)

# Connect to imap mail server
server = IMAPClient('mail.server.gr', ssl=False, port=143)
server.login(db_user, db_pass)

# Select mail folder to be parsed with several options like subject, sender etc..
select_backup = server.select_folder('#Public.#Support.Backup_support')
print('%d messages in Backup folder' % select_backup[b'EXISTS'])

messages = server.search(['SUBJECT', 'naboo', 'FROM', 'm@m.gr'])
print("%d messages from our backup system" % len(messages))

# loop through mail folder and display result coresponding to choosen options
for msgid, data in server.fetch(messages, ['ENVELOPE']).items():
     envelope = data[b'ENVELOPE']
     print('ID #%d: "%s" received %s' % (msgid, envelope.subject.decode(), envelope.date))

# Get message subject
naboosubj = envelope.subject.decode()

# Insert results into database by creating sql query file

if '[Success]' in naboosubj:
    f = open('C:/tools/backup/data/' + str(datetime.date.today()) + '_backup_state_naboo_' + str(uuid.uuid1()) + '.sql', 'w') # the file name contains the current date of execution and unique id number(uuid)
    f.write('Insert into papback (Day, Result, Reason) VALUES (' + '\'' + str(mydate) + '\'' + ' ,' + '\'' + 'True' + '\'' + ' ,' + '\'' + envelope.subject.decode() +'\'' ')')
    f.close()
    f = open('C:/tools/backup/data/export_backup_state_naboo.sql', 'w')
    f.write('Insert into papback (Day, Result, Reason) VALUES (' + '\'' + str(mydate) + '\'' + ' ,' + '\'' + 'True' + '\'' + ' ,' + '\'' + envelope.subject.decode() +'\'' ')')
    f.close()
    print("Success")
elif '[Warning]' in naboosubj:
    f = open('C:/tools/backup/data/' + str(datetime.date.today()) + '_backup_state_naboo_' + str(uuid.uuid1()) + '.sql', 'w') # the file name contains the current date of execution and unique id number(uuid)
    f.write('Insert into papback (Day, Result, Reason) VALUES (' + '\'' + str(mydate) + '\'' + ' ,' + '\'' + 'True' + '\'' + ' ,' + '\'' + envelope.subject.decode() +'\'' ')')
    f.close()
    f = open('C:/tools/backup/data/export_backup_state_naboo.sql', 'w')
    f.write('Insert into papback (Day, Result, Reason) VALUES (' + '\'' + str(mydate) + '\'' + ' ,' + '\'' + 'True' + '\'' + ' ,' + '\'' + envelope.subject.decode() +'\'' ')')
    f.close()
    print("Warning")
elif '[Failed]' in naboosubj:
    f = open('C:/tools/backup/data/ERROR-export_backup_state_naboo.sql', 'a')
    f.write(str(datetime.datetime.now()) + '\n')
    f.write("Backup error" + '\n')
    f.write('%d messages in Backup folder' % select_backup[b'EXISTS'] + '\n')
    f.write("%d messages from our backup system" % len(messages) + '\n')
    f.close()
    f = open('C:/tools/backup/data/export_backup_state_naboo.sql', 'w')
    f.write('Insert into papback (Day, Result, Reason) VALUES (' + '\'' + str(mydate) + '\'' + ' ,' + '\'' + 'False' + '\'' + ' ,' + '\'' + envelope.subject.decode() +'\'' ')')
    f.close()
    print("Failed")

# close server connection
server.logout()     
# End getting mail from naboo
time.sleep(5)
