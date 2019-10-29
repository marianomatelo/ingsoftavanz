#!/usr/bin/python
# -*- coding: utf-8 -*-
### IMPORT LIBRARIES ###
import sys
from django.utils.timezone import datetime
from pg.models import Daemon
from engine import engine_core as ec


def run_daemon():
	'''
	'''

	try:
		oldest_run = Daemon.objects.filter(status='waiting').order_by('-sent_date')[0]

		oldest_run.run_date = datetime.today()
		oldest_run.status = 'running'
		oldest_run.save()

		### RUN MODEL ###
		try:
			ec.run_engine(oldest_run.id, oldest_run.model, oldest_run.clean, oldest_run.scaling, oldest_run.training, oldest_run.dataset_id,
						  oldest_run.problem, oldest_run.frequency, oldest_run.user, oldest_run.run_description)


		except Exception as e:
			oldest_run.run_date = datetime.today()
			oldest_run.status = 'error'
			oldest_run.save()
			exc_type, exc_obj, exc_tb = sys.exc_info()
			raise Exception('Error: ', str(e) + ' in line: ' + str(exc_tb.tb_lineno))


	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		raise Exception('Error: ', str(e) + ' in line: ' + str(exc_tb.tb_lineno))