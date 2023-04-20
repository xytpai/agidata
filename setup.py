import subprocess
from setuptools import setup

subprocess.check_call(['pip install -r requirements.txt'], shell=True)


setup(
    name='datasets',
    version='0.0.0',
    packages=['cut'],
    include_package_data=True,
)
