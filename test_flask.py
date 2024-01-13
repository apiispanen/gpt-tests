from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For demonstration purposes. In a real application, keep this secret and unique.

@app.route('/hello', methods=['POST', 'GET'])
def hello():
    # Check if 'count' is already in the session
    if 'count' in session:
        session['count'] += 1
    else:
        session['count'] = 1

    print(f"hello has been accessed {session['count']} times.")
    return f"hello has been accessed {session['count']} times."

@app.route('/api/explicit-contentv2', methods=['POST', 'GET'])
def explicit_contentv2():
    print("explicit-contentv2")
    return "explicit-contentv2"

if __name__ == '__main__':
    HOST = '0.0.0.0' 
    PORT = 5555
    app.run(host=HOST, port=PORT, debug=True)
