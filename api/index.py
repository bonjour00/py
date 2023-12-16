from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "python-flask-69655",
  "private_key_id": "58fe5a3a34c246cd8ab2a3205983910c1a4784d0",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCpPZgoI1ZygiBr\n5csBYfrphXkBVNyzGAnTN4/GkqilbcUgHepH1ng1fXxO1hjJXVcQdNF4SLFHtipi\nvSLEMTIHX39JXNehem9t7mT3bxBUXuaLel0BnJHaAHmWiFMZ1DXnAPL85hBZMFrh\nrrGYGjOmhKylgst9tdizwW4UdFzrIthm9BCfqxwFM7/Q54h17vk+xGABNHH8NcoM\nUL2TmwIj6GCToxXf/3z75PuATiEUkAAeW9ANBBnotvAwpp23IsQAKiFjd8pn3fVO\n2U5+FbfMTO/ArXqPsEP4oq562GbtJxjTkWjEZ8+Bo9xO8zOdlS9kW19kfXp2BI5d\nqt2KHlepAgMBAAECggEAAXSFn+a54g8rXzIhHjhs82AR68iCg0m0H+xM4Ky3JYD9\nnmqTbp2x9+fFz1m46dZTHtGaUXnyiEbRM3sj1uMDZpvUGNnjAsDuP1g65wO99LPC\nMLXTIeXqPSEe6oPujvzLn9pavIDv6Axp46HgZgnnoslmQKAQxtpu7BDANQ3RFLZ6\n5cJjL1LZv+4lrYyxWU5eOJhkNlotWKEQ0lS3W7Bza/llcvtNxhC/Ny0A1pOy4XxV\nqvK3v0xsYIwwLSEQ92T9L/aaDvDdUT1XqzV060q7kFwwwcKvvjP6tkiflWVBXZ8Y\n/ZEfN+KH9OyyVsaf4kjJRZIIvN6dxoJ4zhmq6+ydQQKBgQDg8SJC8Bn/Xn6qQOwG\n1dtts5whJZQnzsWJUy6LpFT+QEVJj5UszCGqh9wEMqAl25kfN9p5vOfUu77Lcjuu\n+8NON/tI2zdSKhecZjbEWjkuZBV+pD8FGIsMR/zls1MFlh2gXpN2cOzFATwVLjal\nb5cIWrqTQvVbd4FX2Rw5e1eWGQKBgQDAm5/a/esH2lFQwngIGYEFFh95WjMqsP/V\nyBu/uGO4vGwnbRxVCLoIGJ7hO7fEn0/aLz7ri1HMWBk0ujgB1JtkFfb06CUYG9tJ\ncGol2mwpgcTnermk/YSo61PXw0c/xwoZ4xwHOJA88wwdr2eHLepdZFmPEibVkSPk\ntdyLQaRgEQKBgHrBfVYUW8uuEOfuuB/e03nhm+HG9TxoLgsMNwmD69I41tcXIWyq\nFfFPZTVxP06Jsd2EiJkJC2df8fZq58FNqb7k9CBFacJQMERsz5SGPFBh1A0hqzan\ntzJDkvLz0unoi1B6bHUlmUDFtLlGWBIefMjVYp582xNIe3Cqjimccyb5AoGBAKIT\nUtUIznnxMHPw8Oh/7Z3GG/4V9PB7uQzAMvmFxAR0Kd6TZj/38/NUJH4Lrnv6Q0uq\nbhvvRInbqHpCKVcA/TGfegxkPLKo3kJSIkBwKIxU8siG8SjxXGx4ejkZzh7Q8qMO\nBUveQSHIs+1W6JtL++dSxjoqYBte4wFWN5vHRPbBAoGADhUI6doByJTg24SXKLnN\nCv7tCXNFTN0Ay+FMbEqNsCOzpgu5WE5CMiaD2n7Q9f3Q0loUZ2X/ljvI6aEgfcpf\n5nM6gbLxtJOmVBJdS+gVdCiWzCcXsPTUrDlS+mtZ6JgGzRmqqbMQRWKlOzrhA0pY\nRgZ27YGTEnGB7FAXoJEc81k=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-k10rc@python-flask-69655.iam.gserviceaccount.com",
  "client_id": "101382753141123991293",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-k10rc%40python-flask-69655.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
# r'C:\Users\User\Desktop\py\key.json'
app = firebase_admin.initialize_app(cred)

db = firestore.client()
app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    doc_ref = db.collection("posts").document("WasXXBdrVywtUc7pz8F6")
    doc = doc_ref.get()

    return jsonify(doc.to_dict())

if __name__ == "__main__":
    app.run(debug=True)