import mysql.connector
import smtplib
import sys
import datetime
import random
from datetime import timedelta
from flask import Flask, render_template,request,jsonify,session,app,redirect,g,url_for,flash
app = Flask(__name__)

app.secret_key="elluminati"
app.permanent_session_lifetime=timedelta(minutes=1)

conn=mysql.connector.connect(
	user="ankur",
	password="Ankur@9352",
	host="localhost",
	database="elluminati")

mycursor=conn.cursor()
mycursor = conn.cursor(buffered=True)
mycursor.execute("use elluminati")
# mycursor.execute("select * from gmail")


gmail_track=[]
cart_track=[]
cart_list=[]
# @app.route("/ss")
# def ss():
# 	mycursor.execute("select * from gmail")

# @app.route("/cc")
# def cc():
# 	s="asdf"
# 	s=s[:3]
# 	return s

# Home Page

@app.route("/")
def index():
	return render_template("home.html")

# LOGIN 
@app.route("/login")
def login():
	# if gmail_track==[]:
		return render_template("login.html")
	# else:
		# return render_template("home.html",name=gmail_track[0])

@app.route("/register")
def reg():
	return render_template("sign_up.html")

# Sign Up
@app.route("/signup")
def inde():
	return render_template("sign_up.html")

# Sign Up- Receive data of signup so to add to database
@app.route("/sign_up/add_data",methods=["POST"])
def get_data():
	mycursor.execute("select * from gmail")
	gm=request.form["gmail_id"]
	# mycursor.execute("use elluminati")
	# mycursor.execute("select * from gmail")
	for i in mycursor:
		if i[0]==gm:
			
			return render_template("sign_up.html")
	gmail_track.append(gm)
	passwrd=request.form["password"]
	na=request.form["name"]
	gmail_track.append(na)
	mob=request.form["mobile"]
	if len(mob)!=10:
		return "Invalid Mobile Number"
	a=mycursor.execute("INSERT INTO gmail (gmail_id, password, name, mobile) VALUES (%s,%s,%s,%s)",(gm,passwrd,na,mob))
	conn.commit()
	conn.close()
	return redirect(url_for("login"))
	# return render_template("home.html",name=gmail_ls[1])
	


# # LOGIN 
# @app.route("/login")
# def login():
# 	return render_template("login.html")

# Login -Verification of login details
@app.route("/login/log",methods=["POST"])
def _data():
	mycursor.execute("select * from gmail")
	gm=request.form["gmail_id"]
	passwrd=request.form["password"]
	for data in mycursor:
		if data[0]==gm:
			if data[1]==passwrd:
				gmail_track.append(gm)
				# x=datetime.datetime.now()
				# minute=x.strftime("%M")
				# minute=int(minute)
				# query = """ UPDATE gmail
			 #    SET ship = %s
			 #    WHERE gmail_id = %s """

				# data = (minute,  gmail_track[0])
				# mycursor.execute (query, data)
				# conn.commit()
				# conn.close()
				

				# # session_permanent = True
				# x=datetime.datetime.now()
				# minute=x.strftime("%M")
				# minute=int(minute)
				# x=2
				# if x< 58:
				# 	minute=minute+2
				# 	sess.append(minute)
				# else:
				# 	minute=minute+x-60
				# 	sess.append(minute)
				# session.pop("user",None)
				# session[gm]=passwrd	
				# session.permanent = True
        # session????
				# app.permanent_session_lifetime = timedelta(minutes=2)
				# app.secret_key="elluminati"

				#app.config['permanent_session_lifetime']=timedelta(minutes=1)
				return render_template("home.html",name=data[2])
			else:
				return render_template("login.html")

		else:
			continue

	return render_template("sign_up.html")

# login - forgot password
@app.route("/login/edit")
def edit():
	return render_template("edit.html")

# login -sent otp to user
@app.route("/login/otp",methods=["POST"])
def otp():
	gm=request.form["gmail_id"]
	gmail_ls.append(gm)
	server = smtplib.SMTP("smtp.gmail.com",587)
	server.ehlo()
	server.starttls()
	email = "ankurgupta9352@gmail.com"
	password = "Ankur@1994"
	server.login(email,password)
	from_address = email
	to_address = gm
	# otp = "Your verifiction otp is : "
	# otp1= random.randint(10000,100000)
	otp="87654"
	gmail_ls.append(otp)
	# otp=otp + str(otp1)
	# otp="www.google.com"
	# print(otp)
	server.sendmail(from_address,to_address,str(otp))
	server.quit()
	return render_template("verify.html") 

