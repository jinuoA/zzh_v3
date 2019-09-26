
from setuptools import setup, find_packages
setup(
    name='zzh',
    version='2.0',
    packages=find_packages(),
    include_package_data = True,
    entry_points={'scrapy':['settings=zzh.settings']},
)