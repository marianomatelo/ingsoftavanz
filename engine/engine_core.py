#!/usr/bin/python
# -*- coding: utf-8 -*-
### IMPORT LIBRARIES ###
import sys
import pandas as pd
from tqdm import tqdm
from datetime import timedelta, datetime
from multiprocessing import Pool, cpu_count
from sklearn.model_selection import train_test_split
from engine.DataManager import DataManager
from engine.Predictor import Forecaster


def run_multithreaded_regression(run_dict):
	'''
	Runs a multithreading prediction, each instance of this method is assigned to a worker and belongs to a Target
	'''

	for key, value in run_dict.items():
		fu = key
		train = value[0]
		test = value[1]
		output_table = value[2]
		model = value[3]

	'''create instance of Forecaster Class'''
	f = Forecaster()

	'''calls make forecast method of Forecaster Class'''
	f.run_regression(train, test, output_table, model)



def run_engine(id, model, clean, scaling, training, dataset_id, dataset_problem,
			   dataset_frequency, dataset_user, run_description):
	''' 
	PREDICTION:
	- Loads future variables from database
	- Loads a trained predictive model from folder models
	- Checks calibration status from database and warns if a target requires to be calibrated
	- Runs a forecast from supplied date up to the following horizon days
	- Saves the prediction to the database
	'''

	try:
		print('================================================')
		print('               PLAYGROUND ENGINE                ')
		print('================================================')

		### SET PROBLEM TYPE ###
		if dataset_problem == 'Regression':

			'''Input table containing historic data and variables'''
			# TODO: agregar soporte variables categoricas
			input_table = 'pg_dataset_{}'.format(dataset_id)

			'''Output table'''
			output_table = 'pg_output_{}'.format(id)

			### DB CONNECTION ###
			dm = DataManager(input_table=input_table, output_table=output_table)

			### INPUT LOADING ###
			print('Downloading Input')
			df_input = dm.dao.download_from_query("SELECT * FROM {} order by date".format(input_table))

			fus = df_input['fu'].unique()

			train, test = train_test_split(df_input, test_size=int(30)/100)

			'''Create a list of Tasks to run'''
			run_list = []

			for fu in fus:

				run_list.append({fu: [pd.DataFrame(train.loc[train.fu == fu]), pd.DataFrame(test.loc[test.fu == fu]),
									output_table, model]})

			print('================================================')
			print('                STARTING ENGINE                 ')
			print('================================================')

			### PREDICTION STARTS ###
			'''Start a pool of workers to allow multithreaded prediction based on number of cpu cores'''
			pool = Pool(cpu_count())

			'''Map each free worker to a Target'''
			list(tqdm(pool.imap(run_multithreaded_regression, run_list), total=len(run_list)))

			'''Finished submiting tasks to workers'''
			pool.close()

			'''Wait for all workers to finish all tasks'''
			pool.join()

			q = '''UPDATE pg_daemon SET status = 'finished' WHERE id = {} '''.format(id)
			dm.dao.run_query(q)

			print('================================================')
			print('               PLAYGROUND FINISHED              ')
			print('================================================')

		elif dataset_problem == 'Classification':
			pass

		else:
			raise Exception(('Problem not yet supported: {}'.format(dataset_problem)))

	except Exception as e:

		q = '''UPDATE pg_daemon SET status = 'error: {}' WHERE id = {} '''.format(str(e), id)
		dm.dao.run_query(q)

		exc_type, exc_obj, exc_tb = sys.exc_info()
		raise Exception('Error: ', str(e) + ' in line: ' + str(exc_tb.tb_lineno))