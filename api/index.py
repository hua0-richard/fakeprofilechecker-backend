#flask imports, cors imports
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json

# snscrape imports
import snscrape.modules.twitter as sntwitter

# openAI imports
import openai

# openAI key
openai.api_key = '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' 

# timeout imports
import signal

# CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

def openAI(tweet, user):
  return (openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  temperature=0,
  messages=[
        {"role": "user", "content": "The following tweet is from the user " + user},
        {"role": "user", "content": "If the tweet contains misleading information output #true. Otherwise, output #false: " + tweet},
    ]   
    ))

def openAIContext(tweet, user): 
    return (openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
            {"role": "user", "content": "The following tweet is from the user " + user},
            {"role": "user", "content": "Explain the context of the tweet" + tweet},
        ]   
        ))

def openAIExplainMisinfo(tweet, user):
    return (openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
            {"role": "user", "content": "The following tweet is from the user " + user},
            {"role": "user", "content": "Explain why this twee contains misleading information" + tweet},
        ]   
        )) 

def findTweets(user):
    attributes_container = []
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:' + user).get_items()):
        if i>10:
            break
        attributes_container.append([tweet.date, tweet.likeCount, tweet.sourceLabel, tweet.content, tweet.media, tweet.user.username, tweet.user.profileImageUrl])
    return attributes_container


@app.route("/default", methods=['POST'])
def hello_world():
    attributes_container = findTweets(request.get_json()['test'])
    ret = []
    for i in attributes_container:
        temp = i[4]
        if (i[4] is None):
            temp = ""
        else:
            if (len(i[4]) == 0):
                temp = ""
            else:
                if(type(i[4][0]) == sntwitter.Photo):
                    temp = i[4][0].previewUrl
                else:
                    temp = ""
                print (i[4][0])
        ##openAiResponse = openAI(i[3], request.get_json()['test']).choices[0].message.content
        openAiResponse = ""
        # print(i[6])
        retElement = {"likes": i[1], "source": i[2], "content": i[3], "media": temp, "analysis": openAiResponse, "user": i[5], 'profilepic': i[6]}
        ret.append(retElement)
    result = jsonify(ret)
    return result

@app.route("/misinformation", methods=['POST'])
def misinfo():
    content = request.get_json()['content']
    user = request.get_json()['user']
    print(user)
    print(content)
    openAiResponse = openAI(content, user).choices[0].message.content
    print(openAiResponse)
    return jsonify(openAiResponse)

@app.route("/factCheck")
def fact_check():
    return ""