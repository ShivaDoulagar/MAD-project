from flask import Flask,render_template,request
import sqlite3


main = Flask(__name__)

@main.route("/",methods= ['GET'])
def loginpage():
    return render_template('index.html')

@main.route('/form',methods=['POST'],endpoint='form')
def sinin():
    try:
            given_mail = request.form['mail']
            given_password = request.form['password']

            db = sqlite3.connect('project.db')
            users = db.execute('SELECT * FROM users WHERE mail =?  AND password =?',(given_mail,given_password)).fetchone()
            users = list(users)
            db.close()

            if (given_mail == users[1] and given_password == users[2]):

                user_type = users[3]
                if user_type == 'admin':
                    return "I am admin"
                elif user_type == 'customer':
                    return "I am customer"
                else:
                    return "I am Pro"
            else:
                return "Invalid credentials, please try again."
    except Exception as e:
        return f"SORRY! SOME ERROR HAS OCCURRED: {str(e)}"


@main.route('/register',methods =['GET'] )
def register():
    try:
        return render_template('register.html')
    except:
        return "Some error has occured"




@main.route('/register_as_pro',methods =['GET'] )
def register_as_pro():
    try:
        return render_template('register_as_pro.html')
    except:
        return "Some Error as occured"









if __name__ == "__main__":
    main.run(debug=True)