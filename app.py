from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            data = pd.read_csv(file_path)
            return redirect(url_for('results', data=data.to_json()))
        elif 'data' in request.form:
            data = pd.read_csv(request.form['data'])
            return redirect(url_for('results', data=data.to_json()))

    return render_template('index.html')

@app.route('/results')
def results():
    data_json = request.args.get('data')
    data = pd.read_json(data_json)

    # Perform basic analysis (example: summary statistics)
    summary = data.describe().to_html()

    return render_template('results.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
