from config import DB_Config
from datetime import datetime, timedelta
from mongoengine import Document, DateTimeField

class Userlogin:
    collection = DB_Config.col_userlogin

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_data(cls, data):
        return dict(cls.collection.find_one(data))
    
    @classmethod
    def find_data(cls, username_in):
       try:
        data = {'userid': username_in}
        output = cls.collection.find_one(data)
        if output:
            return dict(output)
        else:
            return 0
       except Exception as e:
           return {'error': str(e)}

    
    @classmethod
    def get_count(cls, data, limit=None):
        count = cls.collection.count_documents(data, limit=limit)
        return count

class Userdata:
    collection = DB_Config.col_userdata

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_data(cls, data):
        return dict(cls.collection.find_one(data))
    
    @classmethod
    def find_and_sort_documents(cls, sort_field='_id', sort_order= -1, limit1=1):
        cursor = cls.collection.find().sort(sort_field, sort_order).limit(limit1)
        return list(cursor)
    
    @classmethod
    def find_user_count(cls):
        query = {'userid': {'$exists': True}}
        count = cls.collection.count_documents(query)
        return count
    
    @classmethod
    def find_user_status(cls, data):
        query = {'Activation_status': data}
        count = cls.collection.count_documents(query)
        return count

class Adminlogin:
    collection = DB_Config.col_adminlogin

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_data(cls, data):
        return dict(cls.collection.find_one(data))
    
    @classmethod
    def get_count(cls, data, limit=None):
        count = cls.collection.count_documents(data, limit=limit)
        return count
    @classmethod
    def find_data(cls, data):
       try:
        output = cls.collection.find_one(data)
        if output:
            return dict(output)
        else:
            return 0
       except Exception as e:
           return {'error': str(e)}


class Admindata:
    collection = DB_Config.col_admindata

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_data(cls, data):
        return dict(cls.collection.find_one(data))
    
    @classmethod
    def find_and_sort_documents(cls, sort_field='_id', sort_order= -1, limit1=1):
        cursor = cls.collection.find().sort(sort_field, sort_order).limit(limit1)
        return list(cursor)


class Userotp:
    collection = DB_Config.col_otp
    created_at = DateTimeField(required=True, default=datetime.utcnow)

    @classmethod
    def save(cls, userid, otp):
        #created_at = DateTimeField(required=True, default=datetime.utcnow)
        data = {'userid': userid, 'otp': otp}
        return cls.collection.insert_one(data)
    
    @classmethod
    def find_otp(cls, username_in):
       try:
        data = {'userid': username_in}
        output = cls.collection.find_one(data)
        if output:
            return dict(output)
        else:
            return 0
       except Exception as e:
           return {'error': str(e)}
    
    @classmethod
    def delete_data(cls, user_id):
        result = cls.collection.delete_one({'userid': user_id})
        return result.deleted_count > 0
   
    @classmethod
    def delete_old_otp(cls):
        two_minutes_ago = datetime.utcnow() - timedelta(minutes=2)
        #cls.objects(timestamp__lt=two_minutes_ago).delete()
        result = cls.collection.delete_one(timestamp__lt=two_minutes_ago)
        return result.deleted_count > 0
    

    