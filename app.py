#!usr/bin/env python3
from flask import Flask,render_template,flash,redirect,request,url_for,session,logging
from flask_mysqldb import MySQL#pip install flask-mysqldb ,pip install WTFROMS
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,SelectField,BooleanField,SelectMultipleField,widgets
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired,Length,Email
from passlib.hash import sha256_crypt#pip install passlib
from db import *
from flask import Flask
from flask_mail import Mail, Message#pip install flask_mail
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user#pip install flask_login
import os
from functools import wraps
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup#pip install beautifulsoup4
import requests#scrapy#pip install requests
from flask import jsonify#neewsfeeds
from scrapingneews import scrape12#neewsfeeds


import datetime
from datetime import date, timedelta
now = datetime.date.today()
dt=now
district1=[]

db = Db()
district1 = []
for i in db.execute("SELECT dist,dist_id FROM state_dist"):
    district1.append(i)
db.commit()
db.close()
print(district1)



# from flask_wtf.csrf import CSRFProtect#pip install flask_csrf
aa=0
mark={}
# for i in db.execute("SELECT * FROM course_names"):
#     courseList.append(i)


app=Flask(__name__)
app.config.from_object(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'agmark'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql=MySQL(app)

@app.route('/home12')
def home12():
    return render_template('home.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
#--------------------------static routes-------------------------
@app.route('/about')
def about():
    return render_template('navbarpages/about.html')
class Contact_usForm(Form):
  state=StringField('State', [validators.Length(min=1, max=50),InputRequired()])
  district=StringField('District', [validators.Length(min=1, max=50),InputRequired()])
@app.route('/contact_us',methods = ['GET','POST'])
def contact_us():
  # form=Contact_usForm(request.form)
  # if request.method == 'POST' and form.validate():
  #   username=form.state.data
  #   password_candidate=form.district.data
  #   print(username,password_candidate)
    # return redirect(url_for('scrape12'))
    return render_template('navbarpages/contact_us.html')

@app.route('/our_vision')
def our_vision():
    return render_template('navbarpages/our_vision.html')
@app.route('/how_to_reg')
def how_to_reg():
    return render_template('how_to_reg.html')
#-----services-----------------
comm_c={}
class Cate_agriForm(Form):
  state = SelectField(u'State', choices=[('','Choose your State'),('Andhra Pradesh','Andhra Pradesh'),('Telangana','Telangana')])
  district = SelectField(u'District', choices=district1)

@app.route('/cate_agri',methods = ['GET','POST'])
def cate_agri():
  form=Cate_agriForm(request.form)
  if request.method == 'POST' and form.validate():
    username=form.state.data
    password_candidate=form.district.data
    print(username,password_candidate)

    cur = mysql.connection.cursor()

       # get user by username
    cur.execute("SELECT DISTINCT COMMODITY  FROM `updatetables` WHERE state = %s AND DISTRICT=%s",[username,password_candidate])
    agri=cur.fetchall()
    agri=list(agri)
    comm_b={}
    aa=len(agri)
    if(aa>0):
      print(aa)
      for i in range(0,aa):

        comm=(agri[i]['COMMODITY'])

        cur.execute("SELECT  COMMODITY,MIN_PRICE,MAX_PRICE,MODAL_PRICE  FROM `updatetables` WHERE state = %s AND DISTRICT=%s AND COMMODITY=%s",[username,password_candidate,comm])
        comm_argi=cur.fetchall()
        comm_argi=list(comm_argi)
        comm_b[i]=comm_argi
        comm_c[i]=comm_b[i][0]



      # return redirect(url_for('scrape12'))
      comm_lc=len(comm_c)
      return render_template('cate_agri.html',comm_c=comm_c,form=form,comm_lc=comm_lc,aa=aa)
    # elif(len(agri)>0 and len(agri)<=3):
    #   print(len(agri))
    #   for i in range(0,3):

    #     comm=(agri[i]['COMMODITY'])

    #     cur.execute("SELECT  COMMODITY,MIN_PRICE,MAX_PRICE,MODAL_PRICE  FROM `updatetables` WHERE state = %s AND DISTRICT=%s AND COMMODITY=%s",[username,password_candidate,comm])
    #     comm_argi=cur.fetchall()
    #     comm_argi=list(comm_argi)
    #     comm_b[i]=comm_argi
    #     comm_c[i]=comm_b[i][0]



    #   # return redirect(url_for('scrape12'))
    #   comm_lc=len(comm_c)
    #   return render_template('cate_agri.html',comm_c=comm_c,form=form,comm_lc=comm_lc)
    else:
      comm_c.clear()
      comm_lc=len(comm_c)
      return render_template('cate_agri.html',form=form,comm_c=comm_c,comm_lc=comm_lc,aa=aa)

  comm_c.clear()
  comm_lc=len(comm_c)
  return render_template('cate_agri.html',form=form,comm_c=comm_c,comm_lc=comm_lc)
@app.route('/cate_agri1')
def cate_agri1():
    return render_template('navbarpages/cate_agri1.html')

@app.route('/cate_dairy')
def cate_dairy():
    return render_template('navbarpages/cate_dairy.html')
@app.route('/cate_ani')
def cate_ani():
    return render_template('navbarpages/cate_ani.html')
#-----service-------------------------------
@app.route('/service_farmer')
def service_farmer():
    return render_template('navbarpages/service_farmar.html')
@app.route('/service_process')
def service_process():
    return render_template('navbarpages/service_process.html')
@app.route('/service_storage')
def service_storage():
    return render_template('navbarpages/service_storage.html')
@app.route('/service_supplier')
def service_supplier():
    return render_template('navbarpages/service_supplier.html')
@app.route('/service_trader')
def service_trader():
    return render_template('navbarpages/service_trader.html')
@app.route('/service_logistics')
def services_logistics():
    return render_template('navbarpages/service_logistics.html')
@app.route('/service_vendor')
def services_vendor():
    return render_template('navbarpages/service_vendor.html')


#-------------------------end static routes----------------------
#-----------------------------login-login----------------
@app.route('/login1',methods = ['GET','POST'])
def login1():
   if request.method == 'POST':
       #get form fields

       username = request.form['username']
       password_candidate = request.form['password']

       # Create cursor
       cur = mysql.connection.cursor()

       # get user by username

       result = cur.execute("SELECT * FROM users WHERE name = %s",[username])
       print('name:',username)
       if result > 0:

           data = cur.fetchone()
           password = data['status']

           # print('password1',password1);
           print('password:',password_candidate)

           # if sha256_crypt.verify(password_candidate,password):
           if (password_candidate==password):


               #app.logger.info('Passwords Matched')
               session['logged_in'] = True
               session['username'] = username
               # print('password11',password_candidate);
               # print('password12:',password)

               flash('You are now logged in','success')
               return redirect(url_for('scrape12'))
           else:
               error = 'Invalid Login'
               #app.logger.info('Passwords Not matched')
               return render_template('login1.html',error=error)
           # close connection
           cur.close()
       else:
           #app.logger.info('No user')
           error = 'Username not found'
           return render_template('login1.html',error=error)

   return render_template('login1.html')
def is_logged_in1(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       if 'logged_in1' in session:
           return f(*args, **kwargs)
       else:
           flash('Unauthorized, Please Login','danger')
           return redirect(url_for('login1'))
   return wrap

   return render_template('login1.html')
# Logout
@app.route('/logout1')
def logout1():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login1'))
# ------------------------market-prices-----------------------------------


# @app.route('/market')


# def market():
#     now = datetime.date.today()
#     now1=date.today() - timedelta(1)
#     a='mark_prices%s'%now
#     f='mark_prices%s'%now1
#     punctuations = '''#-'"\,'''
#     my_str = a
#     no_punct = ""
#     for char in my_str:
#        if char not in punctuations:
#            no_punct = no_punct + char
#     my_str1 = f
#     no_punct1 = ""
#     for char in my_str1:
#        if char not in punctuations:
#            no_punct1 = no_punct1 + char
#     e=no_punct1
#     d=no_punct
#     c=' TABLE ' + d

#     cur = mysql.connection.cursor()
#     cur.execute("SHOW TABLES")
#     rv1=cur.fetchall()
#     for i in range(0,len(rv1)):
#       rv2=rv1[i]['Tables_in_agmark']
#       if(str(rv2)==str(d)):
#         print(rv2,'==',d)
#         z=1
#     if(z==1):
#       print("exit")   
#       cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Paddy'AND `VARIETY`='Paddy'"%d)
#       paddy=cur.fetchall()
#     else:
#       cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Paddy'AND `VARIETY`='Paddy'"%e)
#       paddy=cur.fetchall()
#     print(paddy)


#     cur.execute("DROP TABLE IF EXISTS %s"%d)    
#     cur.execute( "CREATE %s SELECT * FROM %s"%(c,e))
#     dt=now
#     cur.execute('''SELECT * FROM %s'''%d)
#     # try:
#     #   cur.execute('''SELECT * FROM %s'''%d)
#     #   dt=now
#     #   print(1)
#     #   rv=cur.fetchall()
#     # except:
#     #   cur.execute('''SELECT * FROM %s'''%e)
#     #   dt=now1
#     #   print(2)
#     rv=cur.fetchall()

#     cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Paddy'AND `VARIETY`='Paddy'"%d)
#     paddy=cur.fetchall()
#        #commit to DB

#     mysql.connection.commit()

#        #close connection
#     cur.close()

#     return render_template('admin.html',rv=rv,dt=dt,paddy=paddy)
#-------------------------admin-refresh-button-----------
@app.route('/refreshbutton')


def refreshbutton():
  now = datetime.date.today()
  now1=date.today() - timedelta(1)
  now2=date.today()
  a='mark_prices%s'%now
  f='mark_prices%s'%now1
  punctuations = '''#-'"\,'''
  my_str = a
  no_punct = ""
  for char in my_str:
     if char not in punctuations:
         no_punct = no_punct + char
  my_str1 = f
  no_punct1 = ""
  for char in my_str1:
     if char not in punctuations:
         no_punct1 = no_punct1 + char
  e=no_punct1
  d=no_punct
  c=' TABLE ' + d
  z=0
  dt=now
  

  cur = mysql.connection.cursor()
  cur.execute("SHOW TABLES")
  rv1=cur.fetchall()
  print(len(rv1))
  for i in range(0,len(rv1)):
      rv2=rv1[i]['Tables_in_agmark']
      if(str(rv2)==str(d)):
        print(rv2,'==',d)
        z=1
  if(z==1):
    print("exit")   
    cur.execute('''SELECT * FROM %s'''%d)
    rv=cur.fetchall()
  else:
    cur.execute("SELECT * FROM `updatetables`")
    update=cur.fetchall()
    update=list(update)
    update=str(update[0]['DATE'])
    now=str(now)
    print(update,now)
    cur.execute("UPDATE `updatetables` SET `DATE`='%s' WHERE `DATE`='%s'"%(now,update))
    cur.execute("SELECT * FROM `updatetables`")
    cur.execute( "CREATE %s SELECT * FROM `updatetables`"%(c))
    # cur.execute( "DELETE FROM 'updatetables'")
    # cur.execute( "CREATE TABLE 'updatetables' SELECT * FROM %s"%(d))
    cur.execute('''SELECT * FROM %s'''%d)
    rv=cur.fetchall()
    print("ceate table succeully")

      #commit to DB

  mysql.connection.commit()

     #close connection
  cur.close()

        # cur.execute("DROP TABLE IF EXISTS %s"%d)    

      
      
  return render_template('admin.html',dt=dt,rv=rv)

#-------------------------admin--refresh-----------
@app.route('/admin')

def refresh():
    now = datetime.date.today()
    now1=date.today() - timedelta(1)
    a='mark_prices%s'%now
    f='mark_prices%s'%now1
    punctuations = '''#-'"\,'''
    my_str = a
    no_punct = ""
    for char in my_str:
       if char not in punctuations:
           no_punct = no_punct + char
    my_str1 = f
    no_punct1 = ""
    for char in my_str1:
       if char not in punctuations:
           no_punct1 = no_punct1 + char
    e=no_punct1
    d=no_punct
    

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `updatetables`")
    dt=now
    print(2)
    rv=cur.fetchall()

       #commit to DB

    mysql.connection.commit()

       #close connection
    cur.close()

    return render_template('cate_ani.html')

    # return render_template('adminupdate.html',dt=dt,rv=rv)


# #----------------updated-market-prices-----------------------
@app.route('/update_market_price')
def update_market_price():

  now = datetime.date.today()
  a='mark_prices%s'%now
  punctuations = '''#-'"\,'''
  my_str = a
  no_punct = ""
  for char in my_str:
     if char not in punctuations:
         no_punct = no_punct + char

  d=no_punct     
  id=request.args.get('id')
  cur=mysql.connection.cursor()
  cur.execute("SELECT * FROM %s WHERE id=%s"%(d,id))
  rv=cur.fetchall()
  person=list(rv)
  person=person[0]

  return render_template('update.html',person=person)



  #==================update12===============================
@app.route('/update12')

def update12():
  now = datetime.date.today()
  a='mark_prices%s'%now
  punctuations = '''#-'"\,'''
  my_str = a
  no_punct = ""
  for char in my_str:
     if char not in punctuations:
         no_punct = no_punct + char

  d=no_punct      
  DISTRICT=request.args.get('name1')
  MARKET=request.args.get('name2')
  COMMODITY=request.args.get('name3')
  VARIETY=request.args.get('name4')
  UNITS=request.args.get('name5')
  MIN_PRICE=request.args.get('MIN_PRICE')
  MAX_PRICE=request.args.get('MAX_PRICE')
  MODAL_PRICE=request.args.get('MODAL_PRICE')
  UNITY_OF_PRICE=request.args.get('name6')
  DATE=request.args.get('name7')
  ID=request.args.get('ID')
    
  cur=mysql.connection.cursor()
  cur.execute("SELECT * FROM %s WHERE id=%s"%(d,ID))
  rv=cur.fetchall()
  a=list(rv)
  print("rvv",list(rv))
  b=a[0]['MAX_PRICE']
  c=a[0]['ID']
  a1=a[0]['DISTRICT']

  cur=mysql.connection.cursor()
  cur.execute("UPDATE `%s` SET `MAX_PRICE`=%s,`MIN_PRICE`=%s,`MODAL_PRICE`=%s WHERE `ID`=%s "%(d,MAX_PRICE,MIN_PRICE,MODAL_PRICE,c))
  cur.execute("UPDATE `updatetables` SET `MAX_PRICE`=%s,`MIN_PRICE`=%s,`MODAL_PRICE`=%s WHERE `ID`=%s "%(MAX_PRICE,MIN_PRICE,MODAL_PRICE,c))
  
  mysql.connection.commit()

  cur.close()

  return redirect(url_for('home'))

# ------------------------------REgistations==6----------------------------------


# -------------------Farmer Registration-------------------------

class FarmerRegistrationForm(Form):
  firstName=StringField('First Name',[validators.Length(min=1,max=20)])
  lastName= StringField('Last Name',[validators.Length(min=1,max =10 )])
  dateofBirth= DateField('Date of Birth', format='%Y-%m-%d')
  email=StringField('Email',[validators.Length(min=2,max=50)])
  contactnumber=StringField(u'Mobile',[
            validators.Length(min=1, max=20),
            validators.DataRequired(),
            validators.EqualTo('confirmcontactnumber', message='Contact Number didn\'t match')
        ])
  aadharNumber=StringField('Aadhar number',[validators.Length(min=1,max=16)])
  address=StringField(u'Address of the Unit',[validators.Length(min=1,max=200)])
  photo = FileField(u'Photo')
  croptype = SelectMultipleField(u'', choices=[('Paddy','Paddy'), ('Wheat', 'Wheat'), ('Cotton', 'Cotton'), ('Mirchi', 'Mirchi'), ('Vegetables', 'Vegetables')], option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False))
  animalhusbandrytype = SelectMultipleField(u'', choices=[('Cattle','Cattle'), ('Fish', 'Fish'), ('Poultry', 'Poultry'), ('Goat', 'Goat'), ('Sheep', 'Sheep')], option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False))
  dairyform = SelectMultipleField(u'', choices=[('Cow Milk','Cow Milk'), ('Buffalo Milk', 'Buffalo Milk'), ('Goat Milk', 'Goat Milk')], option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False))
  state = SelectField(u'Choose your State', choices=[('None','None'),('Andhra Pradesh','Andhra Pradesh'),('Telangana','Telangana')])
  district = SelectField(u'District', choices=[('None','None'),('Anantapur','Anantapur'),('Chittoor','Chittoor'),('East Godavari','East Godavari'),('Guntur','Guntur'),('Krishna','Krishna'),('Kurnool','Kurnool'),('Nellore','Nellore'),('Prakasam','Prakasam'),('Srikakulam','Srikakulam'),('Visakhapatnam','Visakhapatnam'),('Vizianagaram','Vizianagaram'),('West Godavari','West Godavari'),('YSR Kadapa','YSR Kadapa'),])
  village=StringField('Village',[validators.Length(min=1,max=16)])
  taluka=StringField('Taluka',[validators.Length(min=1,max=16)])
  pincode=StringField('Pincode',[validators.Length(min=1,max=10)])
  confirmcontactnumber=StringField(u'Confirm Contact Number',[validators.Length(min=1,max=20)])
