#!/usr/bin/python2.7

# Third-party imports.
from flask import Flask, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

# Local imports.
from api import search_books
from config import app
from database import db, Book, User

# The global cache of books that could be added for the user.
books = []

# Ensure that the database is created.
db.create_all()

@app.route("/")
@login_required
def index():
    return redirect(url_for('dashboard'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == "POST":
        # Validate the log-in and direct to the dashboard after logging in.
        form = request.form
        user = User.get_user(form["username"], form["password"])
        if user:
            login_user(user)
            return redirect(url_for("dashboard"))
        # The user was invalid, so simply re-direct to the form.
        else:
            return redirect(url_for("login"))
    else:
        return render_template("login.html")
        

@app.route('/logout', methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/dashboard")
@login_required
def dashboard():
    # Create the page with the contents of the database.
    books = Book.get_books(user_id=current_user.id)
    return render_template("dashboard.html", items=books)


@app.route("/search", methods=["POST"])
@login_required
def search():
    global books
    books = search_books(request.form["type"], request.form["input"])
    return render_template("search.html", request=request.form, items=books)


@app.route("/delete/<book_id>", methods=["POST"])
@login_required
def delete(book_id):
    Book.query.filter_by(id=book_id).delete()
    db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/add/<book_index>", methods=["POST"])
@login_required
def add(book_index):
    book = books[int(book_index)]
    db.session.add(Book(user_id=current_user.id, **book))
    db.session.commit()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)