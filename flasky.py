
from flask import Flask, render_template, request
import datetime
from iexfinance.stocks import Stock
import iexfinance.utils.exceptions as excep
from pytz import timezone
import traceback

app = Flask(__name__)


@app.route("/", methods=["GET"])
def mainpage():
    return render_template("themes/monster-admin/lite version/pages-home.html")


@app.route("/dashboard", methods=["GET"])
def investment_calculator():
    total_amount = request.args.get('search', default = 0, type = int)

    request_strategy_mapping = {
        "EthicalInvest": "Ethical Investing",
        "GrowthInvest": "Growth Investing",
        "IndexInvest": "Index Investing",
        "QualityInvest": "Quality Investing",
        "ValueInvest": "Value Investing",
    }

    stock_mapping = {
        "Ethical Investing" : ['AAPL', 'ADBE', 'NSRGY'],
        "Growth Investing" : ['GDDY', 'ISRG', 'MTH'],
        "Index Investing" : ['VTI', 'IXUS', 'ILTB'],
        "Quality Investing" : ['UFPI', 'VIPS', 'AB'],
        "Value Investing" : ['NRG', 'VIAC', 'NCLH']
    }

    strategies_selected = []
    for k,v in request_strategy_mapping.items():
        if "on" == request.args.get(k, default = "off", type = str):
            strategies_selected.append(v)

    if total_amount < 5000 or len(strategies_selected) > 2 or len(strategies_selected) == 0:
        return "Invalid data passed. Total amount should be atleast 5000 and should select one or two strategies only"

    print ("Amount input: {}".format(total_amount))
    print ("Strategies Selected: {}".format(strategies_selected))

    try:
        investment_results = []
        investment_result_details = []

        amount_per_strategy = total_amount * 1.0 / len(strategies_selected)
        for strategy in strategies_selected:
            res, res_details = get_investment_results(strategy, amount_per_strategy, stock_mapping[strategy])
            investment_results.append([strategy, res])
            investment_result_details.append([strategy, res_details])

        print("Invest results: {}".format(investment_results))
        print("Invest result Details: {}".format(investment_result_details))

        if len(strategies_selected) == 1 and len(investment_results) == 1:
            return render_template("themes/monster-admin/lite version/pages-dashboard.html", results = investment_results, details = investment_result_details)
        elif len(strategies_selected) == 2 and len(investment_results) == 2:
            return render_template("themes/monster-admin/lite version/pages-dashboard.html", results = investment_results, details = investment_result_details)
        else:
            return "Internal server error"

    except ValueError:
        print('Invalid stock symbol configured')
    except Exception as e:
        print('Error connecting to data source, please try again.')
        print(traceback.format_exc())

    return render_template("themes/monster-admin/lite version/pages-dashboard.html")


def get_investment_results(strategy, amount_per_strategy, stocks_array):
    invest_results = []
    invest_results_detailed = []
    return invest_results, invest_results_detailed

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
