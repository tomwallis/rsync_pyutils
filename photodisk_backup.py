"""
This file contains a script to backup from one external
disk to another using rsync. It's intended to back up Tom's family photo
library. The source and destination paths are hand coded.

Run from command line as

python photodisk_backup.py

Tom Wallis wrote it 4.06.2017
"""

import funs, os

# list of possible sources and destinations:
source_list = [os.path.expanduser('~/Dropbox/Keepass'),
               '/Volumes/primary_backup']
dest_list = ['/Volumes/backup_1',
             '/Volumes/backup_2']

# get valid locations:
valid_sources = funs.valid_locations(source_list, 'source')
valid_dests = funs.valid_locations(dest_list, 'dest')

# loop over valid sources and destinations
funs.backup_loop(valid_sources, valid_dests)







