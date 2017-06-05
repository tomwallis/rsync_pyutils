"""

A simple test script for the backup program. Checks that a directory
can be incrementally backed up using rsync.

"""


import funs, os

source_dir = os.path.join(os.getcwd(), 'test', 'source')
dest_dir = os.path.join(os.getcwd(), 'test', 'dest')
recovered_dir = os.path.join(os.getcwd(), 'test', 'recovered')

# create directories for testing output:
funs.ensure_dir(source_dir)
funs.ensure_dir(dest_dir)
funs.ensure_dir(recovered_dir)

# make a test file:
orig_fname = os.path.join(source_dir, 'backup_test_file.txt')
if os.path.exists(orig_fname):
    f = open(orig_fname, mode='w')
else:
    f = open(orig_fname, mode='x')

f.write('This is a test file! \n')
f.close()


# list of possible sources and destinations:
source_list = [source_dir,
               os.path.join(os.getcwd(), 'invalid_source')]
dest_list = [dest_dir,
             os.path.join(os.getcwd(), 'invalid_dest')]


# get valid locations:
valid_sources = funs.valid_locations(source_list, 'source')
valid_dests = funs.valid_locations(dest_list, 'dest')

funs.backup_loop(valid_sources, valid_dests)

print("Append file, re-do backup.")
f = open(orig_fname, mode='a')
f.write('new data!\n')
f.close()

funs.backup_loop(valid_sources, valid_dests)

print("Check that nothing changes when the file is the same:")

funs.backup_loop(valid_sources, valid_dests)
