from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.users import User

class Message:
    DB = "private_wall_schema"

    def __init__(self, data):
        self.id = data['id']
        self.message = data['message']
        self.sender_id = data['sender_id']
        self.recipient_id = data['recipient_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender = None
        self.recipient = None

#create
    @classmethod
    def save(cls,data):
        query = '''INSERT INTO messages (message, sender_id, recipient_id)
                VALUES (%(message)s, %(sender_id)s, %(recipient_id)s);'''
        return connectToMySQL(cls.DB).query_db(query, data)


#read
    @classmethod
    def get_messages_by_recipient(cls, id):
        query = '''
            SELECT messages.id, messages.message, messages.sender_id, messages.recipient_id, messages.created_at, messages.updated_at,
            sender.id AS sender_id, sender.first_name AS sender_first_name, sender.last_name AS sender_last_name, sender.email AS sender_email, sender.password AS sender_password, sender.created_at AS sender_created_at, sender.updated_at AS sender_updated_at,
            recipient.id AS recipient_id, recipient.first_name AS recipient_first_name, recipient.last_name AS recipient_last_name, recipient.email AS recipient_email, recipient.password AS recipient_password, recipient.created_at AS recipient_created_at, recipient.updated_at AS recipient_updated_at
            FROM messages
            JOIN users AS sender ON sender.id = messages.sender_id
            JOIN users AS recipient ON recipient.id = messages.recipient_id
            WHERE messages.recipient_id = %(id)s
        '''
        results = connectToMySQL(cls.DB).query_db(query, id)
        messages = []
        for message in results:
            sender_data = {
                "id": message["sender_id"],
                "first_name": message["sender_first_name"],
                "last_name": message["sender_last_name"],
                "email": message["sender_email"],
                "password": message["sender_password"],
                "created_at": message['sender_created_at'],
                "updated_at": message['sender_updated_at'],
            }

            recipient_data = {
                "id": message["recipient_id"],
                "first_name": message["recipient_first_name"],
                "last_name": message["recipient_last_name"],
                "email": message["recipient_email"],
                "password": message['recipient_password'],
                'created_at': message['recipient_created_at'],
                "updated_at": message['recipient_created_at'],
            }
            message_obj = cls(message)
            message_obj.sender = User(sender_data)
            message_obj.recipient = User(recipient_data)
            messages.append(message_obj)
            
        return messages

    @classmethod
    def get_messages_sent(cls,id):
        query = '''SELECT COUNT(messages.id) as count FROM messages WHERE sender_id = %(id)s;'''
        results = connectToMySQL(cls.DB).query_db(query, id)
        count = results[0]['count']
        return count
    
    @classmethod
    def get_message_recieved_count(cls,id):
        query = '''SELECT COUNT(messages.id) as count FROM messages WHERE recipient_id = %(id)s;'''
        results = connectToMySQL(cls.DB).query_db(query, id)
        recived_count = results[0]['count']
        return recived_count
    
    
#delete
    @classmethod
    def delete_message(cls, id):
        query  = "DELETE FROM messages WHERE id = %(id)s;"
        
        return connectToMySQL(cls.DB).query_db(query, {"id": id}) 


#static
    @staticmethod
    def validate_message(message):
        is_valid = True
        if not len(message['message']) > 0:
            flash(
                "Message can't be blank.", 'message')
            is_valid = False

        return is_valid