from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def getParam(param : str):
    if request.method == 'POST':
        # Accessing POST data
        data = request.form.get(param)
        # Handle POST data here
    elif request.method == 'GET':
        # Accessing GET data
        data = request.args.get(param)
        # Handle GET data here
    return data;

@app.route('/')
def hello_world():  # put application's code here
    return render_template('public_html/index.html')


@app.route("/ajax/<path:params>",methods=["GET", "POST"])
def ajax(params):
    # Extracting func and oper from the params string
    func, oper = params.split('&')
    func = func.split('=')[1]  # Extracting value of func
    oper = oper.split('=')[1]  # Extracting value of oper

    # Accessing additional parameters from the query string
    # to access to other password = request.args.get('password')

    message = f"{func}{oper}"
    return jsonify({"message": message , "val" : getParam('val'),"val2": getParam('val2')})


if __name__ == '__main__':
    app.run()
