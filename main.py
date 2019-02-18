"""
    All flask api
"""
from flask import Flask, request, jsonify
import json


App = Flask(__name__)

@App.route('/wordcloud', methods=['POST'])
def wordcloud_func():
    import word
    try:
        payload = request.get_json()
        response = word.post(payload)
        return json.dumps({
            "Message": "File has been saved as wordcloud.png",
            "Data": response,
            "Success":True
        })
    except Exception as err: 
        return json.dumps({
            "Message" : err,
            "Success" : False
        })


@App.route('/topics', methods=['POST'])
def topics_func():
    import topics
    try:
        payload = request.get_json()
        response = topics.post(payload)
        return json.dumps({
            "Message": "Topic modelling done",
            "Data": response,
            "Success":True
        })
    except Exception as err: 
        return json.dumps({
            "Message" : err,
            "Success" : False
        })


@App.route('/stats', methods=['POST'])
def stats_func():
    import stats
    try:
        payload = request.get_json()
        response = stats.post(payload)
        return json.dumps({
            "Message": "Stats Claculated",
            "Data": response,
            "Success":True
        })
    except Exception as err: 
        return json.dumps({
            "Message" : err,
            "Success" : False
        })


@App.route('/sentiment', methods=['POST'])
def sentiment_func():
    import sentiment
    try:
        payload = request.get_json()
        response = sentiment.post(payload)
        return json.dumps({
            "Message": "Sentiment Analysis done",
            "Data": response,
            "Success":True
        })
    except Exception as err: 
        return json.dumps({
            "Message" : err,
            "Success" : False
        })


@App.route('/entity', methods=['POST'])
def entity_func():
    import entity
    try:
        payload = request.get_json()
        response = entity.post(payload)
        return json.dumps({
            "Message": "Entity recogination done",
            "Data": response,
            "Success":True
        })
    except Exception as err: 
        return json.dumps({
            "Message" : err,
            "Success" : False
        })


# @App.route('/pos_tag', methods=['POST'])
# def pos_tag_func():


#     return json.dumps{
#         "Message":"",
#         "Data":{},
#         "Success":True
#     }

@App.route('/translation', methods=['POST'])
def machine_translation_func():
    import translation
    try:
        payload = request.get_json()
        response = translation.post(payload)
        return json.dumps({
            "Message": "Machine Translation done",
            "Data": response,
            "Success":True
        })
    except Exception as err: 
        return json.dumps({
            "Message" : err,
            "Success" : False
        })


@App.route('/summary', methods=['POST'])
def summary_func():
    import summary
    try:
        payload = request.get_json()
        response = summary.post(payload)
        return json.dumps({
            "Message": "Summarisation done",
            "Data": response,
            "Success":True
        })
    except Exception as err: 
        return json.dumps({
            "Message" : err,
            "Success" : False
        })

@App.route('/qna', methods=['POST'])
def qna_func():
    import qna 
    try:
        payload = request.get_json()
        response = qna.post(payload)
        return json.dumps({
            "Message": "QnA done",
            "Data": response,
            "Success":True
        })
    except Exception as err: 
        return json.dumps({
            "Message" : err,
            "Success" : False
        })



if __name__ == '__main__':
    App.run(host='127.0.0.1', port=5000, debug=True, threaded=True)
