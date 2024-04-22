from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
import _mysql_connector
import mysql.connector
import json
import cryptography

#Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Chenyang'
# SQLITE DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'


# MySql

# url=jdbc:mysql://164.90.137.194:3306/mtc?useSSL=false&serverTimezone=UTC
# username=diz21
# password=InfSci2710_4600049


# The SQLALCHEMY_DATABASE_URI is a configuration key used by Flask-SQLAlchemy.
# It is a string representing the connection info for a database. Here, this app is connected to a MySQL database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://diz21:InfSci2710_4600049@164.90.137.194:3306/mtc'

# The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is used by Flask-SQLAlchemy to signal the application
# every time a change is about to be made to the database.
# It consumes significant system resources, thus it is false to save resources as it is not needed in most cases.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# An object of the SQLAlchemy class is created which is our ORM
db = SQLAlchemy(app)

'''
Defining From Class

The form handles the POST request sent by a client and validates the user input
Flask-WTF extension uses Python classes to represent web forms.
A form class simply defines the fields of the form as class variables.
'''


# Define a form for user to enter their name
class NamerForm(FlaskForm):
    # StringField represents <input type="text"> in HTML

    # DataRequired validator ensures the field is not submitted empty
    name = StringField("What's your name?", validators=[DataRequired()])
    # SubmitField represents a <input type="submit">, a button control in HTML
    submit = SubmitField("Submit")


'''
The CustomerAccountForm class is similar to NamerForm but represents a longer form
'''


# Define a form for customers to enter their account details
class CustomerAccountForm(FlaskForm):
    # StringField represents <input type="text"> in HTML
    # Validators ensure the fields are not submitted empty
    # The customer account form has two fields - username and password
    customerAccount = StringField("Username:", validators=[DataRequired()])
    customerPassword = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Define a form for employees to enter their account details
class EmployeeAccountForm(FlaskForm):
    # StringField represents <input type="text"> in HTML
    # Validators ensure the fields are not submitted empty
    # The employee account form has two fields - username and password
    employeeAccount = StringField("Username:", validators=[DataRequired()])
    employeePassword = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")

'''
CustomerAccount is a class that inherits from db.Model, a base class for all models from Flask-SQLAlchemy. 
This class defines several fields as class variables. The fields represent the columns of the corresponding
table in the MySQL database. SQLAlchemy uses these class-level variables to create new records in the 
database table
'''


# This class creates a 'model' for the 'CustomerAccount' table in the database

class CustomerAccount(db.Model):
    # Define the attributes of the 'CustomerAccount' table
    # The 'db.Column' instances are used for creating column(s) in the database
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Define a string representation for instances of 'CustomerAccount'
    # Execute it with print, returning a string makes object human-readable
    def __repr__(self):
        return '<Username: {}>'.format(self.username)


'''
From this point on, Flask’s route decorators are used for binding functions in the Python script 
to URLs in the web app. These functions are executed when a user visits the bound URL. 
'''


# Define a route for the main ('/') url
@app.route('/')
# Define the action to take when a user visits the main ('/') url
def index():
    # 'render_template' function is used to generate output from a template file
    return render_template("index.html")


'''
The app.route decorator creates a new route for the Flask application. 
The function below the decorator is executed when a user visits the corresponding URL.
'''


# Define a route that includes a variable component ('name') in the URL
@app.route('/user/<name>')
# Define the action to take when a user visits a URL with their name in it
# The 'name' variable is passed as an argument to this function
def user(name):
    return render_template("user.html", name=name)


'''
A POST request is a method that is used when the client needs to send data to the server 
as part of the request, such as when uploading a file or when submitting a completed web form.
'''


# The 'methods' parameter is a list to which we pass HTTP methods that are accepted for this route.
@app.route('/customerAccount/add', methods=['GET', 'POST'])
# This function is executed when a user visits the 'customerAccount/add' url
def addCustomer():
    # An instance of the form is created
    form = CustomerAccountForm()
    username = None
    # form.validate_on_submit() checks if form has been submitted and validated
    if form.validate_on_submit():
        # Check if username already exists in database
        customer = CustomerAccount.query.filter_by(username=form.customerAccount.data).first()
        if customer is None:
            # If user doesn't already exist, create a new user and add it to the database
            customer = CustomerAccount(username=form.customerAccount.data,
                                       password=form.customerPassword.data)
            db.session.add(customer)
            db.session.commit()
            username = form.customerAccount.data
            # clear form
            form.customerAccount.data = ''
            form.customerPassword.data = ''
            flash('Customer account has been created!')
            # render form again if user account has been created successfully
            return render_template("add_customer.html", form=form, username=username,
                                   existing_customerAccounts=CustomerAccount.query.order_by(
                                       CustomerAccount.customer_id).all())
        else:
            flash('Customer account already exists!')
            # render form again if user account already exists
            return render_template("add_customer.html", form=form, username=username,
                                   existing_customerAccounts=CustomerAccount.query.order_by(
                                       CustomerAccount.customer_id).all())
    return render_template("add_customer.html", form=form, username=username,
                           existing_customerAccounts=CustomerAccount.query.order_by(CustomerAccount.customer_id).all())


