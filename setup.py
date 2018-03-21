from setuptools import setup, find_packages

setup(
    name='anchorage',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        anchorage=anchorage.main:main
    ''',
)
