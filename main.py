from flask import Flask,render_template,request,redirect,url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash

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


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            given_mail = request.form['mail']
            given_password = request.form['password']
            given_fullname = request.form['fullname']
            given_address = request.form['address']
            given_pincode = request.form['pincode']

            db = sqlite3.connect('project.db')
            cursor = db.cursor()

            user_exists = cursor.execute('SELECT * FROM users WHERE mail = ?', (given_mail,)).fetchone()
            

            if user_exists is None:
                cursor.execute('INSERT INTO customers(mail, password, fullname, address, pincode) VALUES(?,?,?,?,?)',
                               (given_mail, given_password, given_fullname, given_address, given_pincode))
                cursor.execute('INSERT INTO users(mail, password, usertype) VALUES(?,?,?)',
                               (given_mail, given_password, 'customer'))
                db.commit()
                return redirect(url_for('loginpage'))  
            else:
                return render_template('register.html', user_e='User exists!')

        except Exception as e:
            return f"SORRY! SOME ERROR HAS OCCURRED: {str(e)}"

        finally:
            db.close()
    else:
        return render_template('register.html')


def convert_pdf_to_binary(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

@main.route('/regisiter_as_pro', methods=['GET', 'POST'],endpoint='register_as_pro')
def register_as_pro():
    if request.method == 'POST':
        try:
            given_mail = request.form['mail']
            given_password = request.form['password']
            given_fullname = request.form['fullname']
            given_service = request.form['service']
            given_experience = request.form['experience']
            given_document = request.form['doc']
            given_address = request.form['address']
            given_pincode = request.form['pincode']
            pdf_data = convert_pdf_to_binary(given_document)
            
            db = sqlite3.connect('project.db')
            cursor = db.cursor()

            user_exists = cursor.execute('SELECT * FROM users WHERE mail = ?', (given_mail,)).fetchone()
            

            if user_exists is None:
                cursor.execute('INSERT INTO professionals(mail, password, fullname,service,experience,documents, address, pincode) VALUES(?,?,?,?,?,?,?,?)',
                               (given_mail, given_password, given_fullname,given_service,given_experience,pdf_data, given_address, given_pincode))
                cursor.execute('INSERT INTO users(mail, password, usertype) VALUES(?,?,?)',
                               (given_mail, given_password, 'professional'))
                db.commit()
                return "Successful!" 
            else:
                return render_template('register_as_pro.html', user_e='User exists!')
 
        except Exception as e:
            return f"SORRY! SOME ERROR HAS OCCURRED: {str(e)}"

        finally:
            db.close()


    else:
        return render_template('register_as_pro.html')



if __name__ == "__main__":
    main.run(debug=True)