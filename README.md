
<!-- Add an image from  https://dolphinstudios.co/wp-content/uploads/2022/12/imageedit_3_2868179854-cropped.png -->
<a href="https://dolphinstudios.co/"><img src="https://dolphinstudios.co/wp-content/uploads/2022/12/imageedit_3_2868179854-cropped.png" width="100"></a>
# GPT Testing Repo for Flask 

This application provides a web interface for interacting with an AI chatbot powered by OpenAI's GPT model. It's built using Flask, a lightweight WSGI web application framework in Python.


Built by Dolphin Studios, LLC

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3
- pip (Python package installer)

## Installation

1. **Clone the Repository**

   If you haven't already, clone the repository to your local machine:

   ```bash
   git clone https://github.com/apiispanen/gpt-tests.git
   cd your-repository
Install Dependencies

Navigate to the root directory of the project and install the required Python packages:

   ```pip install -r requirements.txt```

### Set Environment Variables 


You need to set the OPENAI_API_KEY and SECRET_KEY environment variables. You can do this by creating a .env file in the root directory of the project with the following contents:

```plaintext
    OPENAI_API_KEY=your_openai_api_key_here
    SECRET_KEY=your_secret_key_here 
```

Replace your_openai_api_key_here and your_secret_key_here with your actual OpenAI API key and a secret key for Flask, respectively. Secret key can be anything you'd like.

### Running the Application
Start the Flask Server

Run the following command in the root directory of the project:

bash
Copy code
python runserver.py
This will start the Flask server, and you should see output indicating that the server is running, typically on http://127.0.0.1:5000.

Accessing the Application

Open a web browser and navigate to http://127.0.0.1:5000. This will load the AI chat application, where you can interact with the AI model.

## Application Structure
AIWebService/
Contains the Flask application including templates, static files, and Python scripts.
flask_session/
Session files for Flask.
runserver.py
The main Python script to run to start the Flask server.
    requirements.txt
A list of Python packages that need to be installed.
### Additional Notes
Ensure you have a valid OpenAI API key to interact with the GPT model.
The application is set up for development purposes and should be properly secured before any production use.
Support
For support, please contact info@dolphinstudios.com.