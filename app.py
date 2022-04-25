from datetime import datetime
from flask import Flask, redirect, url_for, render_template, request, flash
from sqlalchemy import nullslast
from forms import SignUpForm, LoginForm
from flask_login import (
    LoginManager,
    login_required,
    logout_user,
    current_user,
    login_user,
)

from models import db, ToDO, User

# Flask
app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00"
app.config["DEBUG"] = True

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = True
db.init_app(app)

db.create_all()


# Auth
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


# Routes
@app.route("/", methods=["POST", "GET"])
# @login_required
def tasks():
    if not current_user.is_authenticated:
        return redirect("/login")
    if request.method == "POST":
        description = request.form["description"]
        new_item = ToDO(description=description, user_id=current_user.get_id())
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect("/")
        except:
            return "there was an issue adding your task"

    uncomplete = ToDO.query.filter_by(
        user_id=current_user.get_id(), completed=False
    ).order_by(ToDO.date_created.desc())

    complete = ToDO.query.filter_by(
        user_id=current_user.get_id(), completed=True
    ).order_by(ToDO.date_completed.desc())

    return render_template("index.html", uncomplete=uncomplete, complete=complete)


@app.route("/<ordering_by>")
def sort(ordering_by):
    complete = ToDO.query.filter_by(
        user_id=current_user.get_id(), completed=True
    ).order_by(ToDO.date_completed.desc())
    if ordering_by == "created":
        uncomplete = uncomplete = ToDO.query.filter_by(
            user_id=current_user.get_id(), completed=False
        ).order_by(ToDO.date_created.desc())
    if ordering_by == "due":
        uncomplete = ToDO.query.filter_by(
            user_id=current_user.get_id(), completed=False
        ).order_by(ToDO.due_date.nullslast())

    return render_template("index.html", uncomplete=uncomplete, complete=complete)


@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data.lower()).first()
        if existing_user is None:
            user = User(
                first_name=form.first_name.data.capitalize(),
                last_name=form.last_name.data.capitalize(),
                email=form.email.data.lower(),
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect("/")
        flash("A user already exists with that email address")

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            return redirect("/")
        flash("Invalid email or password")
        return redirect("/login")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    deleted_item = ToDO.query.get_or_404(id)

    try:
        db.session.delete(deleted_item)
        db.session.commit()
        return redirect("/")
    except:
        return "error"


@app.route("/complete/<int:id>", methods=["POST"])
def complete(id):
    item = ToDO.query.get_or_404(id)
    item.completed = not item.completed
    if item.completed == True:
        item.date_completed = datetime.utcnow()
    if item.completed == False:
        item.date_completed = None

    try:
        db.session.commit()
        return redirect("/")

    except:
        return "error"


@app.route("/edit/<int:id>", methods=["POST"])
def update(id):
    edited_item = ToDO.query.get_or_404(id)
    edited_item.description = request.form["description"]
    try:
        db.session.commit()
        return redirect("/")

    except:
        return "error"


@app.route("/date/<int:id>", methods=["POST"])
def add_date(id):
    item = ToDO.query.get_or_404(id)
    date = request.form["due_date"]
    item.due_date = datetime.strptime(date, "%m/%d/%Y").date()

    try:
        db.session.commit()
        return redirect("/")

    except:
        return "error"


if __name__ == "__main__":
    app.run(port=3000)
