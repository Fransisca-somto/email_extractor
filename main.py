from flask import Flask, request, jsonify
import re
import requests
import email_extract

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    data = request.get_json()
    print("Received a request at the home route.")
    emails = email_extract.getemails(data["URLS"])
    return emails

if __name__ == '__main__':
    app.run(debug=True)