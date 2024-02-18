# CORE FLASK ENDPOINTS FILE

# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, jsonify, request, Response, g
#-from flask_session import Session
from AIWebService import app, config, helpers #, schemas, transcriber, gc_visionsensor, fireconnect #, nsfw_final_testing
import openai, json
import dotenv

dotenv.load_dotenv()
import os
import requests


messages = []
system_prompt= {"role": "system","content": "You are a pirate, speak like one!"}


openai.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key_here")
#app.config["SESSION_TYPE"] = "filesystem"
#app.config["SESSION_PERMANENT"] = False
#Session(app)

# THIS IS WHERE YOU SET GPT
client = openai.OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
)

# # THIS IS NORMALLY PULLED FROM DB
messages = []


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'ChatGPTWebAPITester.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/hello', methods=['POST', 'GET'])
def hello():
    return jsonify({"message": "Hello World! Testbot API is online."})


@app.route('/ChatGPTWebAPITester', methods=['GET'])
def chatGPTWebAPITester():
    try:
        return render_template('ChatGPTWebAPITester.html',
            title='ChatGPT Tester',
            year=datetime.now().year,
            message='Use /ChatGPTWebAPI for actual API calls.')

    except Exception as e:
        # For any other exception
        print(e)
        return jsonify({"message": config.anyOtherExceptionErrorMessage})

@app.route('/Chat', methods=['POST'])
def chat_with_gpt(messages=messages):
    messages = mongo_tests.get_messages()
    # add system prompt to the beginning of messages:
    messages.extend([system_prompt])
    prompt = request.form['prompt']
    #Adding Pirate Style here:
    messages.append({"role": "system", "content" :"Arr, speakin' in pirate style, me heartie!"})
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model=config.model,
        messages=messages, 
        max_tokens=config.max_tokens,  # Replace with your actual value
        temperature=config.temperature,  # Replace with your actual value
        frequency_penalty=config.frequency_penalty,  # Replace with your actual value
        stream=False
    )
    response_message = response.choices[0].message.content
    response_message = helpers.remove_extra_emojis(response_message)
    messages.append({"role": "assistant", "content": response_message})
    if len(messages) > 5:
        messages = messages[-5:]

    # MAKE SURE YOU ADD THE MESSAGE TO THE DB with mongo_tests.add_message("assistant", response_message)

    print("response_message :", response_message)


    return jsonify({"message": response_message})



"""Tasks to perform:
#Create GPT that speaks with a colonial accent
def chat_with_gpt_colonial

#Create GPT that Dreh tells me what I need to do. Something with memory aspect. Do research

"""


# ##################################################################################################
#################################################### STOP FOR TESTING ##############################
#####################################################################################################


@app.route('/view-configs', methods=['GET','POST'])
def view_config():
    return f'Temperature: {g.temperature}, <br>Frequency Penalty: {g.frequency_penalty}<br>Spinny Prompt: {g.spinny_prompt},<br>Reset Spinny: {g.reset_spinny}, <br>User Info: {g.user_info}, <br>FAQ: {g.faq}, <br><br>AI Moderation Configs: <br>Nudity: {g.nudity_threshold}, <br>Violence: {g.violence_threshold}, <br>Racy: {g.racy_threshold}, <br>Medical: {g.medical_threshold}, <br>Spoof: {g.spoof_threshold}, <br>Seconds Per Scan: {g.seconds_per_scan}'



@app.route('/ChatGPTWebAPIStream', methods=['POST'])
def ChatGPTWebAPIStream():
    data = request.get_json()
    print("DATA", data)
    if not data:
        return jsonify({"reason": "Invalid JSON", "status":"failure"}), 400



    if data.get('previous_messages'):
        # sample_data = [{"role": "user","content": "Why is math important?"},
        #                {"role": "assistant","content": "Because it is"}, 
        #                {"role": "user","content": "Why is that?"}]
        messages = data.get('previous_messages')
        messages = [{"role": "system","content": g.spinny_prompt}] + messages
        if messages:
            if len(messages) > 5:
                messages = [{"role": "system","content": g.spinny_prompt},messages[-4],messages[-3],messages[-2],messages[-1]]
        print("MESSAGES", messages)

    else:
        messages = [{"role": "system","content": g.spinny_prompt}]
    print("MESSAGES", messages)
    prompt = data.get('question')
    # prompt = helpers.AddEmojiRequestToPrompt(prompt)

    if not prompt:
        return jsonify({"reason": "No prompt provided", "status":"failure"}), 400

    
    return Response( stream_response(prompt, messages, g.frequency_penalty, g.max_tokens, g.temperature,  g.model), mimetype='text/event-stream')



