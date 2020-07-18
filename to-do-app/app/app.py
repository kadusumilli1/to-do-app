from flask import Flask, request, render_template, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
# define database URI to connect to the db
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://kamal@localhost:5432/todoapp"
db = SQLAlchemy(app)


# SQLAlchemy model definitions
class ToDo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<ToDo id: {self.id}, description: {self.description}>"


# create db table(s)
# if they do not exist
db.create_all()


@app.route("/todos/create", methods=["POST"])
def create():
    error = False
    try:
        todo_description = request.get_json().get("description")
        new_todo = ToDo(description=todo_description)
        db.session.add(new_todo)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        # returns a HTTP error code
        # in case of an error
        abort(400)
    else:
        return jsonify({"description": todo_description})


@app.route("/")
def index():
    return render_template("index.html", data=ToDo.query.all())


if __name__ == "__main__":
    app.run(debug=True)
