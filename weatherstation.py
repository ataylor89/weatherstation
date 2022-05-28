from flask import Flask, render_template, jsonify
import weather

app = Flask(__name__)

@app.route("/weather_report/<latitude>,<longitude>", methods=["GET"])
def weather_report(latitude, longitude):
    weather_report = weather.get_weather_report_for_today(latitude, longitude)
    return jsonify(weather_report)

@app.route("/", methods=["GET"])
def home():
    return render_template("weatherstation.html")

def main():
    app.run(host='localhost', port=9875, debug=True)

if __name__ == '__main__':
    main()