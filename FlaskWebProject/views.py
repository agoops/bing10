"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,url_for,request
from FlaskWebProject import app
import os
from py_bing_search import PyBingWebSearch
import requests


class Result:
	def __init__(self, title, text):
		self.text = text
		self.title = title


def searchBing(text):
	auth_key = '1KN2M8IdjS+AsXS7+s9NXFRw1vIcHO/awnbyF1+WjEs'
	search_term = text
	bing_web = PyBingWebSearch(auth_key, search_term)
	first_ten_result= bing_web.search(limit=10, format='json') #1-10
	title_urls = [Result(res.title, res.url) for res in first_ten_result]
	return title_urls


@app.route('/')
def show_entries():
	x = Result('title', 'text')
	return render_template('show_entries.html', searched=False)


@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'GET':
		return render_template('show_entries.html')
	if request.method == 'POST':
		search_term = request.form['search_term']
		print(search_term)

		results = searchBing(search_term)
		return render_template('show_entries.html', entries = results, search_term = search_term, searched=True)
