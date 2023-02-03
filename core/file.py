from zipfile import ZipFile
from json    import load, dump

from os      import system, makedirs, listdir
from shutil  import rmtree

from configparser import ConfigParser

config = ConfigParser()



def unZip (path, extract) :
	with ZipFile(path, 'r') as file :
		file.extractall(extract)


def loadFromJSON (path) :
	with open(path, 'r', encoding='utf8') as file :
		return load(file)


def writeToJSON (path, content) :
	with open(path, 'w', encoding='utf8') as file :
		return dump(content, file, ensure_ascii=1, indent=4)


def loadFromINI (path) :
	config.read(path)
	return config


def newFolder (path) :
	try : makedirs(path)
	except FileExistsError : pass


def deleteFolder (path) :
	rmtree(path)


def filesAndFolders (path) :
	return listdir(path)