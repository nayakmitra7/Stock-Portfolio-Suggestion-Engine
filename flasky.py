
from flask import Flask, render_template, request
import traceback
from alpha_vantage.timeseries import TimeSeries
import time
import math

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
            try:
                res, res_details = get_investment_results(strategy, amount_per_strategy, stock_mapping[strategy])
            except ValueError:
                # Retry after 1 minute and try again as only 5 API calls are allowed per minute
                time.sleep(60)
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
    stock_details = []
    five_days_history = []
    company_to_numstocks_map = {}
    investment_of_day = []
    history_of_day = []

    investment_per_company = amount_per_strategy / 3

    for stock_symbol in stocks_array:

        ts = TimeSeries(key='')
        data, meta_data = ts.get_daily_adjusted(stock_symbol)

        if meta_data:

            count = 0
            for each_entry in data:
                if count < 5:
                    stock_details.append(
                        [strategy, stock_symbol, each_entry, data[each_entry]['5. adjusted close']])
                    five_days_history.append(each_entry)
                    count = count + 1
                else:
                    break

    sorted_date_set = sorted(set(five_days_history))
    print(sorted_date_set)


    # compute number of initial stocks per company for day 1
    for stock_detail in stock_details:
        if stock_detail[2] == sorted_date_set[0]:
            no_of_stocks_per_company = math.floor(investment_per_company / float(stock_detail[3]))
            company_to_numstocks_map[stock_detail[1]] = no_of_stocks_per_company

    for index in range(len(sorted_date_set)):
        investment_of_day.append(0)
        history_of_day.append([])

    for stock_detail in stock_details:
        for index in range(len(sorted_date_set)):
            if stock_detail[2] == sorted_date_set[index]:
                history_of_day[index].append([stock_detail[1], round(float(stock_detail[3]), 2),
                                              company_to_numstocks_map[stock_detail[1]]])
                investment_of_day[index] += company_to_numstocks_map[stock_detail[1]] * float(stock_detail[3])

    for index in range(len(sorted_date_set)):
        invest_results.append([sorted_date_set[index], round(investment_of_day[index], 2)])
        invest_results_detailed.append([sorted_date_set[index], history_of_day[index]])

    print("Investment Results: ")
    print(invest_results)
    print("Stock Value History Results: ")
    print(invest_results_detailed)

    return invest_results, invest_results_detailed


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
