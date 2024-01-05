import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder='static') #initialize

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
#config

db = SQLAlchemy(app)

#defining data model using a class - creating columns
class Letter(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(2500), nullable=False)

#inherits constructor 

@app.route("/")
def hello_world():
  return render_template("home.html")


@app.route("/write", methods=['GET', 'POST'])
def write_letter():
  if request.method == 'POST':
    letter_content = request.form['content'] #puts content from the form into the letter_content var, request.form is a dictionary containing the form data, and 'content' is the name of the form field where the user enters the letter.
    letter = Letter() #letter is an instance of the Letter class,
    letter.content = letter_content #the content of the letter is set to the content of the form
    db.session.add(letter)
    db.session.commit()
    return redirect(url_for('view_letters'))
  return render_template('write_letter.html')


@app.route("/view")
def view_letters():
  letter = Letter.query.order_by(db.func.random()).first()
  # if letter is not None:
  #   letter_id = letter.id  
  # else:
  #   letter_id = None
  return render_template('view_letters.html', letter=letter)



if __name__ == "__main__": #run on local host
  with app.app_context():#in context of application
    db.create_all()#db initialization
  app.run(host='0.0.0.0', port=3306, debug=True)


