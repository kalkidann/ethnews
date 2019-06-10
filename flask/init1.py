#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pandas as pd
import json
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from autocorrect import spell
#Initialize the app from Flask
app = Flask(__name__)


with app.open_resource('data/dtim.json') as f:
	master_df = pd.DataFrame.from_records(json.load(f))



@app.route('/search/<string:query>', methods=('GET', 'POST'))
def search(query):
        if request.method == 'POST':
                query = request.form['search_field']
                query=spell(query)
                return redirect(url_for('search', query=query))
        query_ = [query]
        re_item = "^" + query + "$"
        result = [i for i, word in enumerate(master_df['name']) if re.search(re_item, word, flags=re.IGNORECASE)]
        result += [i  for i, word in enumerate(master_df['name']) if re.search(query, word, flags=re.IGNORECASE)]
        result = [i for i, word in enumerate((master_df['title'])) if re.search(re_item, str(word), flags=re.IGNORECASE)]
        result += [i  for i, word in enumerate((master_df['title'])) if re.search(query, str(word), flags=re.IGNORECASE)]
        result = pd.Series(result).drop_duplicates().tolist()
        returned = [{"name": master_df['name'].iat[idx],"time" :master_df['time'].iat[idx], "title": (master_df['title'].iat[idx].split("https:",1))[0], "url": master_df['url'].iat[idx]} for idx in result]
        return render_template('index.html', query=query, returned=returned)
@app.route('/', methods=('GET', 'POST'))
def index():
	if request.method == 'POST':
		query = request.form['search_field']
		return redirect(url_for('search', query=query))
	
	return render_template('index.html')


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 8000, debug = True)
	app.run('59.152.244.227', 8000, debug = True)
	