# @app.route('/ChatGPTWebAPI', methods=['POST'])
# def GPTResponse2():
#     data = request.get_json()

#     if data.get('previous_messages'):
#         messages = data.get('previous_messages')
#         if len(messages) > 5:
#             messages = [{"role": "system","content": g.spinny_prompt},messages[-4],messages[-3],messages[-2],messages[-1]]
#         print("MESSAGES", messages)
#     else:
#         messages = [{"role": "system","content": g.spinny_prompt}]

#     try:
#         prompt = json.loads(request.data)['question']
#         prompt = helpers.AddEmojiRequestToPrompt(prompt)
 
#         print("***Received PROMPT:",prompt)
#         # Who likes to cook?
#         # specify user_id, with a default value of 1
#         user_id = json.loads(request.data).get('user_id', 1)
#         functions = [
#             {
#             "name": "find_users",
#             "description": "Find related users from our db based on a user's interest (keyword)",
#             "parameters": schemas.FindUsers.schema()
#             },
#             {
#             "name": "find_groups",
#             "description": "Find related groups of users from our db based on a user's interest (keyword)",
#             "parameters": schemas.FindUsers.schema()
#             },
#             {
#                 "name": "find_events",
#                 "description": "Find related events from our db based on a user's interest (keyword)",
#                 "parameters": schemas.FindUsers.schema()
#             },
#             {
#                 "name": "browse_Spinnr_docs",
#                 "description": "Browse Spinnr's FAQs based on a keyword",
#                 "parameters": schemas.FindUsers.schema()
#             }


#         ]
#         print(f"*************GPT CALL RECEIVED **********\n{prompt}")
#         # messages.append({'role':'system', 'content':'You are an assistant named "Spinny" on the app Spinnr, a mentally friendly social media platform.'})

#         messages.append({"role": "user", "content": f"{prompt}"})
        
#         response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#         functions=functions,
#         function_call='auto',
#         max_tokens=g.max_tokens,
#         temperature=g.temperature,
#         frequency_penalty=g.frequency_penalty
#         )

#         # Step 2: check if GPT wanted to call a function
#         print(f"*************RESPONSE FROM GPT **********\n{response}")
#         if response['choices'][0]['message'].get("function_call"):
#             # Step 3: call the function
#             # Note: the JSON response may not always be valid; be sure to handle errors
#             available_functions = {
#                 # "find_users": DBFunctions.find_users,
#                 # "find_groups": DBFunctions.find_groups,
#                 # "find_events": DBFunctions.find_events,
#                 "browse_Spinnr_docs": DBFunctions.browse_Spinnr_docs
#             }  # only one function in this example, but you can have multiple
#             function_name = response['choices'][0]['message']["function_call"]["name"]
#             fuction_to_call = available_functions[function_name]
#             print(f"*************FUNCTION RECEIVED **********\n{function_name}")
#             function_args = json.loads(response['choices'][0]['message']["function_call"]["arguments"])
#             print(f"*************FUNCTION ARGS **********\n{function_args}")
#             try:
#                 function_response = fuction_to_call(
#                     function_args
#                 )['results']
#             except Exception as e:
#                 print(f"ERROR IN SQL :{e}")
#                 function_response = f"Sorry, I couldn't find anything due to error in call: {e}"

#             function_response = f"Here are the results we found from our database: {function_response}"
#             # Step 4: send the info on the function call and function response to GPT
#             # messages.append(response)  # extend conversation with assistant's reply
#             messages.append(
#                 {
#                     "role": "function",
#                     "name": function_name,
#                     "content": function_response,
#                 }
#             )  # extend conversation with function response
#             print(f'messages: {messages}')
#             second_response = openai.ChatCompletion.create(
#                 model=g.model,
#                 messages=messages,
#             )  # get a new response from GPT where it can see the function response
#             # return jsonify({'message':second_response})
#         else:
#             second_response = response
#         messages.append(second_response['choices'][0]['message'].to_dict())
#         # if messages is greater than 5, remove the first message

#         # Keep only the last 5 messages.
#         if len(messages) > 5:
#             messages = [messages[0],messages[-4],messages[-2],messages[-1]]

#         print(f"*************SECOND RESPONSE FROM GPT **********\n{second_response}")
#         return jsonify({'answer':second_response['choices'][0]['message']['content'], 'status': 'success'})
#     except Exception as e:
#         # For any other exception
#         print(e)
#         return jsonify({"reason": e, "status": "failure", "message": config.anyOtherExceptionErrorMessage})


