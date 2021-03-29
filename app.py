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


# landing page that will display all the books in our database
# This function will operate on the Read operation.
@app.route('/')
@app.route('/books')
def showBooks():
    books = session.query(Student).all()
    return render_template('books.html', books=books)


# This will let us Create a new book and save it in our database
@app.route('/books/new/', methods=['GET', 'POST'])
def newBook():
    if request.method == 'POST':
        newStudent = Student(first_name=request.form['name'],
                       last_name=request.form['last_name'],
                       dob=request.form['dob'],
                       amount_due=request.form['amount_due'])
        session.add(newStudent)
        session.commit()
        return redirect(url_for('showBooks'))
    else:
        return render_template('newBook.html')


# This will let us Update our books and save it in our database
@app.route("/books/<int:book_id>/edit/", methods=['GET', 'POST'])
def editBook(book_id):
    editedStudent = session.query(Student).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['amount_due']:
            editedStudent.amount_due = request.form['amount_due']
            return redirect(url_for('showBooks'))
    else:
        return render_template('editBook.html', book=editedStudent)


# This will let us Delete our book
@app.route('/books/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    studentToDelete = session.query(Student).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(studentToDelete)
        session.commit()
        return redirect(url_for('showBooks', book_id=book_id))
    else:
        return render_template('deleteBook.html', book=studentToDelete)


"""
api functions
"""
from flask import jsonify


def get_books():
    books = session.query(Student).all()
    return jsonify(books=[b.serialize for b in books])


def get_book(book_id):
    books = session.query(Student).filter_by(id=book_id).one()
    return jsonify(books=books.serialize)


def makeANewBook(first_name, last_name, dob, amount_due):
    addedstudent = Student(first_name=first_name, last_name=last_name, dob=dob, amount_due=amount_due)
    session.add(addedstudent)
    session.commit()
    return jsonify(Student=addedstudent.serialize)


def updateBook(id, first_name, last_name, dob, amount_due):
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
    return 'Updated a Book with id %s' % id


def deleteABook(id):
    studentToDelete = session.query(Student).filter_by(id=id).one()
    session.delete(studentToDelete)
    session.commit()
    return 'Removed Book with id %s' % id


@app.route('/')
@app.route('/booksApi', methods=['GET', 'POST'])
def booksFunction():
    if request.method == 'GET':
        return get_books()
    elif request.method == 'POST':
        first_name = request.args.get('first_name', '')
        last_name = request.args.get('last_name', '')
        dob = request.args.get('dob', '')
        amount_due = request.args.get('amount_due', '')
        return makeANewBook(first_name, last_name, dob, amount_due)


@app.route('/booksApi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def bookFunctionId(id):
    if request.method == 'GET':
        return get_book(id)

    elif request.method == 'PUT':
        first_name = request.args.get('first_name', '')
        last_name = request.args.get('last_name', '')
        dob = request.args.get('dob', '')
        amount_due = request.args.get('amount_due', '')
        return updateBook(id, first_name, last_name, dob, amount_due)

    elif request.method == 'DELETE':
        return deleteABook(id)


if __name__ == '__main__':
    app.debug = True
    app.run()