@app.route('/farmerregistration', methods=['GET', 'POST'])
def farmerregistration():
  form=FarmerRegistrationForm(request.form)
  if request.method == 'POST' and form.validate():
    farmerFirstname=form.firstName.data
    farmerLastname=form.lastName.data
    farmerDateofBirth=form.dateofBirth.data
    # farmerEmail=form.email.data
    farmerContactNumber=form.contactnumber.data
    farmeraadharNumber=form.aadharNumber.data
    farmerAddress=form.address.data
    farmerCroptype=form.croptype.data
    farmerAnimalHusbandryType=form.animalhusbandrytype.data
    farmerDairyform=form.dairyform.data
    farmerState=form.state.data
    farmerDistrict=form.district.data
    farmerVillage=form.village.data
    farmerTaluka=form.taluka.data
    farmerPincode=form.pincode.data
    selectedCropType="_".join(farmerCroptype)
    selectedAnimalHusbandryType="_".join(farmerAnimalHusbandryType)
    selectedDairyform="_".join(farmerDairyform)
    status="farmer"

    cur = mysql.connection.cursor()
     #commit to DB
    cur.execute("INSERT INTO `far_regs`(`far_first`, `far_last`, `far_dob`, `far_mobile`, `far_aadher`, `far_add`, `far_state`, `far_dist`, `far_village`, `far_taluka`, `far_pin`, `far_croptype`, `far_ani_hus`, `far_dairy`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(farmerFirstname,farmerLastname,farmerDateofBirth,farmerContactNumber,farmeraadharNumber,farmerAddress,farmerState,farmerDistrict,farmerVillage,farmerTaluka,farmerPincode, selectedCropType, selectedAnimalHusbandryType, selectedDairyform))
    cur.execute("INSERT INTO `users`(`name`, `mobile`, `status`)VALUES(%s, %s, %s)",(farmerFirstname,farmerContactNumber,status))

    mysql.connection.commit()

     #close connection
    cur.close()


    flash('Thank you for register')

    return render_template('home1.html')
  return render_template('far_reg.html', form=form)


# -------------------Food Processor Registration-------------------------

class FoodProcessorRegistrationForm(Form):
  fullname=StringField(u'Full Name',[validators.Length(min=1,max=50)])
  companyname=StringField(u'Company Name',[validators.Length(min=1,max=100)])
  companyaddress=StringField(u'Address of the Unit',[validators.Length(min=1,max=200)])
  state = SelectField(u'State', choices=[('','Choose your State'),('Andhra Pradesh','Andhra Pradesh'),('Telangana','Telangana')])
  district = SelectField(u'District', choices=[('','Choose your district'),('Anantapur','Anantapur'),('Chittoor','Chittoor'),('East Godavari','East Godavari'),('Guntur','Guntur'),('Krishna','Krishna'),('Kurnool','Kurnool'),('Nellore','Nellore'),('Prakasam','Prakasam'),('Srikakulam','Srikakulam'),('Visakhapatnam','Visakhapatnam'),('Vizianagaram','Vizianagaram'),('West Godavari','West Godavari'),('YSR Kadapa','YSR Kadapa'),])
  village=StringField('Village',[validators.Length(min=1,max=16)])
  taluka=StringField('Taluka',[validators.Length(min=1,max=16)])
  pincode=StringField('Pincode',[validators.Length(min=1,max=10)])
  yearofIncorporation=DateField('Year of Incorporation', format='%Y-%m-%d')
  contactnumber=StringField(u'Contact Number',[
            validators.Length(min=1, max=20),
            validators.DataRequired(),
            validators.EqualTo('confirmcontactnumber', message='Contact Number didn\'t match')
        ])
  materialprocures = SelectMultipleField(u'', choices=[('Paddy','Paddy'), ('Wheat', 'Wheat'), ('Cotton', 'Cotton'), ('Mirchi', 'Mirchi'), ('Vegetables', 'Vegetables')], option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False))
  gstnumber=StringField(u'GST Number',[validators.Length(min=1,max=50)])
  confirmcontactnumber=StringField(u'Confirm Contact Number',[validators.Length(min=1,max=20)])
  email=StringField(u'Email',[validators.Length(min=1,max=50)])

