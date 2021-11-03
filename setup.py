import os
pjoin = os.path.join

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

__version__ = None
exec(open(pjoin(here,'cdsdashboards/version.py')).read()) # Load __version__

install_requires = [
    'tornado>=6.0.4', # Mainly for jhsingle-native-proxy but best to keep consistent
    'traitlets',
    'jupyterhub>=1.0.0',
    'alembic',
    'pluggy'
]

extras_require = {
    'user': [
        'jhsingle-native-proxy>=0.7.6',
        'plotlydash-tornado-cmd>=0.0.6',
        'bokeh-root-cmd>=0.1.2',
        'rshiny-server-cmd>=0.0.2'
    ],
    'sudospawner': [
        "sudospawner>=0.5.2"
    ]
}

with open(pjoin(here, 'README.md'), encoding="utf8") as f:
    readme = f.read().replace('./docs/_static/screenshots/', 'https://github.com/ideonate/cdsdashboards/raw/master/docs/_static/screenshots/')

setup_metadata=dict(
    version=__version__,
    python_requires='>=3.6',
    author='Ideonate',
    author_email='dan@containds.com',
    license='BSD',
    url='https://github.com/ideonate/cdsdashboards',
    # this should be a whitespace separated string of keywords, not a list
    keywords="containds jupyterhub",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    project_urls={
        'Source': 'https://github.com/ideonate/cdsdashboards',
        'Tracker': 'https://github.com/ideonate/cdsdashboards/issues'
    },
    long_description=readme,
    long_description_content_type='text/markdown',
    platforms="Linux, Mac OS X",
    description="ContainDS Dashboards extension for JupyterHub"
    )

# Data files e.g. templates and static js

share_cdsdashboards = pjoin(here, 'share', 'cdsdashboards')

def get_data_files():
    """Get data files in share/cdsdashboards"""

    data_files = []
    ntrim = len(here + os.path.sep)

    for (d, _, filenames) in os.walk(share_cdsdashboards):
        data_files.append((d[ntrim:], [pjoin(d, f)[ntrim:] for f in filenames]))
    return data_files

def get_package_data():
    """Get package data

    (mostly alembic config)
    """
    package_data = {}
    package_data['cdsdashboards'] = ['alembic.ini', 'cdsalembic/*', 'cdsalembic/versions/*']
    return package_data


setup_metadata.update(dict(
    name='cdsdashboards',
    packages=find_packages(),
    package_data=get_package_data(),
    data_files=get_data_files(),
    install_requires=install_requires,
    extras_require=extras_require
))

setup_metadata.update(dict(
    entry_points={
        'console_scripts': ['cds_sudospawner=cdsdashboards.hubextension.spawners.variablesudospawner:mediator']
    }))

setup(
    **setup_metadata
)
