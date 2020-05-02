
from flask import Flask, render_template, request
import datetime
from iexfinance.stocks import Stock
import iexfinance.utils.exceptions as excep
from pytz import timezone

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("themes/monster-admin/lite version/pages-home.html")


@app.route("/dashboard", methods=["GET", "POST"])
def index1():
    if request.method == 'GET':
        return render_template("themes/monster-admin/lite version/pages-dashboard.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
