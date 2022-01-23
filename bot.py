import os
from twilio.rest import Client

account_sid = os.environ['account_sid']
account_key = os.environ['account_key']
api_url = os.environ['api_url']
client = Client(account_sid, account_key)

'''
  Create an Assistant Resource
'''
assistant = None
unique_assistant_name = 'twilio-bot-assistant'
try:
    assistant = client.autopilot.assistants.create(
        unique_name=unique_assistant_name)
except:
    assistant = client.autopilot.assistants(unique_assistant_name).fetch()
assistant_sid = assistant.sid

'''
  Create a Task Resource
'''
unique_task_name = 'twilio-bot-repl-task'
assistant_task = None
try:
    assistant_task = assistant.tasks.create(
        unique_name=unique_task_name,
        actions={
            "actions": [{
                "collect": {
                    "name": "user_information",
                    "questions": [{
                        "question": "What is your name?",
                        "name": "user_name",
                        "type": "Twilio.FIRST_NAME"
                    }, {
                        "question": "What's your phone number?",
                        "name": "user_phone_number",
                        "type": "Twilio.NUMBER_SEQUENCE"
                    }],
                    "on_complete": {
                        "redirect": {
                            "uri": f'{api_url}/user',
                            "method": "POST"
                        }
                    }
                }
            }]
        })
except:
    assistant_task = assistant.tasks(unique_task_name).fetch()
assistant_task_id = assistant_task.sid


'''
  Add Sample to above task
'''
task_sample = assistant_task.samples.create(language='en-US', tagged_text='register')


'''
Build Model
'''
model_build =  assistant.model_builds.create()

