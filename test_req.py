# Make a request to https://10.60.54.42:5555/api/explicit-videos that sends the data 'vid_url': 'https://spinnrdev.sfo3.digitaloceanspaces.com/ayazemail/ayazemail_intro_20230417_154018_1681726218.mov' and prints the ressponse.text

vid_url = 'https://spinnrdev.sfo3.digitaloceanspaces.com/ayazemail/ayazemail_intro_20230417_154018_1681726218.mov'
# give me a sample video url
# vid_url= 'https://spinnrdev.sfo3.digitaloceanspaces.com/ayazemail/ayazemail_intro_20230417_154018_1681726218.mov'

import requests
import json

#comment 2

# url = 'https://10.10.44.62:5555/api/ChatGPTWebAPI'
# url  = 'https://10.0.0.93:5555/api/explicit-content'
url = 'https://10.0.0.93:5555/api/ChatGPTWebAPIStream'
# url = ' https://192.168.10.103:5555/api/ChatGPTWebAPI'
# url = 'https://spinnrweb.com/api/ChatGPTWebAPIStream'
# url = 'https://ai.spinnrweb.com:5555/api/GPTResponse2'

headers = {
    'Content-Type': 'application/json',
}


# data = {
#     'url': vid_url
# }
data = {'question': 'Hello! What did I last ask?'}

# response = requests.post(url, data=data, headers=headers, verify=False)
response = requests.post(url, data=json.dumps(data), headers=headers, verify=False, stream=True)

print(response.text)
