from flask import Blueprint, render_template, jsonify, request, url_for, redirect
views = Blueprint(__name__, "views")



@views.route("/")
def home():
    return render_template("index.html", name="tim")
@views.route("/profile/<username>")
def profile(username):
    return render_template("index.html", name=username)
@views.route("/json")
def get_json():
    return jsonify({"name": "tim"})
@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)
@views.route("/gthn")
def gthmn():
    return redirect(url_for("views.home"))
