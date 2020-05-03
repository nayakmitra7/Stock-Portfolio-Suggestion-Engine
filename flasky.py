
from flask import Flask, render_template, request
import datetime
from iexfinance.stocks import Stock
import iexfinance.utils.exceptions as excep
from pytz import timezone

app = Flask(__name__)


@app.route("/", methods=["GET"])
def mainpage():
    return render_template("themes/monster-admin/lite version/pages-home.html")


@app.route("/dashboard", methods=["GET"])
def investment_calculator():
    
    return render_template("themes/monster-admin/lite version/pages-dashboard.html")


def get_investment_results(strategy, amount_per_strategy, stocks_array):
    invest_results = []
    invest_results_detailed = []
    return invest_results, invest_results_detailed
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