@app.route('/foodprocesserregistration', methods=['GET', 'POST'])
def foodprocesserregistration():
  form=FoodProcessorRegistrationForm(request.form)
  if request.method == 'POST' and form.validate():
    FPRfullname=form.fullname.data
    FPRcompanyname=form.companyname.data
    FPRcompanyaddress=form.companyaddress.data
    FPRstate=form.state.data
    FPRdistrict=form.district.data
    FPRvillage=form.village.data
    FPRtaluka=form.taluka.data
    FPRpincode=form.pincode.data
    FPRyearofIncorporation=form.yearofIncorporation.data
    FPRcontactnumber=form.contactnumber.data
    FPRgstnumber=form.gstnumber.data
    FPRemail=form.email.data
    FPRmaterialprocures=form.materialprocures.data
    selectedProcureMaterial="_".join(FPRmaterialprocures)
    FPRstatus="processor"
    cur = mysql.connection.cursor()
     #commit to DB
    cur.execute("INSERT INTO `processor_reg`(`proc_name`, `proc_company`, `proc_unit_addr`, `proc_state`, `proc_district`, `proc_village`, `proc_taluka`, `proc_pincode`, `proc_yearofincorp`, `proc_gstnum`, `proc_contactnum`, `proc_mail`, `proc_procurematerial`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(FPRfullname, FPRcompanyname, FPRcompanyaddress, FPRstate, FPRdistrict, FPRvillage, FPRtaluka, FPRpincode, FPRyearofIncorporation, FPRgstnumber, FPRcontactnumber, FPRemail, selectedProcureMaterial))
    cur.execute("INSERT INTO `users`(`name`, `email`, `mobile`, `status`)VALUES(%s, %s, %s, %s)",(FPRfullname,FPRemail,FPRcontactnumber,FPRstatus))
    mysql.connection.commit()
     #close connection
    cur.close()
    flash('Thank you for register')
    print (FPRfullname, FPRcompanyname, FPRcompanyaddress, FPRstate, FPRdistrict, FPRdistrict, FPRvillage, FPRtaluka, FPRpincode, FPRyearofIncorporation, FPRgstnumber, FPRemail )
    return render_template('home1.html')
  return render_template('food_reg.html', form=form)



#--------------------------Storage/Ware House Registration-----------------------

class WarehouseRegistration(Form):
  fullname=StringField(u'Full Name',[validators.Length(min=1,max=50)])
  companyname=StringField(u'Company Name',[validators.Length(min=1,max=100)])
  companyaddress=StringField(u'Address of the Unit',[validators.Length(min=1,max=200)])
  state = SelectField(u'State', choices=[('','Choose your State'),('Andhra Pradesh','Andhra Pradesh'),('Telangana','Telangana')])
  district = SelectField(u'District', choices=[('','Choose your district'),('Anantapur','Anantapur'),('Chittoor','Chittoor'),('East Godavari','East Godavari'),('Guntur','Guntur'),('Krishna','Krishna'),('Kurnool','Kurnool'),('Nellore','Nellore'),('Prakasam','Prakasam'),('Srikakulam','Srikakulam'),('Visakhapatnam','Visakhapatnam'),('Vizianagaram','Vizianagaram'),('West Godavari','West Godavari'),('YSR Kadapa','YSR Kadapa'),])
  village=StringField('Village',[validators.Length(min=1,max=16)])
  taluka=StringField('Taluka',[validators.Length(min=1,max=16)])
  pincode=StringField('Pincode',[validators.Length(min=1,max=10)])
  contactnumber=StringField(u'Contact Number',[
            validators.Length(min=1, max=20),
            validators.DataRequired(),
            validators.EqualTo('confirmcontactnumber', message='Contact Number didn\'t match')
        ])
  email=StringField(u'Email',[validators.Length(min=1,max=50)])
  yearofIncorporation=DateField('Year of Incorporation', format='%Y-%m-%d')
  gstnumber=StringField(u'GST Number',[validators.Length(min=1,max=50)])
  materialstores = SelectMultipleField(u'', choices=[('Paddy','Paddy'), ('Wheat', 'Wheat'), ('Cotton', 'Cotton'), ('Mirchi', 'Mirchi'), ('Vegetables', 'Vegetables')], option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False))
  storagecapacity=StringField(u'Storage Capacity',[validators.Length(min=1,max=50)])
  quantity = SelectField(u'Quantity', choices=[('','Quantity'),('Tonnes','Tonnes'),('Quintal','Quintal')])
  confirmcontactnumber=StringField(u'Confirm Contact Number',[validators.Length(min=1,max=20)])


