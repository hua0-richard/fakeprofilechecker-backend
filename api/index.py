from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
# snscrape imports
import snscrape.modules.reddit as snreddit
app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

#openAI imports
# import openai
#openAI key
# openai.api_key = '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'

# def openAI(tweet, user):
#   return (openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#         {"role": "user", "content": "The following tweet is from the user " + user},
#         {"role": "user", "content": "If the tweet contains misleading information output #true. Otherwise, output #false.: " + tweet},

#     ]
#     ))
def findTweets(user):
    attributes_container = []
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,reddit in enumerate(snreddit.RedditUserScraper(user).get_items()):
        if i>10:
            break
        attributes_container.append([reddit, reddit.author])
    return attributes_container
