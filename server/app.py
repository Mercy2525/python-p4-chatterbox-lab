from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages',methods=['Get','POST'])
def messages():
    pass
    if request.method=='GET':
        messages=[message.to_dict() for message in Message.query.order_by(db.asc('created_at')).all()]
        response=make_response(jsonify(messages),200)
        return response
    
    elif request.method=='POST':

        data = request.get_json()
        new_message = Message(
            body = data.get('body'),
            username = data.get('username')
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict=new_message.to_dict()
        response=make_response(jsonify(message_dict),201)
        return response


@app.route('/messages/<int:id>',methods=['PATCH','DELETE','GET'])
def messages_by_id(id):
    pass
    message = Message.query.filter_by(id=id).first()
    
    if request.method=='GET':
        message_dict = {
            'id': message.id,
            'body': message.body,
            'username':message.username
            # Add other fields as needed
        }
        response = make_response(jsonify(message_dict), 200)
        return response
    
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete successful": True,
            "message": "message deleted successfully"
        }

        response = make_response(
            jsonify(response_body),
            200
        )
        return response
    
    elif request.method=='PATCH':
        for attr in request.form:
            setattr(message,attr,request.form.get(attr))

            db.session.add(message)
            db.session.commit()

            msg_dict=message.to_dict()

            response=make_response(jsonify(msg_dict),200)
            
            return response



if __name__ == '__main__':
    app.run(port=5555,debug=True)
