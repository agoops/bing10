import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from py_bing_search import PyBingWebSearch
import requests

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

# app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.from_object(__name__)

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

# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     db.execute('insert into entries (title, text) values (?, ?)',
#                [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)




if __name__ == '__main__':
    app.run(debug=True)