'''
The function updateCustomerAccount allows user to edit the username and password for a given id.
It uses the 'POST' method to receive the form data and then update the record in the database
'''


@app.route('/customerAccount/update_<int:id>', methods=['GET', 'POST'])
def updateCustomerAccount(id):
    form = CustomerAccountForm()

    if id == 0:
        # Retrieve and store the new username
        username = form.customerAccount.data
        return render_template("updateCustomerAccount.html", id=id, form=form, name_to_update=None,
                               existing_customerAccounts=
                               CustomerAccount.query.order_by(CustomerAccount.customer_id).all())
    # Use Flask-SQLAlchemy to find first username that matches the given id.
    username_to_update = CustomerAccount.query.get_or_404(id)

    # This checks if the HTTP method is POST which indicates data being sent in the request.
    if request.method == "POST":
        username_to_update.username = request.form['customerAccount']
        username_to_update.password = request.form['customerPassword']

        try:
            # Once the record has been updated, it must be committed to the database.
            db.session.commit()
            flash('Customer account details has been updated!')
            return render_template("updateCustomerAccount.html", id=id, form=form, name_to_update=username_to_update,
                                   existing_customerAccounts=CustomerAccount.query.order_by(
                                       CustomerAccount.customer_id).all())
        except:
            flash("An Error Occurred! Looks like something went wrong!")
            return render_template("updateCustomerAccount.html", id=id, form=form, name_to_update=username_to_update,
                                   existing_customerAccounts=CustomerAccount.query.order_by(
                                       CustomerAccount.customer_id).all())
    else:
        return render_template("updateCustomerAccount.html", id=id, form=form, name_to_update=username_to_update,
                               existing_customerAccounts=CustomerAccount.query.order_by(
                                   CustomerAccount.customer_id).all())


'''
This function deletes a 'CustomerAccount' record from the database
'''


@app.route('/customerAccount/delete_<int:id>', methods=['GET', 'POST'])
def deleteCustomerAccount(id):
    form = CustomerAccountForm()
    # Use Flask-SQLAlchemy to find first name that matches the given id.
    username_to_delete = CustomerAccount.query.get_or_404(id)

    try:
        # Use Flask-SQLAlchemy to delete the record from the database
        db.session.delete(username_to_delete)
        db.session.commit()
        flash('Customer account has been deleted!')
        existing_customerAccounts = CustomerAccount.query.order_by(CustomerAccount.customer_id).all()
        return render_template("deleteCustomerAccount.html", id=id, form=form, name_to_delete=username_to_delete,
                               existing_customerAccounts=existing_customerAccounts)
    except:
        flash("Whoops! There was a problem deleting account!")
        return render_template("deleteCustomerAccount.html", id=id, form=form, name_to_delete=username_to_delete,
                               existing_customerAccounts=existing_customerAccounts)


'''
Flask provides a way to handle errors in a centralized place using @app.errorhandler decorator.
404 and 500 are status codes, 404 indicates Not found, and 500 indicates server error.
'''


@app.errorhandler(404)
def page_not_found(e):
    # Note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


'''
Login Form and Validation 
User needs to enter his/her name and successfully log in to access the name page
'''


