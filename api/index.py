from flask import Flask, jsonify
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# Use a service account.
# cred = credentials.Certificate('key.json')
# # r'C:\Users\User\Desktop\py\key.json'
# app = firebase_admin.initialize_app(cred)

# db = firestore.client()
app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    # doc_ref = db.collection("posts").document("WasXXBdrVywtUc7pz8F6")
    # doc = doc_ref.get()

    return jsonify("hello")

if __name__ == "__main__":
    app.run(debug=True)