@app.route('/warehouseregistration', methods=['GET', 'POST'])
def warehouseregistration():
  form=WarehouseRegistration(request.form)
  if request.method == 'POST' and form.validate():
    SWRfullname=form.fullname.data
    SWRcompanyname=form.companyname.data
    SWRcompanyaddress=form.companyaddress.data
    SWRstate=form.state.data
    SWRdistrict=form.district.data
    SWRvillage=form.village.data
    SWRtaluka=form.taluka.data
    SWRpincode=form.pincode.data
    SWRcontactnumber=form.contactnumber.data
    SWRemail=form.email.data
    SWRyearofIncorporation=form.yearofIncorporation.data
    SWRgstnumber=form.gstnumber.data
    SWRmaterialstores=form.materialstores.data
    SWRstoragecapcity=form.storagecapacity.data
    SWRquantity=form.quantity.data
    selectedStorageMaterial="_".join(SWRmaterialstores)
    SWRstatus="warehouse"
    cur = mysql.connection.cursor()
     #commit to DB
    cur.execute("INSERT INTO `storage_reg`(`storage_fullname`, `storage_cmpname`, `storage_companyaddr`, `storage_state`, `storage_district`, `storage_village`, `storage_taluka`, `storage_pincode`, `storage_contactnum`, `storage_mail`, `storage_yearofincorp`,`storage_gstnum`, `storage_storematerial`, `storage_capacity`, `storage_quanity`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(SWRfullname, SWRcompanyname, SWRcompanyaddress, SWRstate, SWRdistrict, SWRvillage, SWRtaluka, SWRpincode, SWRcontactnumber, SWRemail, SWRyearofIncorporation, SWRgstnumber, selectedStorageMaterial, SWRstoragecapcity, SWRquantity))
    cur.execute("INSERT INTO `users`(`name`, `email`, `mobile`, `status`)VALUES(%s, %s, %s, %s)",(SWRfullname,SWRemail,SWRcontactnumber,SWRstatus))
    mysql.connection.commit()
     #close connection
    cur.close()
    flash('Thank you for register')
    print(SWRfullname, SWRcompanyname, SWRcompanyaddress, SWRstate, SWRdistrict, SWRvillage, SWRtaluka, SWRpincode, SWRcontactnumber, SWRemail, SWRyearofIncorporation, SWRgstnumber, SWRmaterialstores, SWRstoragecapcity, SWRquantity)
    return render_template('home1.html')
  return render_template('warehouse_reg.html', form=form)

#--------------------------Trader House Registration-----------------------

class TraderRegistrationForm(Form):
  fullname=StringField(u'Full Name',[validators.Length(min=1,max=50)])
  companyname=StringField(u'Company Name',[validators.Length(min=1,max=100)])
  companyaddress=StringField(u'Address of the Unit',[validators.Length(min=1,max=200)])
  state = SelectField(u'State', choices=[('','Choose your State'),('Andhra Pradesh','Andhra Pradesh'),('Telangana','Telangana')])
  district = SelectField(u'District', choices=[('','Choose your district'),('Anantapur','Anantapur'),('Chittoor','Chittoor'),('East Godavari','East Godavari'),('Guntur','Guntur'),('Krishna','Krishna'),('Kurnool','Kurnool'),('Nellore','Nellore'),('Prakasam','Prakasam'),('Srikakulam','Srikakulam'),('Visakhapatnam','Visakhapatnam'),('Vizianagaram','Vizianagaram'),('West Godavari','West Godavari'),('YSR Kadapa','YSR Kadapa'),])
  village=StringField('Village',[validators.Length(min=1,max=16)])
  taluka=StringField('Taluka',[validators.Length(min=1,max=16)])
  pincode=StringField('Pincode',[validators.Length(min=1,max=10)])
  yearofIncorporation=DateField('Year of Incorporation', format='%Y-%m-%d')
  contactnumber=StringField(u'Contact Number',[
            validators.Length(min=1, max=20),
            validators.DataRequired(),
            validators.EqualTo('confirmcontactnumber', message='Contact Number didn\'t match')
        ])
  materialprocures = SelectMultipleField(u'', choices=[('Paddy','Paddy'), ('Wheat', 'Wheat'), ('Cotton', 'Cotton'), ('Mirchi', 'Mirchi'), ('Vegetables', 'Vegetables')], option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False))
  gstnumber=StringField(u'GST Number',[validators.Length(min=1,max=50)])
  confirmcontactnumber=StringField(u'Confirm Contact Number',[validators.Length(min=1,max=20)])
  email=StringField(u'Email',[validators.Length(min=1,max=50)])

