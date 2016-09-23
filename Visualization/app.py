from flask import Flask
from flask import render_template
import json
import pandas as pd

app = Flask(__name__)

data_path = './sampleData'

@app.route("/")
def index():
    return render_template("line_chart.html")

@app.route("/line")
def linechart():
    return render_template("line_chart.html")

@app.route("/pie")
def piechart():
    return render_template("pie_chart.html")

@app.route("/bar")
def barchart():
    return render_template("bar_chart.html")

@app.route('/data')
def get_data():
    with open(data_path + '/line_chart.tsv') as data_file:
        sample_data = pd.read_csv(data_file, sep='\t')
    return sample_data.to_json(orient='records')


if __name__ == "__main__":
    app.run(port=5000,debug=True)