# FUNCTION_LABELS = [
#     {
#     "name": "find_users",
#     "description": "Find related users from our db based on a user's interest (keyword).",
#     "parameters": schemas.FindUsers.schema()
#     },
#     {
#     "name": "find_groups",
#     "description": "Find related groups of users from our db based on a user's interest (keyword).",
#     "parameters": schemas.FindUsers.schema()
#     },
#     {
#     "name": "find_events",
#     "description": "Find related events from our db based on a user's interest (keyword)",
#     "parameters": schemas.FindUsers.schema()
#     },
#     {
#     "name": "browse_Spinnr_docs",
#     "description": "Browse Spinnr's FAQs based on a keyword.",
#     "parameters": schemas.FindUsers.schema()
#     }
#     ]


# def handle_function_call(function_name, function_args):
#     print(f"*************FUNCTION RECEIVED **********\n{function_name},\nArgs: {function_args}")    
#     AVAILABLE_FUNCTIONS = {
#         "find_users": DBFunctions.find_users,
#         "find_groups": DBFunctions.find_groups,
#         "find_events": DBFunctions.find_events,
#         "browse_Spinnr_docs": DBFunctions.browse_Spinnr_docs
#     }
#     # try:
#     function_to_call = AVAILABLE_FUNCTIONS[function_name]
#     # args is a string right now, so we need to convert it to a dictionary
#     response = function_to_call(json.loads(function_args))['results']
#     return f"Here are the results we found from our database: {response}"
#     # except Exception as e:
#     #     print(f"ERROR IN SQL :{e}")
#     #     return f"Sorry, I couldn't find anything due to error in call: {e}"


# def stream_response(prompt, messages, frequency_penalty, max_tokens, temperature, model):
#     # Add the new user message to the messages list.
#     messages.append({"role": "user", "content": prompt})
#     functions = FUNCTION_LABELS

#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=temperature,
#         stream=True,
#         functions=functions,
#         max_tokens=max_tokens,
#         n=1,
#         frequency_penalty=frequency_penalty
#     )
#     function_args = ''
#     full_response = ''
#     for chunk in response:
#         chunk_message = chunk['choices'][0]['delta']

#         print("CHUNK MESSAGE", chunk_message)
        
#         if chunk_message.get("function_call"):
#             if chunk_message["function_call"].get("name"):
#                 function_name = chunk_message["function_call"].get("name")

#             else:
#                 function_args += chunk_message['function_call'].get('arguments', '')
#             if chunk_message['function_call'].get('arguments') == "}":
            
            
#                 function_response = handle_function_call(function_name, function_args)
#                 messages.append({
#                     "role": "function",
#                     "name": function_name,
#                     "content": function_response,
#                 })
#                 second_response = openai.ChatCompletion.create(
#                     model=model,
#                     messages=messages,
#                     temperature=temperature,
#                     stream=True
#                 )
#                 for chunk in second_response:
#                     print("CHUNK_MESSAGE",chunk)
#                     if chunk['choices'][0]['delta'].get('content'):
#                         full_response += chunk['choices'][0]['delta']['content']
#                         yield json.dumps(chunk['choices'][0]['delta'])


#             if chunk_message.get('content'):
#                 full_response += chunk_message['content']
#         else:
#             yield json.dumps(chunk_message)
   


#     messages.append({"role": "assistant", "content": full_response})
#     # Keep only the last 5 messages.
#     if len(messages) > 5:
#         messages = messages[-5:]

#     # Store the updated messages back in the session
#     # session['messages'] = messages
#     # session.modified = True

#     yield from []  # This is just to ensure the generator has a final yield


# # Static Response
# @app.route('/StupidChatGPTWebAPI', methods=['POST', 'GET'])
# def ChatGPTWebAPI():
#     prompt = json.loads(request.data)['prompt']
#     prompt = helpers.AddEmojiRequestToPrompt(prompt)
#     # result_dict = classification.query_intent(prompt)
#     result_dict = {"squads": {}, "results": [], "response": ""}
    
#     if result_dict['squads'] != {} or result_dict['results'] != []:
#         prompt = prompt + config.foundResults + f'{result_dict}'

#     print("FULL PROMPT TO GPT: ", prompt)
#     messages = [{"role": "user", "content": prompt}]
#     response_text = ""
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo-0613",
#         messages=messages,
#         max_tokens=config.max_tokens,
#         n=1,
#         stop=None,
#         temperature=g.temperature,
#         frequency_penalty=g.frequency_penalty,
#         stream=False
#     )
#     print("response: ", response)
#     response_message = response["choices"][0]["message"]["content"].strip()
#     print("response_message :", response_message)
#     # set response to the entire response object

#     result_dict['response'] = response_message
#     print("result_dict: ", result_dict)
#     return result_dict
