import json
from pymongo import MongoClient
from urllib.parse import unquote
import re

#将mongodb包装到类里，在response函数里调用类进行数据库操作
class JDMongo():
    def __init__(self):
        self.client = MongoClient('localhost')
        self.db = self.client.JDapp
        self.products_collection = self.db.products
        self.comments_collection = self.db.comments

def response(flow):
    #调用数据库类
    DBJD = JDMongo()

    #提取商品数据
    url1 = 'cdnware.m.jd.com'    #商品详情地址
    if url1 in flow.request.url:
        text = flow.response.text
        data = json.loads(text) #将字符串反序列化
        info = data.get('wareInfo').get('basicInfo')
        id = info.get('wareId') #商品id
        name = info.get('name') #商品名称
        images = info.get('wareImage')  #商品图链接
        print(id, name, images)
        DBJD.products_collection.insert({'id': id,'name': name,'images': images})

    # 提取评论数据
    url2 = 'getCommentListWithCard'  #评论信息地址
    if url2 in flow.request.url:
        pattern = re.compile('sku\":\"(\d+)\"') #创建模式对象
        body = unquote(flow.request.text) #Request请求参数中包含商品ID
        id = re.search(pattern, body).group(1)  #提取商品ID
        # 提取Response Body
        text = flow.response.text
        data = json.loads(text)
        comments = data.get('commentInfoList')
        # 提取评论数据
        for comment in comments:
            info = comment.get('commentInfo')
            nickname = info.get('userNickName') #买家昵称
            text = info.get('commentData')  #买家评价
            print(id, nickname, text)
            DBJD.comments_collection.insert({'id': id,'nickname': nickname,'text': text})