@app.route('/traderregistration', methods=['GET', 'POST'])
def traderregistration():
  form=TraderRegistrationForm(request.form)
  if request.method == 'POST' and form.validate():
    traderfullname=form.fullname.data
    tradercompanyname=form.companyname.data
    tradercompanyaddress=form.companyaddress.data
    traderstate=form.state.data
    traderdistrict=form.district.data
    tradervillage=form.village.data
    tradertaluka=form.taluka.data
    traderpincode=form.pincode.data
    traderyearofIncorporation=form.yearofIncorporation.data
    tradercontactnumber=form.contactnumber.data
    tradergstnumber=form.gstnumber.data
    traderemail=form.email.data
    tradermaterialprocures=form.materialprocures.data
    selectedMaterialProcures="_".join(tradermaterialprocures)
    traderstatus="trader"
    cur = mysql.connection.cursor()
     #commit to DB
    cur.execute("INSERT INTO `trader_reg`(`trader_name`, `trader_cmpname`, `trader_addr`, `trader_state`, `trader_district`, `trader_village`, `trader_taluka`, `trader_pincode`, `trader_contactnum`, `trader_mail`, `trader_yearofincorp`, `trader_gstnum`, `trader_procurematerial`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(traderfullname, tradercompanyname, tradercompanyaddress, traderstate, traderdistrict, tradervillage, tradertaluka, traderpincode, tradercontactnumber, traderemail, traderyearofIncorporation, tradergstnumber, selectedMaterialProcures))
    cur.execute("INSERT INTO `users`(`name`, `email`, `mobile`, `status`)VALUES(%s, %s, %s, %s)",(traderfullname, traderemail, tradercontactnumber,traderstatus))
    mysql.connection.commit()
     #close connection
    cur.close()
    flash('Thank you for register')
    print (traderfullname, tradercompanyname, tradercompanyaddress, traderstate, traderdistrict, tradervillage, tradertaluka, traderpincode, traderyearofIncorporation, tradergstnumber, traderemail )
    return render_template('home1.html')
  return render_template('trader_reg.html', form=form)

# ------------------------Logistics/Transport Registration----------------------------

class LogisticsRegistrationForm(Form):
  fullname=StringField('Full Name', [validators.Length(min=1, max=50)])
  contactnumber=StringField(u'Contact Number',[
            validators.Length(min=1, max=20),
            validators.DataRequired(),
            validators.EqualTo('confirmcontactnumber', message='Contact Number didn\'t match')
        ])
  email=StringField('Email',[validators.Length(min=2,max=50)])
  companyName=StringField('Comapny Name',[validators.Length(min=2,max=50)])
  vehicleType = SelectField(u'Vehicle Type', choices=[('','Vehicle Type'),('Ape/Tata Ace','Ape/Tata Ace'),('Truck/DCM','Truck/DCM'),('Lorry', 'Lorry')])
  confirmcontactnumber=StringField(u'Confirm Contact Number',[validators.Length(min=1,max=20)])

@app.route('/logisticsregistration', methods=['GET', 'POST'])
def logisticsregistration():
  form=LogisticsRegistrationForm(request.form)
  if request.method == 'POST' and form.validate():
    LTRfullname=form.fullname.data
    LTRcontactnumber=form.contactnumber.data
    LTRemail=form.email.data
    LTRcompanyName=form.companyName.data
    LTRvehicleType=form.vehicleType.data
    logisticstatus="logistic"
    cur = mysql.connection.cursor()
     #commit to DB
    cur.execute("INSERT INTO `logistics_reg`(`logistic_fullname`, `logistic_contactnum`, `logistic_mail`, `logistic_cmpname`, `logisitic_vehicletype`) VALUES(%s, %s, %s, %s, %s)",(LTRfullname, LTRcontactnumber, LTRemail, LTRcompanyName, LTRvehicleType))
    cur.execute("INSERT INTO `users`(`name`, `email`, `mobile`, `status`)VALUES(%s, %s, %s, %s)",(LTRfullname, LTRemail, LTRcontactnumber,logisticstatus))
    mysql.connection.commit()
     #close connection
    cur.close()
    flash('Thank you for register')
    print (LTRfullname, LTRcontactnumber, LTRemail, LTRcompanyName, LTRvehicleType)
    return render_template('home1.html')
  return render_template('logistics_reg.html', form=form)


#==========================end registations=======================================

class LogForm(Form):
  username=StringField('User name', [validators.Length(min=1, max=50),InputRequired()])
  password=PasswordField('Pass word', [validators.Length(min=1, max=50),InputRequired()])
 
@app.route('/log', methods=['GET', 'POST'])
def log():
  form=LogForm(request.form)
  if request.method == 'POST' and form.validate():
    username = form.username.data
    password_candidate=form.password.data

    cur = mysql.connection.cursor()

       # get user by username

    result = cur.execute("SELECT * FROM users WHERE name = %s",[username])
    print('name:',username)
    if result > 0:

        data = cur.fetchone()
        password = data['status']

         # print('password1',password1);
        print('password:',password_candidate)

         # if sha256_crypt.verify(password_candidate,password):
        if (password_candidate==password):


             #app.logger.info('Passwords Matched')
            session['logged_in'] = True
            session['username'] = username
             # print('password11',password_candidate);
             # print('password12:',password)

            flash('You are now logged in','success')
            return render_template('home1.html')
        else:
            error = 'Invalid Login'
             #app.logger.info('Passwords Not matched')
            return render_template('index1.html', form=form,l=l,a1=a1,dt=dt,mark=mark,error=error)
         # close connection
        cur.close()
    else:
         #app.logger.info('No user')
        error = 'Username not found'
  return render_template('index1.html', form=form,l=l,a1=a1,dt=dt,mark=mark)
def is_logged_in(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       if 'logged_in' in session:
           return f(*args, **kwargs)
       else:
           flash('Unauthorized, Please Login','danger')
           return redirect(url_for('scrape12'))
   return wrap

   return render_template('index1.html', form=form,l=l,a1=a1,dt=dt,mark=mark)
#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('scrape12'))



# -----------------------------Login/logout-------------------------------- 


@app.route('/index')


def home():
    return render_template('home1.html')



#--------------------------neewsfeed-------------------------------
l = []
a1=len(l)
class LoginForm(Form):
  username=StringField('User Name',[validators.Length(min=1,max=20)])
  password= PasswordField('Password',[validators.Length(min=1,max =10 )])
@app.route('/')
def scrape12():
    base_url = 'https://economictimes.indiatimes.com/news/economy/agriculture/articlelist/msid-1202099874,contenttype-a.cms'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")
    all_product = soup.find_all('div', class_="eachStory")
    for item in all_product:
        d = { }

        # image
        product_image = item.find("img", {"class":"lazy"})
        if(product_image==None):
          d['product_image'] = product_image
        else:
        # image = image.text.replace('\n', "").strip()
          product_image1 = product_image['src']
          product_image = product_image['data-original']
          d['product_image'] = product_image
        product_name = item.find("a")

        product_name12=item.find("h3").text
        product_desc=item.find("p").text
        product_time=item.find("time").text
        product_link = 'https://economictimes.indiatimes.com' + product_name['href']

        d['product_link'] = product_link
        d["product_name12"]=product_name12
        d["product_desc"]=product_desc
        d["product_time"]=product_time
        l.append(d)

    a1=len(l)

    # print(l[0]['product_image'])
#--------------market_price in home page-----------------------------
    now = datetime.date.today()
    now1=date.today() - timedelta(1)
    a='mark_prices%s'%now
    f='mark_prices%s'%now1
    punctuations = '''#-'"\,'''
    my_str = a
    no_punct = ""
    for char in my_str:
       if char not in punctuations:
           no_punct = no_punct + char
    my_str1 = f
    no_punct1 = ""
    for char in my_str1:
       if char not in punctuations:
           no_punct1 = no_punct1 + char
    e=no_punct1
    d=no_punct
    c=' TABLE ' + d
    z=0
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES")
    rv1=cur.fetchall()
    print(len(rv1))
    for i in range(0,len(rv1)):
        rv2=rv1[i]['Tables_in_agmark']
        if(str(rv2)==str(d)):
          z=1
    if(z==1):  
      cur.execute('''SELECT * FROM %s'''%d)
      dt=now
      rv=cur.fetchall()
    else:
      cur.execute('''SELECT * FROM `updatetables`''')
      rv=cur.fetchall()
      dt=now1
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Paddy'AND `VARIET.Y`='Paddy'"%d)
      paddy=cur.fetchall()
      paddy=list(paddy)
      mark["paddy_com"]=paddy[0]['COMMODITY']
      mark["paddy_min"]=paddy[0]['MIN_PRICE']
      mark["paddy_max"]=paddy[0]['MAX_PRICE']
      mark["paddy_model"]=paddy[0]['MODAL_PRICE']
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Paddy'AND `VARIETY`='Paddy'")
      paddy=cur.fetchall()
      paddy=list(paddy)
      mark["paddy_com"]=paddy[0]['COMMODITY']
      mark["paddy_min"]=paddy[0]['MIN_PRICE']
      mark["paddy_max"]=paddy[0]['MAX_PRICE']
      mark["paddy_model"]=paddy[0]['MODAL_PRICE']
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Groundnut'AND `VARIETY`='Local'"%d)
      groundnut=cur.fetchall()
      groundnut=list(groundnut)
      mark["groundnut_com"]=groundnut[0]['COMMODITY']
      mark["groundnut_min"]=groundnut[0]['MIN_PRICE']
      mark["groundnut_max"]=groundnut[0]['MAX_PRICE']
      mark["groundnut_model"]=groundnut[0]['MODAL_PRICE']
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Groundnut'AND `VARIETY`='Local'")
      groundnut=cur.fetchall()
      groundnut=list(groundnut)
      mark["groundnut_com"]=groundnut[0]['COMMODITY']
      mark["groundnut_min"]=groundnut[0]['MIN_PRICE']
      mark["groundnut_max"]=groundnut[0]['MAX_PRICE']
      mark["groundnut_model"]=groundnut[0]['MODAL_PRICE']
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Dry Chillies'AND `VARIETY`='1st Sort'"%d)
      Chillies=cur.fetchall()
      Chillies=list(Chillies)
      mark["Chillies_com"]=Chillies[0]['COMMODITY']
      mark["Chillies_min"]=Chillies[0]['MIN_PRICE']
      mark["Chillies_max"]=Chillies[0]['MAX_PRICE']
      mark["Chillies_model"]=Chillies[0]['MODAL_PRICE']
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Dry Chillies'AND `VARIETY`='1st Sort'")
      Chillies=cur.fetchall()
      Chillies=list(Chillies)
      mark["Chillies_com"]=Chillies[0]['COMMODITY']
      mark["Chillies_min"]=Chillies[0]['MIN_PRICE']
      mark["Chillies_max"]=Chillies[0]['MAX_PRICE']
      mark["Chillies_model"]=Chillies[0]['MODAL_PRICE']
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Tamarind Fruit'AND `VARIETY`='Flower Ac'"%d)
      tamarindfruit=cur.fetchall()
      tamarindfruit=list(tamarindfruit)
      mark["tamarindfruit_com"]=tamarindfruit[0]['COMMODITY']
      mark["tamarindfruit_min"]=tamarindfruit[0]['MIN_PRICE']
      mark["tamarindfruit_max"]=tamarindfruit[0]['MAX_PRICE']
      mark["tamarindfruit_model"]=tamarindfruit[0]['MODAL_PRICE']
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Tamarind Fruit'AND `VARIETY`='Flower Ac'")
      tamarindfruit=cur.fetchall()
      tamarindfruit=list(tamarindfruit)
      mark["tamarindfruit_com"]=tamarindfruit[0]['COMMODITY']
      mark["tamarindfruit_min"]=tamarindfruit[0]['MIN_PRICE']
      mark["tamarindfruit_max"]=tamarindfruit[0]['MAX_PRICE']
      mark["tamarindfruit_model"]=tamarindfruit[0]['MODAL_PRICE']
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Cotton'AND `VARIETY`='MCU 5'"%d)
      cotton=cur.fetchall()
      cotton=list(cotton)
      mark["cotton_com"]=cotton[0]['COMMODITY']
      mark["cotton_min"]=cotton[0]['MIN_PRICE']
      mark["cotton_max"]=cotton[0]['MAX_PRICE']
      mark["cotton_model"]=cotton[0]['MODAL_PRICE']
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Cotton'AND `VARIETY`='MCU 5'")
      cotton=cur.fetchall()
      cotton=list(cotton)
      mark["cotton_com"]=cotton[0]['COMMODITY']
      mark["cotton_min"]=cotton[0]['MIN_PRICE']
      mark["cotton_max"]=cotton[0]['MAX_PRICE']
      mark["cotton_model"]=cotton[0]['MODAL_PRICE']

#==============vegitables=============
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Tomato'AND `VARIETY`='Local'"%d)
      tomato=cur.fetchall()
      tomato=list(tomato)
      mark["tomato_com"]=tomato[0]['COMMODITY']
      mark["tomato_min"]=tomato[0]['MIN_PRICE']
      mark["tomato_max"]=tomato[0]['MAX_PRICE']
      mark["tomato_model"]=tomato[0]['MODAL_PRICE']
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Tomato'AND `VARIETY`='Local'")
      tomato=cur.fetchall()
      tomato=list(tomato)
      mark["tomato_com"]=tomato[0]['COMMODITY']
      mark["tomato_min"]=tomato[0]['MIN_PRICE']
      mark["tomato_max"]=tomato[0]['MAX_PRICE']
      mark["tomato_model"]=tomato[0]['MODAL_PRICE']
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Banana - Green'AND `VARIETY`='Banana - Green'"%d)
      banana=cur.fetchall()
      banana=list(banana)
      mark["banana_com"]=banana[0]['COMMODITY']
      mark["banana_min"]=banana[0]['MIN_PRICE']
      mark["banana_max"]=banana[0]['MAX_PRICE']
      mark["banana_model"]=banana[0]['MODAL_PRICE']
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Banana - Green'AND `VARIETY`='Banana - Green'")
      banana=cur.fetchall()
      banana=list(banana)
      mark["banana_com"]=banana[0]['COMMODITY']
      mark["banana_min"]=banana[0]['MIN_PRICE']
      mark["banana_max"]=banana[0]['MAX_PRICE']
      mark["banana_model"]=banana[0]['MODAL_PRICE']
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Coconut'AND `VARIETY`='Coconut'"%d)
      Coconut=cur.fetchall()
      Coconut=list(Coconut)
      mark["Coconut_com"]=Coconut[0]['COMMODITY']
      mark["Coconut_min"]=Coconut[0]['MIN_PRICE']
      mark["Coconut_max"]=Coconut[0]['MAX_PRICE']
      mark["Coconut_model"]=Coconut[0]['MODAL_PRICE']
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Coconut'AND `VARIETY`='Coconut'")
      Coconut=cur.fetchall()
      Coconut=list(Coconut)
      mark["Coconut_com"]=Coconut[0]['COMMODITY']
      mark["Coconut_min"]=Coconut[0]['MIN_PRICE']
      mark["Coconut_max"]=Coconut[0]['MAX_PRICE']
      mark["Coconut_model"]=Coconut[0]['MODAL_PRICE']
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Onion'AND `VARIETY`='Local'"%d)
      Onion=cur.fetchall()
      Onion=list(Onion)
      mark["Onion_com"]=Onion[0]['COMMODITY']
      mark["Onion_min"]=Onion[0]['MIN_PRICE']
      mark["Onion_max"]=Onion[0]['MAX_PRICE']
      mark["Onion_model"]=Onion[0]['MODAL_PRICE']
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Onion'AND `VARIETY`='Local'")
      Onion=cur.fetchall()
      Onion=list(Onion)
      mark["Onion_com"]=Onion[0]['COMMODITY']
      mark["Onion_min"]=Onion[0]['MIN_PRICE']
      mark["Onion_max"]=Onion[0]['MAX_PRICE']
      mark["Onion_model"]=Onion[0]['MODAL_PRICE']
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Papaya'AND `VARIETY`='Papaya'"%d)
      Papaya=cur.fetchall()
      Papaya=list(Papaya)
      mark["Papaya_com"]=Papaya[0]['COMMODITY']
      mark["Papaya_min"]=Papaya[0]['MIN_PRICE']
      mark["Papaya_max"]=Papaya[0]['MAX_PRICE']
      mark["Papaya_model"]=Papaya[0]['MODAL_PRICE']
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Papaya'AND `VARIETY`='Papaya'")
      Papaya=cur.fetchall()
      Papaya=list(Papaya)
      mark["Papaya_com"]=Papaya[0]['COMMODITY']
      mark["Papaya_min"]=Papaya[0]['MIN_PRICE']
      mark["Papaya_max"]=Papaya[0]['MAX_PRICE']
      mark["Papaya_model"]=Papaya[0]['MODAL_PRICE']

    form=LoginForm(request.form)
    if request.method == 'POST' and form.validate():
      username=form.username.data
      password=form.password.data
      
      print (username, password)
      return render_template('home1.html')
#================milk
#====endmilk========
 
        #commit to DB

    mysql.connection.commit()

       #close connection
    cur.close()

    return render_template('index1.html',l=l,rv=rv,dt=dt,mark=mark,form=form)           
    
    # return render_template('index.html')

@app.route('/weather')


def weather():
  api_address='http://api.openweathermap.org/data/2.5/weather?appid=d1e883aefcf29c8de1e89a03ef58bb5c&q='
  city= "hyderabad"
  url=  api_address + city

  json_data = requests.get(url).json()
  print(json_data)
  formatted_data1=json_data['main']['temp_min']
  formatted_data = int(formatted_data1-273)
  
  return render_template('reg.html',formatted_data=formatted_data,json_data=json_data,city=city)


# #--------------------------------------farmer reg---------------


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegisterForm(Form):
  first_name=StringField('first_name',[validators.Length(min=1,max=10)])
  last_name1= StringField('last_name',[validators.Length(min=1,max =10 )])
  dt = DateField('Date', format='%Y-%m-%d')
  email=StringField('Email',[validators.Length(min=2,max=50)])
  mobile=StringField('Phone',[validators.Length(min=10,max=13)])
  aadher_number=StringField('Aadher number',[validators.Length(min=1,max=16)])
  string_of_files = ['Paddy\r\nWheat\r\nCotton\r\nMirchi\r\nVegetables']
  list_of_files = string_of_files[0].split()
  files = [(x, x) for x in list_of_files]
  example = MultiCheckboxField('Label', choices=files)

  string_of_files1 = ['Cattle\r\nFish\r\nPoultry\r\nGoat\r\nSheep']
  list_of_files1 = string_of_files1[0].split()
  files1 = [(x, x) for x in list_of_files1]
  example1 = MultiCheckboxField('Label', choices=files1)

  string_of_files2 = ['Milk\r\nGhee\r\nButter\r\nCheese\r\nMilk Powder']
  list_of_files2 = string_of_files2[0].split()
  files2 = [(x, x) for x in list_of_files2]
  example2 = MultiCheckboxField('Label', choices=files)

  address = TextAreaField(u'Address', [validators.optional(), validators.length(max=200)])
  stata = SelectField(u'Choose your State', choices=[('None','None'),('Andhra Pradesh','Andhra Pradesh'),('Telangana','Telangana')])
  districtand = SelectField(u'District', choices=[('None','None'),('Anantapur','Anantapur'),('Chittoor','Chittoor'),('East Godavari','East Godavari'),('Guntur','Guntur'),('Krishna','Krishna'),('Kurnool','Kurnool'),('Nellore','Nellore'),('Prakasam','Prakasam'),('Srikakulam','Srikakulam'),('Visakhapatnam','Visakhapatnam'),('Vizianagaram','Vizianagaram'),('West Godavari','West Godavari'),('YSR Kadapa','YSR Kadapa')])
  Village=StringField('Village',[validators.Length(min=1,max=16)])
  Taluka=StringField('Taluka',[validators.Length(min=1,max=16)])
  Pincode=StringField('Pincode',[validators.Length(min=4,max=10)])



@app.route('/register', methods = ['GET', 'POST'])

def register():
   form = RegisterForm(request.form)
   print("hiii")
   if request.method == 'POST' and form.validate():
       print("h3")
       target = os.path.join(APP_ROOT, 'images/')
       print (target)

       if not os.path.isdir(target):
        os.mkdir(target)
       for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print (destination)
        file.save(destination)
       fname = form.first_name.data
       lname1 = form.last_name1.data
       dt = form.dt.data
       email = form.email.data
       mobile = form.mobile.data
       aadher_number = form.aadher_number.data
       address = form.address.data
       stata = form.stata.data
       districtand = form.districtand.data
       Village = form.Village.data
       Taluka = form.Taluka.data
       Pincode= form.Pincode.data
       print(fname,lname1,dt,email,mobile,aadher_number,address,stata,districtand,Village,Taluka,Pincode)
       print ("you checked",form.example.data)
       print ("you checked",form.example1.data)
       print ("you checked",form.example2.data)
       
       return redirect(url_for('home'))

   return render_template('register.html',form = form)


#------------currentpage--------------------
@app.route('/currentstatus')


def currentstatus():
  cur=mysql.connection.cursor()
  cur.execute('''SELECT * FROM registers''')
  rv=cur.fetchall()
  return render_template('currentstatus.html',rv=rv)

if __name__=='__main__':
  app.secret_key = os.urandom(12)
  app.run(host='localhost', port=8181, debug=True)