@app.route('/login', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('You have successfully logged in.', 'success')
    return render_template("name.html", form=form, name=name)


'''
This function returns a list of dictionary where each dictionary contains an account and its details.
The results are converted into json format.
'''


@app.route('/customerAccount/data', methods=['GET'])
def customer_accounts_data():
    # Query all customer accounts
    customer_accounts = CustomerAccount.query.all()
    # Convert the customer account objects into a list of dictionaries for JSON conversion
    accounts_list = []
    for account in customer_accounts:
        account_data = {
            'customer_id': account.customer_id,
            'username': account.username,
            'password': account.password  # Be cautious about returning passwords; consider omitting this line
        }
        accounts_list.append(account_data)

    # Use jsonify to convert list of dictionaries to JSON and return it
    return jsonify(accounts_list)


# Main driver function for running the Flask application
if __name__ == '__main__':
    # app.run runs the application on a local server.
    # Debug mode is used to provide useful error messages and enable reloader that restarts
    # server whenever any changes are noticed in the scripts.
    app.run(debug=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://diz21:InfSci2710_4600049@164.90.137.194:3306/mtc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
'''
db = SQLAlchemy(app)


# Create a From Class
class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CustomerAccountForm(FlaskForm):
    customerAccount = StringField("Username:", validators=[DataRequired()])
    customerPassword = StringField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")
'''

class EmployeeAccount(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    #Create a String
    def __repr__(self):
        return '<Username: {}>'.format(self.username)
'''
# Create a route decorator
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)
'''

@app.route('/EmployeeAccount/add', methods=['GET', 'POST'])
def addEmployee():
    form = EmployeeAccountForm()
    username = None
    if form.validate_on_submit():
        employee = EmployeeAccount.query.filter_by(username = form.employeeAccount.data).first()
        if employee is None:
            employee = EmployeeAccount(username = form.employeeAccount.data, password = form.employeePassword.data)
            db.session.add(employee)
            db.session.commit()
            username = form.employeeAccount.data
            # clear form
            form.employeeAccount.data = ''
            form.employeePassword.data = ''
            flash('Employee account has been created!')
            return render_template("add_employee.html", form=form, username=username,
                           existing_employeeAccounts=EmployeeAccount.query.order_by(EmployeeAccount.employee_id).all())
        else:
            flash('Employee account already exists!')
            return render_template("add_employee.html", form=form, username=username,
                                   existing_employeeAccounts=EmployeeAccount.query.order_by(EmployeeAccount.employee_id).all())
    return render_template("add_employee.html", form=form, username=username,
                           existing_employeeAccounts=EmployeeAccount.query.order_by(EmployeeAccount.employee_id).all())


@app.route('/employeeAccount/update_<int:id>', methods=['GET', 'POST'])
def updateEmployeeAccount(id):
    form = EmployeeAccountForm()

    if id == 0:
        username = form.employeeAccount.data
        return render_template("updateEmployeeAccount.html", id=id, form=form, name_to_update = None,
                               existing_employeeAccounts=
                               EmployeeAccount.query.order_by(EmployeeAccount.employee_id).all())
    username_to_update = EmployeeAccount.query.get_or_404(id)

    if request.method == "POST":
        username_to_update.username = request.form['employeeAccount']
        username_to_update.password = request.form['employeePassword']

        try:
            db.session.commit()
            flash('Employee account details has been updated!')
            return render_template("updateEmployeeAccount.html", id = id,form=form, name_to_update=username_to_update,
                                   existing_employeeAccounts=EmployeeAccount.query.order_by(EmployeeAccount.employee_id).all())
        except:
            flash("An Error Occurred! Looks like something went wrong!")
            return render_template("updateEmployeeAccount.html", id = id,form=form, name_to_update=username_to_update,
                                   existing_employeeAccounts=EmployeeAccount.query.order_by(EmployeeAccount.employee_id).all())
    else:
        return render_template("updateEmployeeAccount.html", id = id,form=form, name_to_update=username_to_update,
                           existing_employeeAccounts=EmployeeAccount.query.order_by(EmployeeAccount.employee_id).all())


@app.route('/EmployeeAccount/delete_<int:id>', methods=['GET', 'POST'])
def deleteEmployeeAccount(id):
    form = EmployeeAccountForm()
    username_to_delete = EmployeeAccount.query.get_or_404(id)

    try:
        db.session.delete(username_to_delete)
        db.session.commit()
        flash('Employee account has been deleted!')
        existing_EmployeeAccounts = EmployeeAccount.query.order_by(EmployeeAccount.employee_id).all()
        return render_template("deleteEmployeeAccount.html", id = id,form=form, name_to_delete=username_to_delete,
                               existing_EmployeeAccounts=existing_EmployeeAccounts)
    except:
        flash("Whoops! There was a problem deleting account!")
        return render_template("deleteEmployeeAccount.html", id = id,form=form, name_to_delete=username_to_delete,
                               existing_EmployeeAccounts=existing_EmployeeAccounts)




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

'''
# Create Name Page
@app.route('/login', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('You have successfully logged in.', 'success')
    return render_template("name.html", form=form, name=name)
'''
@app.route('/employeeAccount/data', methods=['GET'])
def employee_accounts_data():
    # Query all employee accounts
    employee_accounts = EmployeeAccount.query.all()
    # Convert the employee account objects into a list of dictionaries for JSON conversion
    accounts_list = []
    for account in employee_accounts:
        account_data = {
            'employee_id': account.employee_id,
            'username': account.username,
            'password': account.password  # Be cautious about returning passwords; consider omitting this line
        }
        accounts_list.append(account_data)

    # Use jsonify to convert list of dictionaries to JSON and return it
    return jsonify(accounts_list)

if __name__ == '__main__':
    app.run(debug=True)


# Define a form for Program details
class DeviceProgramForm(FlaskForm):
    # StringField represents <input type="text"> in HTML
    # Validators ensure the fields are not submitted empty
    # The DeviceProgram form has 3 fields - program_name, program_version and expiration_status
    program_name = StringField("Program name:", validators=[DataRequired()])
    program_version = StringField("Program version", validators=[DataRequired()])
    expiration_status = StringField("Expiration Status", validators=[DataRequired()])
    submit = SubmitField("Submit")


class DeviceProgram(db.Model):
    program_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program_name = db.Column(db.String(255), nullable=False)
    program_version = db.Column(db.String(255), nullable=False)
    expiration_status = db.Column(db.String(255), nullable=False)

    #Create a String
    def __repr__(self):
        return '<Program name: {}>'.format(self.program_name)

@app.route('/DeviceProgram/add', methods=['GET', 'POST'])
def addProgram():
    form = DeviceProgramForm()
    program_name = None
    if form.validate_on_submit():
        program = DeviceProgram.query.filter_by(program_name = form.program_name.data).first()
        if program is None:
            program = DeviceProgram(program_name = form.program_name.data, program_version = form.program_version.data, expiration_status = form.expiration_status.data)
            db.session.add(program)
            db.session.commit()
            program_name = form.program_name.data
            # clear form
            form.program_name.data = ''
            form.program_version.data = ''
            form.expiration_status.data = ''
            flash('Program has been created!')
            return render_template("add_program.html", form=form, program_name=program_name,
                                   existing_programs=DeviceProgram.query.order_by(DeviceProgram.program_id).all())
        else:
            flash('Program already exists!')
            return render_template("add_program.html", form=form, program_name=program_name,
                                   existing_programs=DeviceProgram.query.order_by(DeviceProgram.program_id).all())
    return render_template("add_program.html", form=form, program_name=program_name,
                           existing_programs=DeviceProgram.query.order_by(DeviceProgram.program_id).all())


@app.route('/DeviceProgram/update_<int:id>', methods=['GET', 'POST'])
def updateProgram(id):
    form = DeviceProgramForm()

    if id == 0:
        program_name = form.program_name.data
        return render_template("updateProgram.html", id=id, form=form, program_to_update = None,
                               existing_programs=DeviceProgram.query.order_by(DeviceProgram.program_id).all())
    program_to_update = DeviceProgram.query.get_or_404(id)

    if request.method == "POST":
        program_to_update.program_name = request.form['program_name']
        program_to_update.program_version = request.form['program_version']
        program_to_update.expiration_status = request.form['expiration_status']

        try:
            db.session.commit()
            flash('Device Program details has been updated!')
            return render_template("updateProgram.html", id = id,form=form, program_to_update=program_to_update,
                                   existing_programs=DeviceProgram.query.order_by(DeviceProgram.program_id).all())
        except:
            flash("An Error Occurred! Looks like something went wrong!")
            return render_template("updateProgram.html", id = id,form=form, program_to_update=program_to_update,
                                   existing_programs=DeviceProgram.query.order_by(DeviceProgram.program_id).all())
    else:
        return render_template("updateProgram.html", id = id,form=form, program_to_update=program_to_update,
                               existing_programs=DeviceProgram.query.order_by(DeviceProgram.program_id).all())


@app.route('/DeviceProgram/delete_<int:id>', methods=['GET', 'POST'])
def deleteProgram(id):
    form = DeviceProgramForm()
    program_to_delete = DeviceProgram.query.get_or_404(id)

    try:
        db.session.delete(program_to_delete)
        db.session.commit()
        flash('Device Program has been deleted!')
        existing_programs = DeviceProgram.query.order_by(DeviceProgram.program_id).all()
        return render_template("deleteProgram.html", id = id,form=form, program_to_delete=program_to_delete,
                               existing_programs=existing_programs)
    except:
        flash("Whoops! There was a problem deleting Device Program!")
        return render_template("deleteProgram.html", id = id,form=form, program_to_delete=program_to_delete,
                               existing_programs=existing_programs)

@app.route('/DeviceProgram/data', methods=['GET'])
def device_programs_data():
    # Query all device programs
    device_programs = DeviceProgram.query.all()
    # Convert the device program objects into a list of dictionaries for JSON conversion
    programs_list = []
    for program in device_programs:
        program_data = {
            'program_id': program.program_id,
            'program_name': program.program_name,
            'program_version': program.program_version,
            'expiration_status': program.expiration_status
        }
        programs_list.append(program_data)

    # Use jsonify to convert list of dictionaries to JSON and return it
    return jsonify(programs_list)
