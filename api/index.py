from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
import math
import time

# Use a service account."./key.json"
cred = credentials.Certificate('./key.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)

headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

@app.route('/COURSE',methods=['GET'])
def fetchData():
   query = request.args
   url = f'https://api.hahow.in/api/products/search?anonymousId=3709ed70-2eda-4eff-83af-8fbee003de9c&category=COURSE&filter=PUBLISHED&groups={query.get("groups")}&page=0&sort=FEEDBACK_SCORE'
   response = requests.get(url, headers=headers)
   if response.status_code == 200:
        data = response.json()
        totalCourses = data['data']['courseData']["productCount"]
        pages = math.ceil(totalCourses/24)
        courses = []
        for page in range(pages):
            time.sleep(0.2)
            url = f'https://api.hahow.in/api/products/search?anonymousId=3709ed70-2eda-4eff-83af-8fbee003de9c&category=COURSE&filter=PUBLISHED&groups={query.get("groups")}&page={page}&sort=FEEDBACK_SCORE'
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for product in data['data']['courseData']['products']:
                    course = {
                        "id": product["_id"],
                        "author" : product["owner"]["name"],
                        "title":product["title"],
                        "metaDescription":product["metaDescription"],
                        "averageRating": product["averageRating"],
                        "numSoldTickets":product["numSoldTickets"],
                        "price":product["price"], #原價
                        "discountPrice":product["purchasePlan"]["price"],
                        "coverImage":product["coverImage"]["url"],
                        "numRating":product["numRating"]
                    }
                    courses.append(course)
        if (query.get("sort") == "price"):
            return jsonify(sorted(courses, key=lambda x: x["discountPrice"]))
        elif(query.get("sort") == "free"):
            return jsonify(list(filter(lambda x: x["discountPrice"]== 0, courses)))
        return jsonify(courses)
   
@app.route('/COURSEDETAIL/<string:id>',methods=['GET'])
def fetchDetail(id):
    url = f'https://api.hahow.in/api/courses/{id}?requestBackup=false'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        product = response.json()
        productDetails = {
            "author" : product["owner"]["name"],
            "title":product["title"],
            "metaDescription":product["metaDescription"],
            "averageRating": product["averageRating"],
            "numSoldTickets":product["numSoldTickets"],
            "price":product["price"], #原價
            "discountPrice":product["purchasePlan"]["price"],
            "description": product["description"],
            "targetGroup":product["targetGroup"],#哪些人適合這堂課？
            "willLearn":product["willLearn"],#你可以學到
            "requiredTools" : product["requiredTools"], #上課前的準備
            "video": product["video"]["videos"][1]["link"],
            "numRating":product["numRating"],
            "profileImageUrl":product["owner"].get("profileImageUrl","")
        }
   
    url = f'https://api.hahow.in/api/courses/{id}/modules/items'
    response = requests.get(url, headers=headers)
    chapters= [] 
    if response.status_code == 200:
        data = response.json()
        for chapter in data:
            
            items= [{
            "id":item["_id"],
            "chapterNumber":item["chapterNumber"],
            "title":item["content"]["title"]
        } for item in chapter["items"]]
            chapterDetail = {
                    "id": chapter["_id"],
                    "title":chapter["title"],
                    "chapterNumber":chapter["chapterNumber"],
                    "items":items,         
                }
            chapters.append(chapterDetail)
    return jsonify({
        "productDetails":productDetails,
        "chapters":chapters
    })
@app.route('/courseComment',methods=['GET'])
def fetchComments():
    query = request.args
    url = f'https://api.hahow.in/api/v2/courses/{query.get("id")}/comments?limit=5&page={query.get("page")}'
    response = requests.get(url, headers=headers)
    comments= [] 
    if response.status_code == 200:
        data = response.json()
        totalComments = data['_metadata']['count']
        pages = math.ceil(totalComments/5)
        print(totalComments,pages)
        for comment in data["data"]:
            commentDetail = {
                "id": comment["_id"],
                "name":comment["owner"]["name"],
                    "profileImageUrl":comment["owner"].get("profileImageUrl",""),
                "content":comment["content"],
            }
            comments.append(commentDetail)
    return jsonify({"comments":comments,
                    "pages":pages
                    })
@app.route('/Articles',methods=['GET'])
def fetchArtical():
   query = request.args
   url = f'https://api.hahow.in/api/products/search?anonymousId=9674e00d-b758-4608-8e1c-56d30ca6c426&category=ARTICLE&page=0&sort=VIEW_COUNT&groups={query.get("groups")}'
   response = requests.get(url, headers=headers)
   if response.status_code == 200:
        data = response.json()
        totalArticles = data['data']['articleData']["productCount"]
        pages = math.ceil(totalArticles/24)
        articals = []
        for page in range(pages):
          time.sleep(0.2)
          url = f'https://api.hahow.in/api/products/search?anonymousId=9674e00d-b758-4608-8e1c-56d30ca6c426&category=ARTICLE&sort=VIEW_COUNT&groups={query.get("groups")}&page={page}'
          response = requests.get(url, headers=headers)
          if response.status_code == 200:
                data = response.json()
                for product in data['data']['articleData']['products']:
                    artical = {
                        "id": product["_id"],
                        "author" : product["creator"]["name"],
                        "title":product["previewTitle"],
                        "previewDescription":product["previewDescription"],
                        "coverImage": product.get("coverImage",""),
                        "viewCount":product["viewCount"],
                        "updatedAt":product["updatedAt"],
                      
                    }
                    articals.append(artical)
        return jsonify(articals)
@app.route('/ArticleDetail/<string:id>',methods=['GET'])
def fetchArticleDetail(id):
   url = f'https://api.hahow.in/api/articles/{id}'
   response = requests.get(url, headers=headers)
   if response.status_code == 200:
        product = response.json()
        articleDetails = {
            "id": product["_id"],
            "author" : product["creator"]["name"],
            "title":product["title"],
            "previewDescription":product["previewDescription"],
            "content": product["contentBlocks"][0]["content"],
            "coverImage": product.get("coverImage",""),
        "viewCount":product["viewCount"],
           "updatedAt":product["updatedAt"],
        }
        return jsonify(articleDetails)

if __name__ == "__main__":
    app.run(debug=True)