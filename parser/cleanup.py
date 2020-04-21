import os


def cleanit(path):
	os.system('echo Starting clean up of new directory')
	os.system('rm -v ' + path + '*.json')
