from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader (template_dir), autoescape = True)


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/signup')
def display_signup():
    template = jinja_env.get_template('signin_form.html')
    return template.render()

@app.route('/signup', methods=['POST'])
def signup():
    
    name = request.form['name']
    password = request.form['password']
    password2 = request.form['password2']
    email = request.form['email']

    name_error = ''
    password_error = ''
    email_error = ''

    if name == '':
        name_error = 'Username cannot be blank'
    else:
        if ' ' in name:
            name_error = 'Username cannot contain spaces'
        else:
            if len(name) < 3 or len(name) > 20:
                name_error = 'Username must be between 3 and 20 characters'

    if password != password2:
            password_error = 'Passwords do not match'
            password = ''
            password2 = ''
    else:
        if password == '':
            password_error = 'Password cannot be blank'
            password = ''
            password2 = ''
        else:
            if ' ' in name:
                password_error = 'Password cannot contain spaces'
                password = ''
                password2 = ''
            else:
                if len(name) < 3 or len(name) > 20:
                    password_error = 'Password must be between 3 and 20 characters'
                    password = ''
                    password2 = ''
    
    if email != '':
        if ' ' in name:
            email_error = 'Email cannot contain spaces'
        else:
            if len(name) < 3 or len(name) > 20:
                email_error = 'Email must be between 3 and 20 characters'
            else:
                at = 0
                dot = 0
                for char in email:
                    if char == chr(64):
                        at = at + 1
                    if char == chr(46):
                        dot = dot + 1
                if dot != 1:
                    email_error = "Email is not valid (.)."
                else:
                    if at != 1:
                        email_error = "Email is not valid (@)."

    if not name_error and not password_error and not email_error:
        return redirect('/login?name={0}'.format(name))
    else:
        template = jinja_env.get_template('signin_form.html')
        return template.render(name_error=name_error, password_error=password_error, email_error=email_error, name=name, password=password, password2=password2, email=email)

@app.route('/login')
def login():
    name = request.args.get('name')
    template = jinja_env.get_template('login.html')
    return template.render(user=name)

app.run()