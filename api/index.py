from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
# snscrape imports
import snscrape.modules.reddit as snreddit
app = Flask(__name__)
#CORS(app)
@app.route('/default')
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

app = Flask(__name__)
CORS(app)


@app.route("/default", methods=['POST'])
def hello_world():
    
    attributes_container = findTweets(request.get_json()['test'])
    ret = []
    for i in attributes_container:
        ## openAiResponse = openAI(i[3], request.get_json()['test']).choices[0].message.content
        ## print(i[0])
        print(type(i[0]))
        temp = ""
        if (type(i[0]) is snreddit.Comment):
            print(i[0].body)
            temp = i[0].body
        elif (type(i[0]) is snreddit.Submission):
            print(i[0].title)
            temp = i[0].title
        retElement = {"content": temp, "user": i[1]}
        ret.append(retElement)
    return json.dumps(ret)



