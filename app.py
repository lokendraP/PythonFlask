from flask import Flask, render_template, request
from form import LoginForm, SignUpForm
import re
import psycopg2

myapp = Flask(__name__, template_folder='templates')
myapp.config['SECRET_KEY'] = 'thevirim'

connection = psycopg2.connect(user = "postgres",
                                  password = "root",
                                  host = "localhost",
                                  port = "5433",
                                  database = "VirimTest")


@myapp.route('/register', methods = ['POST', 'GET'])
def register_form():
    form = SignUpForm()
    lgform = LoginForm()
    message = {'status': 'success', 
    'message': 'user register successfully'}
    cursor1 = connection.cursor()
    
    if request.method == 'POST' and form.validate_on_submit():
        #user_id  = request.form.get('username')
        #pwd = request.form.get('password')
        #is_admin = request.form.get('isadmin',0)
        #confirm  = request.form.get('confirm')
        try:
           cursor2 = connection.cursor()
           user_check_query = "select * from userdata"
           cursor2.execute(user_check_query)
           rows = cursor2.fetchall()
        except Exception as ex:
            print (f"Error while Executing {ex}")
        finally:
            cursor2.close()

        for r in rows:
            if form.username.data in {r[0]}:
                message['status'] = 'Failed'
                message['message'] = 'Account already exist'
                return render_template('Register.html', form=form, message=message)
                
        if not re.match(r'[A-Za-z0-9]+', form.username.data):
            message['status'] = 'Failed'
            message['message'] = 'Username must contain only character and numbers'

        else:
            user_register_query = "insert into userdata (username, password, isadmin) values (%s,%s,%s)"
            cursor1.execute(user_register_query, (form.username.data, form.password.data, form.isadmin.data))
            connection.commit()
            #register_user[user_id] = {}
            #register_user[user_id]['Password'] = pwd
            #register_user[user_id]['is Admin'] = 1 if is_admin else 0
            return render_template('login.html', lgform = lgform)
            
    cursor1.close()   
    return render_template('Register.html', form=form, message=message)


@myapp.route('/login', methods = ['POST', 'GET'])
def login_form():
    lgform = LoginForm()
    cursor2 = connection.cursor()
    if request.method == 'POST':
        #userid = request.form.get('USERID')
        #loginpwd = request.form.get('loginpwd')
        user_login_query = "select * from userdata"
        cursor2.execute(user_login_query)
        rows = cursor2.fetchall()
        for r in rows:
            if lgform.loginusername.data in {r[0]} and lgform.loginpassword.data in {r[1]} and 1 in {r[2]}:
                return render_template('userdata.html', list_users = rows)
            elif lgform.loginusername.data in {r[0]} and lgform.loginpassword.data in {r[1]}:
                return "Welcome User"
            else:
                return render_template('login.html', lgform = lgform)

    cursor2.close()
    return render_template('login.html', lgform = lgform)


if __name__ == '__main__':
    myapp.run(debug = True)