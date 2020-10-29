# -*- coding: utf-8 -*-
from flask import Flask
from redis import Redis
from flask import render_template

app = Flask(__name__)
redis = Redis(host="mydb", port=6379)


@app.route("/")
def home():
    redis.incr("hits")
    return render_template("abc.html", visit_cnt=redis.get("hits").decode("utf8"))
    # return "Hello , dfff %s times." % redis.get("hits")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
