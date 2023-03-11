from flask import Flask, render_template, request
import requests,json
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)