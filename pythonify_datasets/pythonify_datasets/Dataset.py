__author__ = "Akash Kumar"
__credits__ = ["Aalto University"]
__email__ = "akash.dhaka@aalto.fi"
__license__ = "GPL MIT"


import os, sys
import numpy as np 
import pickle
import scipy
import scipy.io as sio
import pandas as pd 



SEED = 1000

DIRECTORIES = []
DIR_DOWNLOAD = 'raw_datasets/' 
TEMP_DIR = 'expand_datasets/'
DIR_PICKLED = 'pickled_datasets/'


class Dataset(object):
	''' single class to have all dataset functionality'''
	#  D represents complete train data in the form of a pandas dataframe.
	def __init__(self, X_train= None, Y_train=None, D=None,  X_test=None, Y_test=None, name='', description='', filename='', weburl=''):
		self.X = X_train
		self.Y = Y_train 
		self.X_test = X_test
		self.Y_test = Y_test
		self.D = D

		# assert self.X.shape[0] == self.Y.shape[0]
		self.name = name
		self.description = description
		self.filename = filename
		self.weburl = weburl
		self.contents = {}


	def __str__(self):
		textstr =  'Name:' + self.name + '\n' + 'File Extension:' + self.filename.split('.')[-1] +"\n" + "Dataset Info:" + str(self.description) 
		# + "\n" + "" + str(self.weburl)
		return textstr



	def sample(percent):
		n_rows = self.X.shape[0]
		ind = np.arange(n_rows)
		np.random.shuffle(ind)
		x_shuffled = self.X[ind]
		Y_shuffled = self.Y[ind]
		n_samples = abs(self.X.shape[0] * percent)
		X_sub = x_shuffled[:n_samples]
		Y_sub = Y_shuffled[:n_samples]
		return X_sub, Y_sub


	def __saveData(self):


		# self.contents = {'X': self.X, 'Y':self.Y, 'X_test': self.X_test, \
		# 			'name':self.name, 'description':self.description, 'weburl':self.weburl}

		self.contents = {'D':self.D, 'X': self.X, 'Y':self.Y, \
					'name':self.name, 'description':self.description, 'weburl':self.weburl}

		# self.contents['X'] = self.X
		# self.contents['Y'] = self.Y
		# self.contents['X_test'] = self.X_test
		# self.contents['Y_test'] = self.Y_test
		# self.contents['name'] = self.name
		# self.contents['description'] = self.description
		# self.contents['weburl'] = self.weburl
		


	def savemat(self, dirpath=''):
		self.__saveData()
		if dirpath == '':
			# dirpath = os.getcwd()
			dirpath = os.path.abspath(os.path.dirname(__file__))

		dirpath = dirpath +  DIR_PICKLED + self.name +  '.mat'   
		
		# sio.savemat( dirpath + 'dataset_' + self.name + '.mat', self.contents)
		sio.savemat(dirpath, self.contents)


	def savenpy(self):
		self.__saveData()
		# sio.


	def picklify(self, picklename='', dirpath=''):
		# revert to dataset name if picklename not given.

		print dirpath
		exit()
		if dirpath == '':
			dirpath = os.path.abspath(os.path.dirname(__file__))

		self.__saveData()
		picklename = self.name
		self.picklename = picklename + '.p'
		target_dirpath = dirpath + self.picklename
		print target_dirpath
		exit()
		pickle.dump(self.contents, open(target_dirpath, 'wb'))


	def load_dataset(self):
		pass


	def load_pickled_data(self):
		if self.picklename != None:
			try:
				dataset_unpickled = pickle.load( open(self.picklename, 'rb'))
				return dataset_unpickled
			except Exception:
				print("Dataset not pickled yet !!")



	def savenpz(self):
		pass 










