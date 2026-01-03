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

@app.route('/emails', methods=['POST'])
def extract_emails():
    data = request.get_json()
    emails = email_extract.getemails(data["URLS"])
    emails_response = emails["Responses"]
    only_emails = []
    for email_list in emails_response.values():
        only_emails.extend(email_list)
    return jsonify({"emails": only_emails})

if __name__ == '__main__':
    app.run(debug=True)