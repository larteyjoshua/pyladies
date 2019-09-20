from flask import *
import os
import sqlite3
from flask_toastr import Toastr




app = Flask(__name__)
toastr = Toastr(app)
app.config['SECRET_KEY'] = '3e8277726c74cf0d4a68e2da'


def create_table():
    print("Creating table...")
    conn = sqlite3.connect('pyladies.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS questions (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, created_at date default current_time not null, first_name text, question text)""")
    conn.commit()

print('...inside create db fxn') 

# if not included, creates only DB without any table    
create_table()


    #Entering data from into database
def add_question_to_db(first_name, question):
    conn = sqlite3.connect('pyladies.db')
    c = conn.cursor()
    c.execute("insert into questions(first_name, question) values (?, ?)", (first_name, question))
    conn.commit()
    flash("Question submitted", "success")



@app.route('/')
def index():
    conn = sqlite3.connect("pyladies.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select * from questions order by id DESC")
    rows = c.fetchall()
    return render_template("index.html",rows=rows)

@app.route('/add_question')
def add_question():
   
    first_name = request.args.get('first_name')
    question = request.args.get('question')
    print(first_name)
    print(question)
    add_question_to_db(first_name, question)
    return redirect("/", code=302)


@app.route('/edit_question')
def edit_question():
    id = request.args.get('id')
    first_name = request.args.get('first_name')
    question = request.args.get('question')
  
    print(first_name)
    print(question)
    print(id)

    conn = sqlite3.connect('pyladies.db')
    print('connected')
    c = conn.cursor()
    c.execute('''UPDATE questions SET first_name = ?, question =? WHERE id = ?''', (first_name, question, id))
    conn.commit()
    flash("question Updated SUCCESSFULLY", "success")
    return redirect("/", code=302)

if __name__ == '__main__':
     port=os.environ.get('PORT', 5000)
     app.run(debug=True, host='0.0.0.0', port=port)