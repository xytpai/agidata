import subprocess
from setuptools import setup

subprocess.check_call(['pip install -r requirements.txt'], shell=True)


setup(
    name='agidata',
    version='0.0.0',
    packages=['agidata'],
    include_package_data=True,
)
