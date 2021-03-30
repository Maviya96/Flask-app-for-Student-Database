from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student

# Connect to Database and create database session
engine = create_engine('sqlite:///students-collection.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# landing page that will display all the students in our database
# This function will operate on the Read operation.
@app.route('/')
@app.route('/records')
def showStudent():
    records = session.query(Student).all()
    return render_template('home.html', records=records)


# This will let us Create a new record and save it in our database
@app.route('/records/new/', methods=['GET', 'POST'])
def newStudent():
    if request.method == 'POST':
        newStudent = Student(first_name=request.form['name'],
                       last_name=request.form['last_name'],
                       dob=request.form['dob'],
                       amount_due=request.form['amount_due'])
        session.add(newStudent)
        session.commit()
        return redirect(url_for('showStudent'))
    else:
        return render_template('newStudent.html')


# This will let us Update our records and save it in our database
@app.route("/records/<int:stud_id>/edit/", methods=['GET', 'POST'])
def editStudent(stud_id):
    editedStudent = session.query(Student).filter_by(id=stud_id).one()
    if request.method == 'POST':
        if request.form['amount_due']:
            editedStudent.amount_due = request.form['amount_due']
            return redirect(url_for('showStudent'))
    else:
        return render_template('editStudent.html', stud=editedStudent)


# This will let us Delete our record
@app.route('/records/<int:stud_id>/delete/', methods=['GET', 'POST'])
def deleteStudent(stud_id):
    studentToDelete = session.query(Student).filter_by(id=stud_id).one()
    if request.method == 'POST':
        session.delete(studentToDelete)
        session.commit()
        return redirect(url_for('showStudent', stud_id=stud_id))
    else:
        return render_template('deleteStudent.html', stud=studentToDelete)


"""
api functions
"""
from flask import jsonify


def get_records():
    records = session.query(Student).all()
    return jsonify(records=[b.serialize for b in records])


def get_record(stud_id):
    records = session.query(Student).filter_by(id=stud_id).one()
    return jsonify(records=records.serialize)


def makeANewRecord(first_name, last_name, dob, amount_due):
    addedstudent = Student(first_name=first_name, last_name=last_name, dob=dob, amount_due=amount_due)
    session.add(addedstudent)
    session.commit()
    return jsonify(Student=addedstudent.serialize)


def updateRecord(id, first_name, last_name, dob, amount_due):
    updatedStudent = session.query(Student).filter_by(id=id).one()
    if not first_name:
        updatedStudent.first_name = first_name
    if not last_name:
        updatedStudent.last_name = last_name
    if not dob:
        updatedStudent.dob = dob
    if not amount_due:
        updatedStudent.amount_due = amount_due
    session.add(updatedStudent)
    session.commit()
    return 'Updated a Record with id %s' % id


def deleteARecord(id):
    studentToDelete = session.query(Student).filter_by(id=id).one()
    session.delete(studentToDelete)
    session.commit()
    return 'Removed Record with id %s' % id


@app.route('/')
@app.route('/recordsApi', methods=['GET', 'POST'])
def recordsFunction():
    if request.method == 'GET':
        return get_records()
    elif request.method == 'POST':
        first_name = request.args.get('first_name', '')
        last_name = request.args.get('last_name', '')
        dob = request.args.get('dob', '')
        amount_due = request.args.get('amount_due', '')
        return makeANewRecord(first_name, last_name, dob, amount_due)


@app.route('/recordsApi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def recordFunctionId(id):
    if request.method == 'GET':
        return get_record(id)

    elif request.method == 'PUT':
        first_name = request.args.get('first_name', '')
        last_name = request.args.get('last_name', '')
        dob = request.args.get('dob', '')
        amount_due = request.args.get('amount_due', '')
        return updateRecord(id, first_name, last_name, dob, amount_due)

    elif request.method == 'DELETE':
        return deleteARecord(id)


if __name__ == '__main__':
    app.debug = True
    app.run()