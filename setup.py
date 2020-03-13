import os

from setuptools import setup, find_packages
#import subprocess

#import versioneer


here = os.path.dirname(__file__)

with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = [
        l.strip() for l in f.readlines()
        if not l.strip().startswith('#')
    ]

# Build our js and css files before packaging

#subprocess.check_call(['npm', 'install'])
#subprocess.check_call(['npm', 'run', 'webpack'])

setup(
    name='cdsbuilder',
    version='0.0.1', #versioneer.get_version(),
    #cmdclass=versioneer.get_cmdclass(),
    python_requires='>=3.6',
    author='Ideonate',
    author_email='dan@ideonate.com',
    license='BSD',
    url='https://ideonate.com/',
    # this should be a whitespace separated string of keywords, not a list
    keywords="containds jupyterhub",
    description="builder service as part of containds live",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
)
