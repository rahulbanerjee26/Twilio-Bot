from flask import Flask, request
from replit import db
import json

app = Flask('app')


@app.route('/')
def hello_world():
    return 'This is a Twilio Bot', 200


@app.route('/user', methods=['GET', 'POST'])
def user():
    # GET Request
    if request.method == 'GET':
        users = []
        for key in db.keys():
            users.append({'name': key, 'number': db[key]})
        return {'data': users}, 200
    else:
        postData = json.loads(request.form['Memory'])
        postData = postData['twilio']['collected_data']['user_information'][
            'answers']
        name = postData['user_name']['answer']
        phoneNumber = postData['user_phone_number']['answer']
        db[name] = phoneNumber
        return {
            "actions": [{
                "say":
                f"Thank You, {name}! Your info has been saved in the repl db"
            }]
        }, 201


if __name__ == '__main__':
    db.clear()
    app.run(host='0.0.0.0', port=8080, debug=True)
