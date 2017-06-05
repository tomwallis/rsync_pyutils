"""

Helper functions for rsync backup script. Requires python 3.5 or higher
 due to subprocess.run, and rsync 3.x.x or higher.

Tom Wallis

"""

import os, subprocess
from itertools import product


def check_location_exists(path, file_type):
    """
    :param path: absolute path to directory / file you want to check
    :param file_type: string: 'source' or 'dest'.
    :return: prints status to command line
    """

    if file_type != 'source' and file_type != 'dest':
        raise ValueError('Specify source or dest type')

    if os.path.exists(path):
        valid = True
        print('Found {} location {}'.format(file_type, path))
    else:
        valid = False
        print('Couldn\'t find {} location {} !!'.format(file_type, path))

    return valid


def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


def valid_locations(path_list, file_type):
    """
    Return valid source / dest locations
    :param path_list: list of paths to be checked.
    :param file_type: 'source' or 'dest'
    :return: a list containing valid paths
    """

    valid_list = []
    for path in path_list:
        status = check_location_exists(path, file_type)
        if status:
            valid_list.append(path)

    # summarise valid paths in console:
    print('Found {} valid {}s'.format(len(valid_list), file_type))

    return valid_list


def backup(source, dest):
    """
    The main backup function, using rsync. I use the following rsync options:

    -a = archive mode. Do recursive backup, preserving links and permissions
    -H = preserve hard-linked files.
    -X = preserve extended attributes. Requires rsync v 3.x.x
        (update via homebrew if required).
    -A = preserve acls (
    -h = human-readable numbers.
    -vv = double verbosity of output.
    --no-whole-file = ensure that delta (incremental) update is used even for
        local transfers.
    --delete = delete extraeneous files from the destination directory.
        old files in the library won't be kept on the backup.

    :param source: full path to source
    :param dest: full path to dest
    :return:
    """

    # source = source + '/'  # add trailing slash to not duplicate parent dir.

    # do a dry run, have user confirm:
    print('\nDry-run of backup {} to {} ...'.format(source, dest))
    subprocess.run('rsync -aHXAhvv --no-whole-file --delete --dry-run {} {}'.
                   format(source, dest), shell=True)

    answer = []
    while answer != 'y' and answer != 'n':
        answer = input('Do you want to proceed with real backup? [y / n]')

    if answer == 'y':
        print('\nBacking up {} to {} ...'.format(source, dest))
        subprocess.run('rsync -aHXAhvv --no-whole-file --delete {} {}'.
                       format(source, dest), shell=True)
    else:
        print('\nYou decided not to proceed!')


def backup_loop(valid_sources, valid_dests):
    for dest, source in product(valid_dests, valid_sources):
        backup(source, dest)


