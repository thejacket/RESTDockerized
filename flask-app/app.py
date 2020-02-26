#!/usr/bin/env python
import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from celery import current_app
from celery.signals import after_task_publish
from flask import send_file
from celery import Celery
from selenium import webdriver
import json
import requests
import shutil
from worker import celery


env=os.environ
app = Flask(__name__)

@app.route('/downloadResources/<websiteUrl>', methods=['GET'])
def downloadResources(websiteUrl):
	shutil.make_archive(websiteUrl, 'zip', websiteUrl)
	return send_file(websiteUrl + '.zip')

@app.route('/textFromWebsite/<websiteUrl>', methods=['POST', 'GET'])
def textFromWebsite(websiteUrl):
	#task = celery.get_text_from_website.apply_async(args=[websiteUrl])
	task = celery.send_task('get_text_from_website', args=[websiteUrl], kwargs={})
	return jsonify({}, 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)})
												  
												  
												  
@app.route('/imagesFromWebsite/<websiteUrl>', methods=['POST', 'GET'])
def imagesFromWebsite(websiteUrl):
	#task = celery.get_images_from_website.apply_async(args=[websiteUrl])
	task = celery.send_task('get_images_from_website', args=[websiteUrl], kwargs={})
	return jsonify({}, 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)})

@app.route('/status/<task_id>')
def taskstatus(task_id):
	task = celery.AsyncResult(task_id)
	if task.state == 'PENDING':
		response = {
			'state': task.state,
			'current': 0,
			'total': 1,
			'status': 'Pending...'
		}
	elif task.state != 'FAILURE':
	response = {
			'state': task.state,
			'current': task.info.get('current', 0),
			'total': task.info.get('total', 1),
			'status': task.info.get('status', '')
		}
		if 'result' in task.info:
			response['result'] = task.info['result']
	else:
		# something went wrong in the background job
		response = {
			'state': task.state,
			'current': 1,
			'total': 1,
			'status': str(task.info),  # this is the exception raised
		}
	return jsonify(response)

if __name__ == '__main__':
	app.run(debug=env.get('DEBUG',True),
			port=int(env.get('PORT',5000)),
			host=env.get('HOST','0.0.0.0')
	)
