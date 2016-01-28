from flask import render_template, Flask
app = Flask(__name__)


@app.route('/')
def assistant():
    return render_template('action-selection.html')


if __name__ == "__main__":
    app.run(debug=True)
