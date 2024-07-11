import os
from stat import S_ISREG, ST_MTIME, ST_MODE, ST_SIZE

from .log import LOG

def read_stripped_lines(filename):
    """Read a file and return a list of stripped lines.

    Args:
        filename (str): path to file to read.

    Returns:
        (list) list of lines stripped from leading and ending white chars.
    """
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                yield line


def read_dict(filename, div='='):
    """Read file into dict.

    A file containing:
        foo = bar
        baz = bog

    results in a dict
    {
        'foo': 'bar',
        'baz': 'bog'
    }

    Args:
        filename (str):   path to file
        div (str): deviders between dict keys and values

    Returns:
        (dict) generated dictionary
    """
    d = {}
    with open(filename, 'r') as f:
        for line in f:
            key, val = line.split(div)
            d[key.strip()] = val.strip()
    return d


def mb_to_bytes(size):
    """Takes a size in MB and returns the number of bytes.

    Args:
        size(int/float): size in Mega Bytes

    Returns:
        (int/float) size in bytes
    """
    return size * 1024 * 1024


def _get_cache_entries(directory):
    """Get information tuple for all regular files in directory.

    Args:
        directory (str): path to directory to check

    Returns:
        (tuple) (modification time, size, filepath)
    """
    entries = (os.path.join(directory, fn) for fn in os.listdir(directory))
    entries = ((os.stat(path), path) for path in entries)

    # leave only regular files, insert modification date
    return ((stat[ST_MTIME], stat[ST_SIZE], path)
            for stat, path in entries if S_ISREG(stat[ST_MODE]))


def _delete_oldest(entries, bytes_needed):
    """Delete files with oldest modification date until space is freed.

    Args:
        entries (tuple): file + file stats tuple
        bytes_needed (int): disk space that needs to be freed

    Returns:
        (list) all removed paths
    """
    deleted_files = []
    space_freed = 0
    for moddate, fsize, path in sorted(entries):
        try:
            os.remove(path)
            space_freed += fsize
            deleted_files.append(path)
        except Exception:
            pass

        if space_freed > bytes_needed:
            break  # deleted enough!

    return deleted_files

def ensure_directory_exists(directory, domain=None, permissions=0o777):
    """Create a directory and give access rights to all

    Args:
        directory (str): Root directory
        domain (str): Domain. Basically a subdirectory to prevent things like
                      overlapping signal filenames.
        rights (int): Directory permissions (default is 0o777)

    Returns:
        (str) a path to the directory
    """
    if domain:
        directory = os.path.join(directory, domain)

    # Expand and normalize the path
    directory = os.path.normpath(directory)
    directory = os.path.expanduser(directory)

    if not os.path.isdir(directory):
        try:
            save = os.umask(0)
            os.makedirs(directory, permissions)
        except OSError:
            LOG.warning("Failed to create: " + directory)
        finally:
            os.umask(save)

    return directory


def create_file(filename):
    """Create the file filename and create any directories needed

    Args:
        filename: Path to the file to be created
    """
    ensure_directory_exists(os.path.dirname(filename), permissions=0o775)
    with open(filename, 'w') as f:
        f.write('')
