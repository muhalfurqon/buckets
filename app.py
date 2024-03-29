from http import client
from flask import Flask, render_template, request, jsonify
import requests
from pymongo import MongoClient
import os
from os.path import dirname,join
from dotenv import load_dotenv

doten_vpath = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")
client = MongoClient(MONGO_URI)

db = client.dbbuckets

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        {'num': int(num_receive) },
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update done'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': buckets_list})

@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num_receive = int(request.form["num_give"])
    db.bucket.delete_one({'num': num_receive})
    return jsonify({'msg': 'Delete done!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)