import os

from setuptools import setup

here = os.path.dirname(__file__)

with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = [
        l.strip() for l in f.readlines()
        if not l.strip().startswith('#')
    ]

setup(
    name='cdsdashboards',
    packages=['cdsdashboards'],
    version='0.0.3',
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
    platforms="Linux, Mac OS X",
    description="ContainDS Dashboards extension for JupyterHub",
    include_package_data=True,
    install_requires=requirements,
)
