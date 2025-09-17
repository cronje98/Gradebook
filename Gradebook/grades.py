from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#database configuration for 3 db(Student List, IT and Math marks)
app = Flask(__name__) #application instance
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Grades.db"
app.config['SQLALCHEMY_BINDS'] = {
    'second': 'sqlite:///maths.db',
    'third': 'sqlite:///it.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app) #database instance

#Creation of the 3 db's below
class Students(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String[50])
    
class Maths(db.Model):
        __bind_key__ = 'second'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))
        Mathematics=db.Column(db.Integer)

class IT(db.Model):
        __bind_key__ = 'third'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))
        IT=db.Column(db.Integer)


# Create tables in DB
with app.app_context():
    db.create_all()




# Creation of the routes below [for adding students, IT and maths mark, and home page]
@app.route('/') 
def home():
     return render_template('index.html')

@app.route('/add', methods=['POST']) #for adding names to registry
def add():
    sName = request.form['Student']  # Get task from form
    names=[]
    names.append(sName)

    new_task = Students(name=sName)   # Create task
    db.session.add(new_task)           # Add to DB
    db.session.commit()                # Save
    
    return redirect(url_for('home'))  # Go back to home page
    
    

@app.route('/studentList') # for displaying all the current students
def studentList():
    tasks = Students.query.all()
    return render_template('student.html', tasks=tasks)


@app.route('/mgrades', methods=['GET','POST']) #for adding math students grades
def mgrades():
    if request.method == 'POST':
        sName = request.form['Student']
        sMark = request.form['Percentage']

        try:
            # Convert the math mark to integer
            sMark = int(sMark)
        except ValueError:
            return "Invalid mark: must be a number", 400

        # Create and add the student
        new_student = Maths(name=sName, Mathematics=sMark)
        db.session.add(new_student)
        db.session.commit()

    all_students = Maths.query.all()
    return render_template('mgrades.html', students=all_students)
    


@app.route('/ITgrades', methods=['GET','POST']) #for adding IT marks
def igrades():
    if request.method == 'POST':
        sName = request.form['Student']
        sMark = request.form['Percentage']

        try:
            # Convert the IT mark to integer
            sMark = int(sMark)
        except ValueError:
            return "Invalid mark: must be a number", 400

        # Create and add the student for IT
        new_student = IT(name=sName, IT=sMark)
        db.session.add(new_student)
        db.session.commit()

    all_students = IT.query.all()
    return render_template('igrades.html', students=all_students)



    


if __name__ == '__main__': #will run flas on terminal and open window
    app.run(debug=True)