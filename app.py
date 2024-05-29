# Import needed libraries #
from flask import Flask, render_template, request, Response
from dotenv import load_dotenv
import json, urllib, os

# Start Flask App #
load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/get_weather/", methods=['POST'])
def get_weather():
    # Get weather from the user #
    if request.method == 'POST':
        city = request.form['city']
    else: return render_template("index.html", message="No city arguments.")

    # Get API url #
    key = os.getenv("api_key")
    full_url = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + key).read()
    list_of_data = json.loads(full_url)
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "pressure": str(list_of_data['main']['pressure']) + 'hPa',
        "humidity": str(list_of_data['main']['humidity']) + 'RH',
        "temp-c" : str(round(list_of_data['main']['temp'] - 273)) + '°',
        "temp-f": str(round((list_of_data['main']['temp'] - 273) * 1.8 ) + 32) + '°'
    }
    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
