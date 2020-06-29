from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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


# create db table(s) if they do not exist
db.create_all()


@app.route("/")
def index():
    return render_template("index.html", data=ToDo.query.all())


@app.route("/todos/create", methods=["POST"])
def create():
    todo_description = request.form.get("description")
    new_todo = ToDo(description=todo_description)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
