from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = [message.to_dict() for message in Message.query.all()]
        response = make_response(jsonify(messages), 200)
        # response.headers["Content-Type"] = "application/json"
        return response
    elif request.method == "POST":
        request_data = request.get_json()
        new_message = Message(
            body=request_data.get("body"), username=request_data.get("username")
        )
        db.session.add(new_message)
        db.session.commit()
        return make_response(jsonify(new_message.to_dict()), 201)


@app.route("/messages/<int:id>", methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == "PATCH":
        request_data = request.get_json()
        for attr in request_data:
            setattr(message, attr, request_data.get(attr))
        db.session.add(message)
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 202)
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        return make_response("", 204)


if __name__ == "__main__":
    app.run(port=5555)
