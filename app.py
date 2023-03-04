from flask import Flask,render_template,request,redirect
from pprint import pprint
import pymongo
from pymongo import MongoClient
import io
from PIL import Image
import requests
from instabot import Bot
import os 
import glob
cookie_del = glob.glob("config/*cookie.json")
if cookie_del : os.remove(cookie_del[0])

filee=[]
app = Flask(__name__)
bot = Bot()

@app.route('/')#,methods=['GET'])
def home_start():
    #if request.method == 'GET':
    ids = []
    tweets = []
    postt = collection.find({})
    for posts in postt:
        print(posts)
        if(posts["choice"]=="nposted"):
            idd = posts["_id"]
            if idd not in ids:
                ids.append(posts["_id"])
                tweets.append(posts)
                if posts["file_name"] not in filee:
                    image_content = requests.get(posts["img_url"]).content
                    image_file = io.BytesIO(image_content)
                    image = Image.open(image_file)
                    file_path = "static/" + posts["file_loc"]
                    with open(file_path, "wb") as file:
                        image.save(file, "JPEG")
                    filee.append(posts["file_name"])
                
    print(ids)   
    return render_template('index.html',tweets=tweets)


@app.route('/posting',methods=['POST'])
def postit():
    if request.method == 'POST':
        post_text = request.form['posttxt']
        file_name = request.form['filename']
        pstatust = request.form['pstatus']
    #bot.login(username="srightmedia",password="Captainjay@32")
    if(pstatust=="posted"):
        imagelloc = "static/imagis/" + file_name + ".jpg"
        bot.upload_photo(imagelloc,caption=post_text)
        prev = {"file_name" : file_name}
        nxt = {"$set":{"choice" : pstatust}}
        collection.update_one(prev,nxt)
    else:
        prev = {"file_name" : file_name}
        nxt = {"$set":{"choice" : pstatust}}
        collection.update_one(prev,nxt)
    return redirect('/')

if __name__ == "__main__":
    bot.login(username="srightmedia",password="Captainjay@32", is_threaded=True)
    client = pymongo.MongoClient("mongodb+srv://ForeverKnight:Captainjay32@cluster0.au5htbm.mongodb.net/?retryWrites=true&w=majority")
    print(client)
    db = client['db-name']
    collection=db['post']
    print("running yo``````")
    app.run(debug=True)