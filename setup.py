import os
pjoin = os.path.join

from setuptools import setup, find_packages

here = os.path.dirname(__file__)

with open(pjoin(here, 'requirements.txt')) as f:
    requirements = [
        l.strip() for l in f.readlines()
        if not l.strip().startswith('#')
    ]

# Data files e.g. templates and static js

here = os.path.abspath(os.path.dirname(__file__))
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

with open('README.md', encoding="utf8") as f:
    readme = f.read()

setup(
    name='cdsdashboards',
    packages=find_packages(),
    package_data=get_package_data(),
    version='0.0.13',
    python_requires='>=3.6',
    author='Ideonate',
    author_email='dan@containds.com',
    license='BSD',
    url='https://containds.com/',
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
    description="ContainDS Dashboards extension for JupyterHub",
    data_files=get_data_files(),
    install_requires=requirements,
)
