"""
The flask application package.
"""
#Maybe address issues here:

from flask import Flask
app = Flask(__name__)

import AIWebService.views
