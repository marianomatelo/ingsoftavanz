#!/usr/bin/python
# -*- coding: utf-8 -*-
### IMPORT LIBRARIES ###
import os, sys
from engine.DataManager import DataManager
import xgboost as xgb
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class Forecaster(object):
	'''
	Forecaster Class used to Calibrate and generates a Forecast using a predictive Model
	'''

	def run_regression(self, train, test, output_table, model):
		'''
		Generates a Forecast using input variables from data_vars for each Target
		:param target: Forecast for a specific target
		:param data_vars: input table containing the future values for the required variables
		:param output_table: name of the output table used to save the Forecast
		'''

		### BUILD MODEL ###
		try:

			if model == 'XGBoost':
				'''Creates instance of XGBoost Regressor with Tunned parameters'''
				model = xgb.XGBRegressor(max_depth=8, gamma=0, min_child_weight=1,
											 max_delta_step=0, subsample=0.8,
											 colsample_bytree=0.8, n_jobs=-1,
											 eta=0.1, objective='reg:linear', booster='gbtree')

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			raise Exception('Error Building Model: ', str(e) + ' in line: ' + str(exc_tb.tb_lineno))

		### TRAIN MODEL ###
		trained_model = self.train_data(train, model)

		### MAKE TRAIN PREDICTION ###
		train['predicted'] = self.forecast_data(train, trained_model)
		train['train'] = 1

		### MAKE TEST PREDICTION ###
		test['predicted'] = self.forecast_data(test, trained_model)
		test['train'] = 0

		### SAVE PREDICTION ###
		self.save_forecast(train, test, output_table)


	def train_data(self, data, model):
		'''
		Trains the predictive Model with the input data
		:param data: dataframe containing the historic input data and variables
		:param model: predictive model to train
		:return: a trained predictive model ready to generate a Forecast
		'''

		try:
			return model.fit(data.iloc[:, 3:], data['target'])

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			raise Exception('Error Training Model: ', str(e) + ' in line: ' + str(exc_tb.tb_lineno))


	def forecast_data(self, data, trained_model):
		'''
		Generate forecast with trained model
		:param trained_model: predictive trained model
		:param data_vars: dataframe containing the future variables
		:return: dataframe with predicted forecast
		'''
		try:
			data.drop(['target'], axis=1, inplace=True)
			return trained_model.predict(data.iloc[:, 2:])

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			raise Exception('Error Making Forecast: ', str(e) + ' in line: ' + str(exc_tb.tb_lineno))


	def save_forecast(self, train, test, output_table):
		'''
		Saves the Forecast to a Database table
		:param forecast: series containing the prediction
		:param target: target of the prediction
		:param output_table: name of the output table to save the prediction
		:param dates: list of dates of each day of the prediction
		:return:
		'''
		try:
			print('================================================')
			print('                 SAVING RESULTS                 ')
			print('================================================')

			### STARTS DB CONNECTION ###
			dm = DataManager()

			dm.dao.run_query('DROP TABLE IF EXISTS {}'.format(output_table))

			'''Saves the prediction results dataframe into the output table in the database'''
			dm.dao.upload_from_dataframe(train, output_table, if_exists='append')
			dm.dao.upload_from_dataframe(test, output_table, if_exists='append')

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			raise Exception('Error Saving Forecast: ', str(e) + ' in line: ' + str(exc_tb.tb_lineno))