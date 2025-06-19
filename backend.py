from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

# Route pour servir le fichier manifest.json depuis static/
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

# Route pour servir le service-worker.js depuis /
@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('.', 'service-worker.js', mimetype='application/javascript')  # Le point signifie "le dossier courant"

@app.route('/offline.html')
def offline():
    return render_template('offline.html')




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False)

