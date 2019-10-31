import os
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
#import slack
from ibm_watson  import AssistantV2
import requests
import json


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

service = AssistantV2(
    version='2019-02-28',
    username='apikey',
    password='2OOvszbkkg8jErnokzeDXvi77FainHD1nYdq8E_bSDIK',
    url='https://gateway-wdc.watsonplatform.net/assistant/api/'
)

assistant_id1 ='213721cd-ace3-454f-bf2c-72b97564c321'

response = service.create_session(
    assistant_id= assistant_id1
).get_result()

ms1= json.dumps(response)
session_id1 = json.loads(ms1)

sid=session_id1["session_id"]




service.set_default_headers({'x-watson-learning-opt-out': "true"})


#print(json.dumps(response, indent=2))
#print(msj)
#msj1=msj["generic"]["text"][0]
#print(msj["output"]["text"][0])

def chat(message):
    print("hey here")
    msg = message
    print(msg)
    response1 = service.message(
    	assistant_id= assistant_id1,
    	session_id= sid,
    	input={
        	'message_type': 'text',
        	'text': msg,
    		}
	).get_result()
    return response1
    # ms= json.dumps(response1, indent=2)
    # msj = json.loads(ms)
    # rk=msj["output"]["generic"][0]
    # return rk

"""
web_hook_url = "https://hooks.slack.com/services/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"

slack_msg={'text':'Hi'}

#chat.postMessage(web_hook_url,data=json.dumps(slack_msg))
requests.post(web_hook_url,data=json.dumps(slack_msg))

"""

@app.route("/")
@app.route("/home")
def main():
	#return render_template('log.html')
	return render_template('home.html')

@app.route("/get_response", methods=['GET'])
@cross_origin()
def get_response():
    if request.method == "GET":
        text = request.args.get('text')
        return json.dumps(chat(text))


if __name__ == "__main__":
	app.run(debug=True)
