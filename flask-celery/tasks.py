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
from selenium.webdriver.chrome.options import Options
import io
import json
import requests
import shutil

env=os.environ
CELERY_BROKER_URL=env.get('CELERY_BROKER_URL','redis://localhost:6379'),
CELERY_RESULT_BACKEND=env.get('CELERY_RESULT_BACKEND','redis://localhost:6379')


celery= Celery('tasks',
				broker=CELERY_BROKER_URL,
				backend=CELERY_RESULT_BACKEND)


@celery.task(bind=True, name='get_text_from_website')
def get_text_from_website(self, websiteUrl):
	time.sleep(5)
	#websiteUrl = 'onet.pl'
	print("Got a request for a text from: " + websiteUrl)
	#WEBDRIVER_PATH = "chromedriver.exe"
	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--window-size=1420,1080')
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(chrome_options=chrome_options)
	
	driver.get('http://' + websiteUrl)
	pageText = driver.find_element_by_tag_name("body").text
	websiteUrl = driver.current_url.replace('https://', '').replace('https://', '').replace('www.', '') # handle redirections
	driver.close()
	result = {
		"ID": websiteUrl,
		"TextOnly": pageText,
	}
	json_string = json.dumps(result, ensure_ascii=False).encode('utf8')
	if not os.path.exists(websiteUrl + '/text'):
		os.makedirs(websiteUrl + '/text')
	with io.open(websiteUrl + '/text/pageText.txt', 'w', encoding='utf-8') as file:
		file.write(pageText)
	
	return {'current': 100, 'total': 100, 'status': 'Task completed!',
			'result': 'Its done'}
			
			
@celery.task(bind=True, name='get_images_from_website')
def get_images_from_website(self, websiteUrl):
	time.sleep(5)
	print("Got a request for images from: " + websiteUrl)
	#WEBDRIVER_PATH = "chromedriver.exe"
	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--window-size=1420,1080')
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get('http://' + websiteUrl)
	imageElements = driver.find_elements_by_tag_name("img")
	imageLinks = [el.get_attribute("src") for el in imageElements]
	websiteUrl = driver.current_url.replace('https://', '').replace('https://', '').replace('www.', '') # handle redirections
	driver.close()
	fileName = 0
	if not os.path.exists(websiteUrl + '/images'):
		os.makedirs(websiteUrl + '/images')
	with io.open(websiteUrl + '/images/imagesLinks.txt', 'w', encoding='utf-8') as linksFile:
		for src in imageLinks:
			if src:
				r = requests.get(src, stream=True )
				if r.status_code == 200:
					r.raw.decode_content = True
					#if not os.path.exists(websiteUrl + '/images'):
					#	os.makedirs(websiteUrl + '/images')
					with open(websiteUrl + '/images/' + str(fileName) + '.jpg', 'wb') as fileImage:
						shutil.copyfileobj(r.raw, fileImage)
					# TODO: handle svg and other potentially non-standard image formats
					fileName = fileName + 1
			linksFile.write('{}.jpg, {}\n'.format(fileName, src))
	
	return {'current': 100, 'total': 100, 'status': 'Task completed!',
			'result': 'Its done'}