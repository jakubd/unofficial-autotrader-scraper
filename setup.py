from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Unofficial Autotrader Scraper',
    version='0.1dev',
    packages=['unofficialautotraderscraper', ],
    entry_points={
        'console_scripts': [
            'atscrape=unofficialautotraderscraper.cliapp:stub',
        ],
    },
    include_package_data=True,
    license='The 3-Clause BSD License',
    long_description=open('README.md').read(),
    install_requires=requirements,
)
