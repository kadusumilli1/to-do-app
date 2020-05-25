from flask import Flask, render_template
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


if __name__ == "__main__":
    app.run(debug=True)
