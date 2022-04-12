import json
import os
from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app

#Initialize Flask App
app = Flask(__name__)

#Initialize Firestore DB
cred = credentials.Certificate('keys.json')
default_app = initialize_app(cred)
db = firestore.client()

@app.route("/", methods=['GET'])
def root():
    return "Welcome"


@app.route("/reports/<cpf>", methods=['GET'])
def listReportsByDocument(cpf):
    docs = db.collection(cpf).stream()
    all_reports = []
    for doc in docs:
        dict_doc = doc.to_dict()
        dict_doc.pop('id', None)
        all_reports.append(dict_doc)

    return jsonify(all_reports), 200

@app.route("/reports", methods=['GET','POST'])
def reports():
    if (request.method == 'GET'):
        return listAllReports()
    elif (request.method == 'POST'):
        return createReport()
    else:
        return jsonify(), 405


def listAllReports():
    all_documents = []
    collections = db.collections()
    for collection in collections:
        docs = collection.stream()    
        for doc in docs:
            dict_doc = doc.to_dict()
            dict_doc.pop('cpf', None)
            all_documents.append(dict_doc)

    return jsonify(all_documents), 200


def createReport():
    try:
        id = request.json['cpf']
        root_ref = db.collection(id)
        root_ref.document().set(request.json)
        return "", 204
    except Exception as e:
        return jsonify({"error", str(e)}), 500


#port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(debug=False)