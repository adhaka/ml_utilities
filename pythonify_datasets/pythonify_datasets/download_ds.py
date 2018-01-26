__author__ = 'Akash'
__license__ = 'GPL'
__credits__ = 'Aalto University'


import gzip 
import os, sys
import numpy as np 
# import urllib2
import requests
import pickle
import helper_processing as hp
import zipfile
from Dataset import Dataset
import pandas as pd



# dictionary to map names of datasets with their urls.
DATASETS_URL = {}
DATASETS_URL['snelsons'] = 'http://www.gatsby.ucl.ac.uk/~snelson/SPGP_dist.zip'
DATASETS_URL['leukemia'] = ''
DATASETS_URL['moamoa'] = ''
DATASETS_URL['co2'] = ''
DATASETS_URL['faithful'] = ''
DATASETS_URL['coalmining'] = ''
DATASETS_URL['household'] = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip'


DIR_DOWNLOAD = 'raw_datasets/' 
DIR_EXPAND = 'expand_datasets/'
DIR_PICKLED = 'pickled_datasets/'

DIR_ALL = [DIR_DOWNLOAD, DIR_EXPAND, DIR_PICKLED]

cwd = os.path.abspath(os.path.dirname(__file__))
DIR_PICKLED_FULL = os.path.join(cwd, DIR_PICKLED)
DIR_DOWNLOAD_FULL = os.path.join(cwd, DIR_DOWNLOAD)
DIR_EXPAND_FULL = os.path.join(cwd, DIR_EXPAND)

DIR_ALL_FULL = [DIR_DOWNLOAD_FULL, DIR_EXPAND_FULL, DIR_PICKLED_FULL]



def _downloader(weburl, filename=''):
	if filename == '':
		filename = str(weburl).split('/')[-1]

	r = requests.get(weburl, stream=True)
	with open(filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)

	print "Write Successful!!"
	return filename



def download_snelson(weburl=''):
	if weburl == '':
		weburl = DATASETS_URL['snelsons']

	target_filename = str(weburl).split('/')[-1]
	cwd = os.getcwd()

	raw_file_path = os.path.join(DIR_DOWNLOAD_FULL, target_filename)
	filename = _downloader(weburl, raw_file_path)
	return filename



def save_snelson(weburl):
	''' download the file from the internet, process it  and save it in a pickle file. '''
	filename = download_snelson(weburl)
	ext = hp.get_extension(filename)

	if not os.path.isdir(str(cwd+DIR_EXPAND)):
		os.mkdir(str(cwd+DIR_EXPAND))
		print("Making directory for extraction")

	# if ext == 'zip':
	snelson_zip = zipfile.ZipFile(filename, 'r')
	snelson_extracted_files = snelson_zip.extractall(str(cwd+DIR_EXPAND))
	namelist = snelson_zip.namelist()

	dir_snelson = os.path.join(DIR_EXPAND_FULL, namelist[0])
	train_x = np.loadtxt(os.path.join(dir_snelson, 'train_inputs'))
	# train_x = np.loadtxt(DIR_EXPAND_FULL + namelist[0] + 'train_inputs')
	train_y = np.loadtxt(os.path.join(dir_snelson, 'train_outputs'))

	# test_x = np.loadtxt(cwd + '/' + namelist[0] + 'test_inputs')
	test_x = np.loadtxt(os.path.join(dir_snelson, 'test_inputs'))

	Snelson_DS = Dataset(train_x, train_y, test_x, name='snelson1d', 
		description='small dataset for GP- the popular snelson dataset', weburl=DATASETS_URL['snelsons'])

	Snelson_DS.savemat()
	print(DIR_PICKLED_FULL)
	exit()
	Snelson_DS.picklify(dirpath=DIR_PICKLED_FULL)
	return Snelson_DS

	# print(train_y.shape)
	# test_y = np.loadtxt(cwd + namelist[0] + 'test')



def load_snelson(weburl):
	'''check if pickle is there, otherwise download from the internet and process it. '''
	# making the path platform independent
	target_path = os.path.join(DIR_PICKLED_FULL, 'snelson1d.p')
	Snelson = save_snelson(weburl)
	print(target_path)
	# exit()
	try:
		Snelson = pickle.load(open(target_path, 'rb'))
		return Snelson
	except :
		try:
			Snelson = save_snelson(weburl)
			return Snelson
		except:
			print("Something went wrong")



def download_leukemia(weburl):
	pass


