from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/index")
def index():
    return render_template( 'index.html' )

@app.route("/sortable_example")
def sortable_example():
    return render_template( 'sortable_example.html' )


ep = 'select'
@app.route("/{endpoint}".format(endpoint=ep))
def flat_ui():
    return render_template( '{endpoint}.html'.format(endpoint=ep) )

if __name__ == "__main__":
    app.debug = True
    app.run( host='0.0.0.0' )