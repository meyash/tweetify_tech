from flask import Flask, render_template, request, url_for
import twint
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def login():
    return render_template('login.html')


@app.route('/query', methods=["POST", "GET"])
def query():
    username = request.form['username']
    password = request.form['password']
    if username == 'thapar' and password == 'thapar':
        return render_template('twitter.html')
    else:
        return render_template('login.html', warning='Please enter correct username and password')


@app.route('/results', methods=["POST"])
def result():

    keywords = request.form['keyword']
    noofresults = int(request.form['number'])
    sincedate = request.form['since']
    tilldate = request.form['till']
    location = request.form['loc']

    c = twint.Config()
    c.Search = keywords
    c.Limit = noofresults
    c.Since = sincedate
    c.Until = tilldate
    c.Near = location
    c.Pandas = True
    twint.run.Search(c)

    Tweets_df = twint.storage.panda.Tweets_df
    df = Tweets_df[["tweet", "link", "hashtags", "nlikes"]]
    d = df[:noofresults]

    return render_template('twitter.html', tables=[d.to_html(render_links=True, classes=['table table-striped table-bordered table-hover table-responsive'])])


if __name__ == '__main__':
    app.run(debug=True)
