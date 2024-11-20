from flask import Flask, render_template_string, render_template, jsonify
from flask import json
from datetime import datetime
from urllib.request import urlopen
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html') # Commentaire

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route("/commits/")
def commits_graph():
    # Récupération des données depuis l'API GitHub
    repo_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(repo_url)
    commits = response.json()

    # Analyse des données pour extraire les minutes
    commit_minutes = {}
    for commit in commits:
        date_str = commit["commit"]["author"]["date"]
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_obj.minute
        commit_minutes[minute] = commit_minutes.get(minute, 0) + 1

    # Préparer les données pour le graphique
    data = [{"minute": minute, "count": count} for minute, count in commit_minutes.items()]

    # Passer les données au template HTML
    return render_template("commits.html", data=data)

if __name__ == "__main__":
  app.run(debug=True)