def save_leukemia(weburl=''):
	''' download the file from the internet, process it  and save it in a pickle file. '''
	filename = cwd + DIR_EXPAND + 'leukemia.txt'
	target_filename = os.path.join(DIR_EXPAND_FULL, 'leukemia.txt')
	le_df = pd.read_table(filename, sep=' ', header=None, names=['time', 'cens', 'xcoord', 'ycoord', 'age', 'sex', 'wbc', 'tpi', 'district'])
	le_np = le_df.as_matrix()
	Y = le_np[:,0]
	X = le_np[:,1:]
	Leukemia = Dataset(X_train=X, Y_train=Y, D=le_df, name='leukemia', filename='leukemia.txt', description='dataset for leukemia-survival analysis')
	Leukemia.picklify()
	# Leukemia.savemat()
	return Leukemia



def load_leukemia(weburl=''):
	'''check if pickle is there otherwise download from the internet and process it. '''
	target_path = str(cwd + DIR_PICKLED + 'leukemia.p')
	try:
		Leukemia = pickle.load(open(target_path, 'rb'))
		return Leukemia
	except:
		try:
			Leukemia = save_leukemia(weburl)
			return Leukemia
		except:
			print("Something went wrong ... ")



def download_faithful(weburl=''):
	pass



def save_faithful(weburl=''):
	filename = str(DIR_EXPAND_FULL)+ 'faithful.txt'
	fa_df = pd.read_table(filename, sep=' ', header=None, names=['eruptiontime', 'waitingtime'])
	fa_np = fa_df.as_matrix()
	Y = fa_np[:,1]
	X = fa_np[:,0]
	Faithful = Dataset(X_train=X, Y_train=Y, D=fa_df, name='faithful', description='dataset of the old faithful geyser \
		eruption. First col is eruption time, and second is waiting time')
	Faithful.picklify()
	Faithful.savemat()
	return Faithful


def load_faithful(weburl=''):
	# target_path = str(cwd + DIR_PICKLED + 'faithful.p')
	target_path = os.path.join(DIR_PICKLED_FULL, 'faithful.p')
	try:
		Faithful = pickle.load(open(target_path, 'rb'))
		return Faithful
	except:
		try:
			Faithful = save_faithful(weburl)
			return Faithful
		except:
			print("Something went wrong.")




def download_power_consumption(weburl=''):
	if weburl == '':
		weburl = DATASETS_URL['household']

	target_filename = str(weburl).split('/')[-1]
	cwd = os.getcwd()

	raw_file_path = str(cwd) + DIR_DOWNLOAD + target_filename
	filename = _downloader(weburl, raw_file_path)
	return filename



def save_power_consumption(weburl='', saveasDF=True):
	''' saveasDF parameter tells if we want to save it as pandas dataframe. '''
	filename = download_power_consumption(weburl)
	ext = hp.get_extension(filename)

	household_zip = zipfile.ZipFile(filename, 'r')
	if not os.path.isdir(DIR_EXPAND_FULL):
		os.mkdir(DIR_EXPAND_FULL)
		print("Making directory for extraction")


	household_extract_files = household_zip.extractall(str(cwd+DIR_EXPAND))
	file_txt_name = 'household_power_consumption.txt'
	filename =  cwd + DIR_EXPAND + file_txt_name
	HP_DF = pd.read_table(filename, sep=';', header=[0])
	HP_np = HP_DF.as_matrix() 
	Y = HP_np[:,-3:]
	X = HP_np[:,:-3]

	HPC = Dataset(X_train=X, Y_train=Y, D=HP_DF, name="hpc", filename=file_txt_name,
		description=' dataset of power meter readings of UK households', weburl=DATASETS_URL['household'])


	HPC.picklify()
	# HPC.savemat()

	return HPC
	# HousePowerCons = Dataset(train_x)



def load_power_consumption(weburl=''):

	# target_path = str(cwd + DIR_PICKLED + 'hpc.p')
	target_path = os.path.join(DIR_PICKLED_FULL, 'hpc.p')
	try:
		HousePowerCons = pickle.load(open(target_path, 'rb'))
		return HousePowerCons
	except:
		try:
			HousePowerCons = save_power_consumption(DATASETS_URL['household'])
			return HousePowerCons
		except:
			print("Oops, Something went wrong ...")




def download_kin40k(weburl=''):
	pass


def load_kin40k(weburl=''):
	pass


def save_kin40k(weburl=''):
	pass




if __name__ == '__main__':

	for d in DIR_ALL:
		file_full = os.path.join(cwd, d)
		print(file_full)
		# exit()
		if not os.path.exists(file_full):
			try:
				os.mkdir(file_full)
			except:
				print("Check your permissions ...")
				


	Snelson = load_snelson(DATASETS_URL['snelsons'])
	print Snelson
	# Leukemia = load_leukemia(DATASETS_URL['leukemia'])
	# print Leukemia
	# Faithful = load_faithful(DATASETS_URL['faithful'])
	# print Faithful
	# # HousePowerCons = load_power_consumption()
	# print HousePowerCons



