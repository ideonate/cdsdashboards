"""Get the data files for this package."""


def get_data_files():
    """Walk up until we find share/cdsdashboards"""
    import sys
    from os.path import join, abspath, dirname, exists, split

    path = abspath(dirname(__file__))
    starting_points = [path]
    if not path.startswith(sys.prefix):
        starting_points.append(sys.prefix)
    for path in starting_points:
        # walk up, looking for prefix/share/cdsdashboards
        while path != '/':
            share_cdsdashboards = join(path, 'share', 'cdsdashboards')
            static = join(share_cdsdashboards, 'static')
            if all(exists(join(static, f)) for f in ['js', 'css']):
                return share_cdsdashboards
            path, _ = split(path)
    # didn't find it, give up
    return ''


# Package managers can just override this with the appropriate constant
DATA_FILES_PATH = get_data_files()
