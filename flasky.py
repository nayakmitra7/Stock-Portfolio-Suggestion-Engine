
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
    total_amount = request.args.get('search', default = 0, type = int)
    ethical_on = request.args.get('EthicalInvest', default = "off", type = str)
    growth_on = request.args.get('GrowthInvest', default = "off", type = str)
    index_on = request.args.get('IndexInvest', default = "off", type = str)
    quality_on = request.args.get('QualityInvest', default = "off", type = str)
    value_on = request.args.get('ValueInvest', default = "off", type = str)

    strategies_selected = []
    if "on" == ethical_on:
        strategies_selected.append("Ethical Investing")
    if "on" == growth_on:
        strategies_selected.append("Growth Investing")
    if "on" == index_on:
        strategies_selected.append("Index Investing")
    if "on" == quality_on:
        strategies_selected.append("Quality Investing")
    if "on" == value_on:
        strategies_selected.append("Value Investing")

    if total_amount < 5000 or len(strategies_selected) > 2 or len(strategies_selected) == 0:
        return "Invalid data passed. Total amount should be atleast 5000 and should select one or two strategies only"


    ethical_stock_symbol_array = ['AAPL', 'MSFT', 'ADBE']
        growth_stock_symbol_array = ['FIT', 'GPRO', 'NVDA']
        index_stock_symbol_array = ['FB', 'AMZN', 'HMC']
        quality_stock_symbol_array = ['JPM', 'WMT', 'BBY']
        value_stock_symbol_array = ['TSLA', 'TWTR', 'GOOG']
    return render_template("themes/monster-admin/lite version/pages-dashboard.html")


def get_investment_results(strategy, amount_per_strategy, stocks_array):
    invest_results = []
    invest_results_detailed = []
    return invest_results, invest_results_detailed
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
