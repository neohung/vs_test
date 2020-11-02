# -*- coding: utf-8 -*-
from flask import Flask
from redis import Redis
from flask import render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from markupsafe import Markup
import random
from matplotlib import pyplot as plt
from io import StringIO
import base64

# %matplotlib inline

app = Flask(__name__)
bootstrap = Bootstrap(app)
redis = Redis(host="mydb", port=6379)

html = """
<html>
    <body>
        <img src="data:image/png;base64,{}" />
    </body>
</html>
"""


@app.route("/")
def home():
    redis.incr("hits")
    # Should be ?bar_name=XXX&bar_stitle=YYY
    data = request.args.to_dict()
    # return Markup(bar.render_embed())
    # return render_template("abc.html", \
    # visit_cnt=redis.get("hits").decode("utf8"))
    return render_template("bar_pyecharts.html", args_json=data)


@app.errorhandler(404)
def page_not_found(e):
    flash(Markup("ERROR: <b>wrong</b> url"), "success")
    return render_template("404.html"), 404


@app.route("/plot")
def plot():
    fig = plt.figure(figsize=(9, 6))
    left = [1, 2, 3, 4, 5]
    # heights of bars
    height = [random.randint(5, 50) for _ in range(5)]
    # labels for bars
    tick_label = ["one", "two", "three", "four", "five"]
    # plotting a bar chart
    plt.bar(
        left, height, tick_label=tick_label, width=0.8, color=["red", "green"]
    )
    # naming the y-axis
    plt.ylabel("y - axis")
    # naming the x-axis
    plt.xlabel("x - axis")
    # plot title
    plt.title("My bar chart!")
    io = StringIO()
    # plt.savefig("./plot.png")
    fig.savefig(io, format="png")
    data = base64.encodestring(io.getvalue())
    return html.format(data)
    # return render_template("plot.html", url="/static/images/plot.png")


@app.route("/hello/<username>")
def hello(username):
    return render_template("hello.html", yourname=username)


@app.route("/loginurl", methods=["GET", "POST"])
def login_fn():
    if request.method == "POST":
        if login_check(request.form["username"], request.form["password"]):
            flash("Login Success!")
            return redirect(
                url_for("hello", username=request.form.get("username"))
            )
    return render_template("login.html")


def login_check(username, password):
    if username == "admin" and password == "admin":
        return True
    else:
        return False


if __name__ == "__main__":
    app.secret_key = "Your Key"
    app.run(host="0.0.0.0", port=80, debug=True)
