import os

from setuptools import setup, find_packages

here = os.path.dirname(__file__)

with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = [
        l.strip() for l in f.readlines()
        if not l.strip().startswith('#')
    ]

setup(
    name='cdsdashboards',
    version='0.0.2',
    python_requires='>=3.6',
    author='Ideonate',
    author_email='dan@containds.com',
    license='BSD',
    url='https://containds.com/',
    # this should be a whitespace separated string of keywords, not a list
    keywords="containds jupyterhub",
    description="ContainDS Dashboards extension for JupyterHub",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
)
