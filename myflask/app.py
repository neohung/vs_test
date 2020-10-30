# -*- coding: utf-8 -*-
from flask import Flask
from redis import Redis
from flask import render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from markupsafe import Markup
import random

from pyecharts.charts import Bar
from pyecharts import options as opts

app = Flask(__name__)
bootstrap = Bootstrap(app)
redis = Redis(host="mydb", port=6379)


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


@app.route("/barChart")
def get_bar_chart():
    data = request.args.to_dict()
    result = eval(data.get("result"))
    bname = result.get("bar_name")
    bsubtitle = result.get("bar_stitle")
    c = (
        Bar()
        .add_xaxis(
            ["ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ITEM6", "ITEM7"]
        )
        .add_yaxis("A", [random.randint(10, 100) for _ in range(7)])
        .add_yaxis("B", [random.randint(10, 100) for _ in range(7)])
        .set_global_opts(
            title_opts=opts.TitleOpts(title=bname, subtitle=bsubtitle)
        )
    )
    return c.dump_options_with_quotes()


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
