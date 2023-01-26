from flask import *
import sqlite3

connection = sqlite3.connect("login.db")
cursor = connection.cursor()
cursor.execute("""
            CREATE TABLE IF NOT EXISTS Emails (
            "First Name" text,
            "Last Name" text,
            Email TEXT,
            Password TEXT,
            Player1 INTEGER,
            Player2 INTEGER,
            DRAW INTEGER
        )
""")
connection.commit()
connection.close()

app = Flask(__name__,template_folder='templates',static_folder='static')
app.secret_key = "JAVA"


@app.route("/", methods=['GET','POST'])
def home():
    if request.method=='POST':
        select=request.form['page']
        return redirect(url_for(f'{select}'))
    return render_template("home.html")
@app.route("/dice", methods = ["GET", "POST"])
def dice():
    if request.method=='POST':
        session.pop("user")
        return redirect(url_for("home"))
    if "user" in session:
        user = session["user"]
        connection=sqlite3.connect("login.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Emails WHERE Email='{e}'".format(e=user))
        search = cursor.fetchone()
        connection.commit()
        connection.close()
        return render_template("dicee.html",email=user,p1=search[4],p2=search[5],draw=search[6])
    elif "user" not in session:
        return redirect(url_for("home"))

@app.route("/update", methods = ['POST'])
def update():
    data = request.get_json()
    email = data["email"]
    i = data["id"]
    connection=sqlite3.connect("login.db")
    cursor=connection.cursor()
    cursor.execute("BEGIN TRANSACTION")
    cursor.execute("SELECT * FROM Emails WHERE Email='{e}'".format(e=email))
    search = cursor.fetchone()
    column_name = cursor.description[i][0]
    cursor.execute("SELECT {c} FROM Emails WHERE Email='{e}'".format(c=column_name, e=email))
    x = cursor.fetchone()[0]
    x += 1
    cursor.execute("UPDATE Emails SET {c} = {x} WHERE Email='{e}'".format(c=column_name, x=x, e=email))
    connection.commit()
    connection.close()
    return jsonify({"message": "Record updated successfully"})

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method=='POST':
        fname = request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        pwd1 = request.form['password1']
        pwd2 = request.form['password2']
        if pwd1 != pwd2:
            return render_template("signup.html", pwd="Please Enter Correct Password")
        connection = sqlite3.connect("login.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Emails WHERE Email='{e}'".format(e=email))
        search = cursor.fetchone()
        if search:
            return render_template("signup.html", pwd = "Email is already taken, Please try another E-MAIL")
        query1 = "INSERT INTO Emails VALUES('{a}','{b}','{c}','{d}', '{e}', '{f}', '{g}')".format(a=fname, b=lname,c=email, d=pwd1, e=0, f=0, g=0)
        connection.execute(query1)
        connection.commit()
        connection.close()
        return redirect(url_for("signup_success",sss=email))
    return render_template("signup.html")


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        pas = request.form['password']
        connection = sqlite3.connect("login.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Emails WHERE Email = '{e}'".format(e=email))
        search = cursor.fetchone()
        connection.commit()
        connection.close()
        if not search:
            return render_template("login.html", pwd="Please Enter Valid Email")
        elif pas!=search[3]:
            return render_template("login.html",pwd="Please Enter Correct Password")
        return redirect(url_for("login_success",pas=email))
    return render_template("login.html")
@app.route("/loginsuccess<pas>",methods=['GET','POST'])
def login_success(pas):
    if request.method=='GET':
        connection = sqlite3.connect("login.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Emails Where Email = '{e}'".format(e=pas))
        search = cursor.fetchone()
        connection.commit()
        connection.close()
        return render_template("loginsuccess.html", name=search[1])
    if request.method=='POST':
        return redirect(url_for("profile",usr=pas))
    return render_template("loginsuccess.html")
@app.route("/signupsuccess<sss>", methods=['GET', 'POST'])
def signup_success(sss):
    if request.method=='GET':
        connection = sqlite3.connect("login.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Emails WHERE Email = '{s}'".format(s=sss))
        search = cursor.fetchone()
        connection.commit()
        connection.close()
        return render_template("signupsuccess.html",name = search[1])
    if request.method=='POST':
        return redirect(url_for("profile",usr=sss))
    return render_template("signupsuccess.html")
@app.route("/profile<usr>",methods=['GET','POST'])
def profile(usr):
    if request.method=='GET':
        connection = sqlite3.connect("login.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Emails WHERE Email = '{s}'".format(s=usr))
        search = cursor.fetchone()
        connection.commit()
        connection.close()
        return render_template("profile.html", fname=search[0], lname=search[1], email=search[2], password=search[3],p1 = search[4],p2 = search[5],draw = search[6])
    if request.method=='POST':
        session["user"]=usr
        return redirect(url_for("dice"))
    return render_template("profile.html")
if __name__=="__main__":
    app.run(debug=True,port=5000)