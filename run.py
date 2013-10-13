from flask import Flask,redirect,render_template
from kutoto.form import MyForm
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#def init():
#    db.create_all()
    
@app.route("/")
def index():
    return "Kochiya Sanae"    

@app.route("/submit",methods=('GET','POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('form.html',form=form)

@app.route('/success')
def success():
    return 'Success'

if __name__ == "__main__":
    app.debug = True
    app.secret_key = '\x03\xedS\x08d`\xb0\x97_\x960x\xac\x12\x87\x88\x9f@x:n`\xeb\xd5'
    app.run()
