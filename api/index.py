from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
import math
import time
from datetime import datetime
# from flask_cors import CORS

# Use a service account."./key.json"
cred = credentials.Certificate("./key.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)  
# CORS(app)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


@app.route("/COURSE", methods=["GET"])
def fetchData():
    # update_db_ref = db.collection("coursesFetch").add({
    #     'language':0,
    #     'financeandinvestment':0,
    #     'programming':0
    # })#前置作業 自動寫入db判斷data
    query = request.args
    # 今天的月份和日期
    # need_db  = ['01-04', '02-04', '03-04', '04-04', '05-04', '06-04', '07-04', '08-04', '09-04', '10-04', '11-04', '12-04']
    today_date = datetime.now()
    # month_and_day = today_date.strftime("%m-%d")
    month =  today_date.month
    
    doc_ref = db.collection("coursesFetch").document("xn9iNR5oGMiqyZ2a3j55")
    doc = doc_ref.get()
    if(doc.to_dict()[''.join(query.get("groups").split('-'))]==0 or doc.to_dict()[''.join(query.get("groups").split('-'))]%month!=0):
        url = f'https://api.hahow.in/api/products/search?anonymousId=3709ed70-2eda-4eff-83af-8fbee003de9c&category=COURSE&filter=PUBLISHED&groups={query.get("groups")}&page=0&sort=FEEDBACK_SCORE'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            totalCourses = data["data"]["courseData"]["productCount"]
            pages = math.ceil(totalCourses / 24)
            # courses = []
            for page in range(pages):
                time.sleep(0.2)
                url = f'https://api.hahow.in/api/products/search?anonymousId=3709ed70-2eda-4eff-83af-8fbee003de9c&category=COURSE&filter=PUBLISHED&groups={query.get("groups")}&page={page}&sort=FEEDBACK_SCORE'
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    for product in data["data"]["courseData"]["products"]:
                        course = {
                            "id": product["_id"],
                            "author": product["owner"]["name"],
                            "title": product["title"],
                            "metaDescription": product["metaDescription"],
                            "averageRating": product["averageRating"],
                            "numSoldTickets": product["numSoldTickets"],
                            "price": product["price"],  # 原價
                            "discountPrice": product["purchasePlan"]["price"],
                            "coverImage": product["coverImage"]["url"],
                            "numRating": product["numRating"],
                        }
                        db.collection(query.get("groups")+"Courses").document(product["_id"]).set(course)
                        # courses.append(course)
            db_add_ref = db.collection("coursesFetch").document("xn9iNR5oGMiqyZ2a3j55")
            db_add_ref.update({''.join(query.get("groups").split('-')): doc.to_dict()[''.join(query.get("groups").split('-'))]+1})    
            # if (query.get("sort") == "price"):#原爬蟲照price排
            #     return jsonify(sorted(courses, key=lambda x: x["discountPrice"]))
            # elif(query.get("sort") == "free"):#原爬蟲照free排
            #     return jsonify(list(filter(lambda x: x["discountPrice"]== 0, courses)))
    courses_ref  = db.collection(query.get("groups")+"Courses")
    courses = [course.to_dict() for course in courses_ref.stream()]
    if (query.get("sort") == "price"):
        return jsonify(sorted(courses, key=lambda x: x["price"]))
    if(query.get("sort") == "free"):
        return jsonify(list(filter(lambda x: x["price"]== 0, courses)))
    
    return jsonify(sorted(courses, key=lambda x: x["averageRating"], reverse=True))


@app.route("/COURSEDETAIL/<string:id>", methods=["GET"])
def fetchDetail(id):
    url = f"https://api.hahow.in/api/courses/{id}?requestBackup=false"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        product = response.json()
        productDetails = {
            "author": product["owner"]["name"],
            "title": product["title"],
            "metaDescription": product["metaDescription"],
            "averageRating": product["averageRating"],
            "numSoldTickets": product["numSoldTickets"],
            "price": product["price"],  # 原價
            "discountPrice": product["purchasePlan"]["price"],
            "description": product["description"],
            "targetGroup": product["targetGroup"],  # 哪些人適合這堂課？
            "willLearn": product["willLearn"],  # 你可以學到
            "requiredTools": product["requiredTools"],  # 上課前的準備
            "video": product["video"]["videos"][1]["link"],
            "numRating": product["numRating"],
            "profileImageUrl": product["owner"].get("profileImageUrl", ""),
        }

    url = f"https://api.hahow.in/api/courses/{id}/modules/items"
    response = requests.get(url, headers=headers)
    chapters = []
    if response.status_code == 200:
        data = response.json()
        for chapter in data:
            items = [
                {
                    "id": item["_id"],
                    "chapterNumber": item["chapterNumber"],
                    "title": item["content"]["title"],
                }
                for item in chapter["items"]
            ]
            chapterDetail = {
                "id": chapter["_id"],
                "title": chapter["title"],
                "chapterNumber": chapter["chapterNumber"],
                "items": items,
            }
            chapters.append(chapterDetail)
    return jsonify({"productDetails": productDetails, "chapters": chapters})


@app.route("/courseComment", methods=["GET"])
def fetchComments():
    query = request.args
    url = f'https://api.hahow.in/api/v2/courses/{query.get("id")}/comments?limit=5&page={query.get("page")}'
    response = requests.get(url, headers=headers)
    comments = []
    if response.status_code == 200:
        data = response.json()
        totalComments = data["_metadata"]["count"]
        pages = math.ceil(totalComments / 5)
        print(totalComments, pages)
        for comment in data["data"]:
            commentDetail = {
                "id": comment["_id"],
                "name": comment["owner"]["name"],
                "profileImageUrl": comment["owner"].get("profileImageUrl", ""),
                "content": comment["content"],
            }
            comments.append(commentDetail)
    comments_ref  = db.collection(query.get("id"))
    comments = [{**comment.to_dict(), "id": comment.id} for comment in comments_ref.stream()]+comments
    pages = math.ceil((totalComments+len(comments)) / 5)
    return jsonify({"comments": comments, "pages": pages})

@app.route("/courseCommentWrite", methods=["GET"])
def writeComments():
    # json_data = request.get_json() #POST遇到CORS問題改GET
    query = request.args
    json_data = {
        "id": query.get("id"),
        "name": query.get("name"),
        "profileImageUrl": query.get("profileImageUrl"),
        "content": query.get("content"),
    }
    db.collection(json_data["id"]).add(json_data)
    return jsonify({"data":"success"})

@app.route("/Articles", methods=["GET"])
def fetchArtical():
    # update_db_ref = db.collection("articlesFetch").add({
    #     'language':0,
    #     'financeandinvestment':0,
    #     'programming':0
    # })#前置作業 自動寫入db判斷data
    query = request.args
    # 今天的月份和日期
    # need_db  = ['01-04', '02-04', '03-04', '04-04', '05-04', '06-04', '07-04', '08-04', '09-04', '10-04', '11-04', '12-04']
    today_date = datetime.now()
    # month_and_day = today_date.strftime("%m-%d")
    month =  today_date.month
    
    doc_ref = db.collection("articlesFetch").document("rxuLOHCLxdenWQEbPazl")
    doc = doc_ref.get()
    if(doc.to_dict()[''.join(query.get("groups").split('-'))]==0 or doc.to_dict()[''.join(query.get("groups").split('-'))]%month!=0):
        url = f'https://api.hahow.in/api/products/search?anonymousId=9674e00d-b758-4608-8e1c-56d30ca6c426&category=ARTICLE&page=0&sort=VIEW_COUNT&groups={query.get("groups")}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            totalArticles = data["data"]["articleData"]["productCount"]
            pages = math.ceil(totalArticles / 24)
            # articals = []
            for page in range(pages):
                time.sleep(0.2)
                url = f'https://api.hahow.in/api/products/search?anonymousId=9674e00d-b758-4608-8e1c-56d30ca6c426&category=ARTICLE&sort=VIEW_COUNT&groups={query.get("groups")}&page={page}'
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    for product in data["data"]["articleData"]["products"]:
                        artical = {
                            "id": product["_id"],
                            "author": product["creator"]["name"],
                            "title": product["previewTitle"],
                            "previewDescription": product["previewDescription"],
                            "coverImage": product.get("coverImage", ""),
                            "viewCount": product["viewCount"],
                            "updatedAt": product["updatedAt"],
                        }
                        # articals.append(artical)
                        db.collection(query.get("groups")+"Articles").document(product["_id"]).set(artical)
                        # courses.append(course)
            db_add_ref = db.collection("articlesFetch").document("rxuLOHCLxdenWQEbPazl")
            db_add_ref.update({''.join(query.get("groups").split('-')): doc.to_dict()[''.join(query.get("groups").split('-'))]+1})
    articles_ref  = db.collection(query.get("groups")+"Articles")
    articals = [artical.to_dict() for artical in articles_ref.stream()]
    articleCus_ref  = db.collection("articles")
    articleCus = [{**article.to_dict(), "id": article.id} for article in articleCus_ref.stream()]
    articleCus+=articals
    sorted_array = sorted(articleCus, key=lambda x: x["viewCount"], reverse=True)
    return jsonify(sorted_array)


@app.route("/articleWrite", methods=["GET"])
def articleWrite():
    # json_data = request.get_json() #POST遇到CORS問題改GET
    query = request.args
    json_data = {
        "author": query.get("author"),
        "title": query.get("title"),
        "previewDescription": query.get("previewDescription"),
        "coverImage": {
            "url":"https://firebasestorage.googleapis.com/v0/b/next-flask.appspot.com/o/%E5%85%A7%E6%96%87.png?alt=media&token=55e9698e-eb63-4a64-a66f-957c303ff87d"
        },
        "viewCount":1,
        "updatedAt": datetime.now(),
        "uid":query.get("uid"),
        "content":query.get("content")
    }
    db.collection("articles").add(json_data)
    return jsonify({"data":json_data})


@app.route("/ArticleDetail/<string:id>", methods=["GET"])
def fetchArticleDetail(id):
    url = f"https://api.hahow.in/api/articles/{id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        product = response.json()
        articleDetails = {
            "id": product["_id"],
            "author": product["creator"]["name"],
            "title": product["title"],
            "previewDescription": product["previewDescription"],
            "content": product["contentBlocks"][0]["content"],
            "coverImage": product.get("coverImage", ""),
            "viewCount": product["viewCount"],
            "updatedAt": product["updatedAt"],
        }
        return jsonify(articleDetails)
    doc_ref = db.collection("articles").document(id)
    doc = doc_ref.get()
    obj = doc.to_dict()
    obj['id'] = doc.id
    doc_ref.update({"viewCount":obj['viewCount']+1})
    return jsonify(obj)

@app.route("/myArticles", methods=["GET"])
def myArtical():
    query = request.args
    articleCus_ref  = db.collection("articles")
    articleCus = [{**article.to_dict(), "id": article.id} for article in articleCus_ref.stream()]
    articleCus = list(filter(lambda x: x["uid"]==query.get("uid"), articleCus))
    sorted_array = sorted(articleCus, key=lambda x: x["viewCount"], reverse=True)
    return jsonify(sorted_array)

@app.route("/myArticlesDel", methods=["GET"])
def myArticalDel():
    query = request.args
    db.collection("articles").document(query.get("id")).delete()
    return jsonify({"data":"delete"})

@app.route("/articleUpdate", methods=["GET"])
def articleUpdate():
    # json_data = request.get_json() #POST遇到CORS問題改GET
    query = request.args
    json_data = {
        "title": query.get("title"),
        "previewDescription": query.get("previewDescription"),
        "updatedAt": datetime.now(),
        "content":query.get("content")
    }
    ref = db.collection("articles").document(query.get("id"))
    ref.update(json_data)
    doc_ref = db.collection("articles").document(query.get("id"))
    doc = doc_ref.get()
    return jsonify(doc.to_dict())
@app.route("/message", methods=["GET"])
def message():
    query = request.args
    url = "https://fju-test3.cognitiveservices.azure.com/language/:query-knowledgebases?projectName=shelly-search-test&api-version=2021-10-01"
    headers= {
          "Content-Type": "application/json",
          "Ocp-Apim-Subscription-Key": "fde6fc08d2e14a71b844af69aeea65f7",
        }
    data = {
    "question": query.get("q"),
}
    response = requests.post(url, headers=headers, json=data)
    data = response.json()
    return jsonify({"message":data})

if __name__ == "__main__":
    app.run(debug=True)