# login-forgot password- details cross check amd update new password
@app.route("/login/verify",methods=["POST"])	
def verify():
	rec_otp=request.form["otp"]
	new_pass=request.form["new"]
	re_new_pass=request.form["re-new"]
	if rec_otp == gmail_ls[1]:
		if new_pass==re_new_pass:
			query = """ UPDATE gmail
			        SET password = %s
			        WHERE gmail_id = %s """

			data = (re_new_pass, gmail_ls[0])
			mycursor.execute(query, data)
			conn.commit()
			conn.close()
			gmail_ls=[]
			return "Successfully Reset Password"
		else: 
			return "Password don't match"

	else:
		return "Render Page again"


@app.route("/add_cart/<idd>",methods=["POST"])
def add_cart(idd):
	mycursor.execute("select * from gmail")
	for x in mycursor:
		if x[0]==gmail_track[0]:
			xx=x[4]
			xx=str(xx)+ str(idd)
			
			# cart_track.append(idd)
			# cart_track.append(idd)
			query = """ UPDATE gmail
			        SET cart = %s
			        WHERE gmail_id = %s """

			data = (xx,  gmail_track[0])
			mycursor.execute (query, data)
			conn.commit()
			conn.close()
			idd=idd[:3]
			return redirect("http://6be97d3e.ngrok.io/view/" + idd)

@app.route("/cart")
def my_cart():
	mycursor.execute("select * from gmail")
	for x in mycursor:
		if x[0]==gmail_track[0]:
			y=x[4]
			# y=str(y)
			# for i in range(0,len(y),4):
			# 	z=y[i:i+4]
			# 	cart_list.append(z)
			return redirect("http://283b8d7d.ngrok.io/cart/" + y)

# @app.route("/dd")
# def cj():
# 	return redirect("view/idd")

# @app.route("/view/<iddd>")
# def iddscs(iddd):
# 	return iddd
	
#  Server_data_extract=API
# @app.route("/api/")
# def sql_api():
# 	api_ls={}
# 	# mycursor.execute("use elluminati")
# 	mycursor.execute("select * from gmail")
# 	for i in mycursor:
# 		# i=list[i]
# 		api_ls[i[0]]={
# 		"gmail_id": i[0],
# 		"password": i[1],
# 		"name" : i[2],
# 		"mobile" : i[3]
# 		}
# 	# galaxy=[]
# 	for name,des in api_ls.items():
# 		galaxy.append({name:des})

# 	return jsonify(galaxy)


	

# particular user data extract
# @app.route("/api/<search_id>")
# def api_id(search_id):

# 	for x in galaxy:

# 		for y in x.keys():	
# 			if y==search_id:
# 				# return "hello"
# 				zz=[]
# 				z= x.get(search_id)
# 				for name,des in z.items():
# 					zz.append({name:des})

				# return jsonify(galaxy)
				# return jsonify(zz)


# View of any product ,servers connect through API
# @app.route("/view/<pr_id>",methods=["POST"])
# def view(pr_id):
# 	gmail_ls.append("gmail")
# 	gmail_ls.append(pr_id)
# 	return 

# @app.before_request
# def before_request():
# 	session_permanent=True
# 	x=datetime.datetime.now()
# 	minute=x.strftime("%M")
# 	minute=int(minute)
# 	# x=2
# 	# if x< 58:
# 	# 	minute=minute+2
# 	# 	# sess.append(minute)
# 	# else:
# 	# 	minute=minute+x-60
# 		# sess.append(minute)
# 	while True:
# 		x=datetime.datetime.now()
# 		mint=x.strftime("%M")
# 		mint=int(minute)
# 		if mint==minute:
# 			sys.exit("PAJJNJN")
# 		else:
# 			return render_template("home.html")
			

		

		# return "BHHJVBJH"	

    # app.permanent_session_lifetime = timedelta(minutes=2)
# @app.before_request
# def before_request():
# 	g.user=None
# 	if gmail_ls[0] in session:
# 		x=datetime.datetime.now()
# 		minute=x.strftime("%M")
# 		minute=int(minute)
# 		if minute==sess[0]:
# 			return render_template("login.html")


if __name__ ==  "__main__":
    app.run(debug=True)
