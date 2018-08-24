from flask import Flask, render_template
import templates, static
app = Flask(__name__)

@app.route('/static')
@app.route('/')
def index():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True)