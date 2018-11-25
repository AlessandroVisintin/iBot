import os
import sys
import subprocess
from sys import stdout as so

# Constants
DRIVER_URL = "https://chromedriver.storage.googleapis.com/2.42/"
DRIVER_NAME = "chromedriver_win32.zip"
UNZIP_NAME = "chromedriver.exe"

def _install(pkg):
	"""
	Install a package.

	:type pkg: string
	:param pkg: Name of package to be installed
	"""
	so.write("Trying to install {}...".format(pkg))
	subprocess.call([sys.executable, "-m", "pip", "install", pkg])
	so.write("[done]\n")

def setup():
	"""
	Intialize the environment for iBot.
	"""

	print("Initializing environment for iBot...")

	so.write("Checking selenium...")
	try:
		import selenium
		so.write('[ok]\n')
	except ImportError, e:
		so.write("[not found]\n")
		_install('selenium')

	so.write("Checking driver for selenium...")
	if not os.path.isfile(UNZIP_NAME):
		so.write("[not found]\n")

		so.write("Checking zipfile...")
		try:
			import zipfile
			so.write('[ok]\n')
		except ImportError, e:
			so.write("[not found]\n")
			_install('zipfile')
			import zipfile

		so.write("Checking wget...")
		try:
			import wget
			so.write('[ok]\n')
		except ImportError, e:
			so.write("[not found]\n")
			_install('wget')
			import wget

		so.write('Downloading {}...'.format(DRIVER_URL+DRIVER_NAME))
		wget.download(DRIVER_URL+DRIVER_NAME, DRIVER_NAME)
		so.write("[done]\n")
		so.write('Unzipping {}...'.format(DRIVER_NAME))
		r = zipfile.ZipFile(DRIVER_NAME, 'r')
		r.extractall()
		r.close()
		so.write("[done]\n")
		os.remove(DRIVER_NAME)
	else:
		so.write("[ok]\n")

if __name__ == '__main__':
	setup()