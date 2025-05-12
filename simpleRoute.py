
from flask import Flask, redirect, url_for, request

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# la funzione route va a dirci a quali url va a rispondere la nostra applicazione
# visto che usiamo '/' come url, risponderà solo al caso univoco, usare una regex per 
# prendere più url
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'primo esempio di Flask!'

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

#usiamo l'url per estrarre il dato che andiamo a mostrare
@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


# semplice login non sicuro che usa sia il metodo POST che GET
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()