from flask import Flask,render_template,flash,redirect,request,url_for,session,logging
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,SelectField,BooleanField,SelectMultipleField,widgets
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired,Length,Email
from passlib.hash import sha256_crypt
from db import *
from flask import Flask
from flask_mail import Mail, Message#pip install flask_mail
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user#pip install flask_login
import os
from functools import wraps
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import requests#scrapy
from flask import jsonify#neewsfeeds
from scrapingneews import scrape12#neewsfeeds

 



# from flask_wtf.csrf import CSRFProtect#pip install flask_csrf
db = Db()
courseList = []
for i in db.execute("SELECT * FROM course_names"):
    courseList.append(i)
db.commit()
db.close()

app=Flask(__name__)
app.config.from_object(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskappdb'
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
    return render_template('about.html')
@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')
@app.route('/faq')
def faq():
    return render_template('faq.html')
@app.route('/how_to_reg')
def how_to_reg():
    return render_template('how_to_reg.html')
#-----services
@app.route('/services_agri')
def services_agri():
    return render_template('services_agri.html')

@app.route('/services_dairy')
def services_dairy():
    return render_template('services_dairy.html')
@app.route('/services_animal_hury')
def services_animal_hury():
    return render_template('services_animal_hury.html')
#-----benefits
@app.route('/benefits_farmer')
def benefits_farmer():
    return render_template('benefits_farmer.html')
@app.route('/benefits_process')
def benefits_process():
    return render_template('benefits_process.html')
@app.route('/benefits_storage')
def benefits_storage():
    return render_template('benefits_storage.html')
@app.route('/benefits_supplier')
def benefits_supplier():
    return render_template('benefits_supplier.html')
@app.route('/benefits_trader')
def benefits_trader():
    return render_template('benefits_trader.html')
@app.route('/benefits_logistics')
def services_logistics():
    return render_template('benefits_logistics.html')


#-------------------------end static routes----------------------
#-----------------------------------------login----------------
@app.route('/login',methods = ['GET','POST'])
def login():
   if request.method == 'POST':
       #get form fields

       username = request.form['username']
       password_candidate = request.form['password']

       # Create cursor
       cur = mysql.connection.cursor()

       # get user by username

       result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
       print('name:',username)
       if result > 0:

           data = cur.fetchone()
           password = data['password']

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
               return redirect(url_for('home'))
           else:
               error = 'Invalid Login'
               #app.logger.info('Passwords Not matched')
               return render_template('login.html',error=error)
           # close connection
           cur.close()
       else:
           #app.logger.info('No user')
           error:'Username not found'
           return render_template('login.html',error=error)

   return render_template('login.html')
def is_logged_in(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       if 'logged_in' in session:
           return f(*args, **kwargs)
       else:
           flash('Unauthorized, Please Login','danger')
           return redirect(url_for('login'))
   return wrap

   return render_template('login.html')
# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

#---------------------------------------------------------

# ------------------------market-prices-----------------------------------
import datetime
from datetime import date, timedelta

@app.route('/market')


def market():
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

    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES")
    rv1=cur.fetchall()
    for i in range(0,len(rv1)):
      rv2=rv1[i]['Tables_in_flaskappdb']
      if(str(rv2)==str(d)):
        print(rv2,'==',d)
        z=1
    if(z==1):
      print("exit")   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Paddy'AND `VARIETY`='Paddy'"%d)
      paddy=cur.fetchall()
    else:
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Paddy'AND `VARIETY`='Paddy'"%e)
      paddy=cur.fetchall()
    print(paddy)


    cur.execute("DROP TABLE IF EXISTS %s"%d)    
    cur.execute( "CREATE %s SELECT * FROM %s"%(c,e))
    dt=now
    cur.execute('''SELECT * FROM %s'''%d)
    # try:
    #   cur.execute('''SELECT * FROM %s'''%d)
    #   dt=now
    #   print(1)
    #   rv=cur.fetchall()
    # except:
    #   cur.execute('''SELECT * FROM %s'''%e)
    #   dt=now1
    #   print(2)
    rv=cur.fetchall()

    cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Paddy'AND `VARIETY`='Paddy'"%d)
    paddy=cur.fetchall()
       #commit to DB

    mysql.connection.commit()

       #close connection
    cur.close()

    return render_template('admin.html',rv=rv,dt=dt,paddy=paddy)
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
      rv2=rv1[i]['Tables_in_flaskappdb']
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
     #    cur.execute('''SELECT * FROM %s'''%d)
     #    dt=now

     #    rv1=cur.fetchall()

     #    cur.execute('''SELECT * FROM %s'''%e)
  
     #    rv2=cur.fetchall()

     # #commit to DB

     #    mysql.connection.commit()

     # #close connection
     #    cur.close()

        # return render_template('admin.html',dt=dt,rv1=rv1,rv2=rv2)
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

    return render_template('adminupdate.html',dt=dt,rv=rv)


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
  print("detalies")
  print(DISTRICT,MARKET,COMMODITY,VARIETY,UNITS,MIN_PRICE,MAX_PRICE,MODAL_PRICE,UNITY_OF_PRICE,ID)



  
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
  # cur.execute("UPDATE `%s` SET `ID`=`%s`,`DISTRICT`=`%s`,`MARKET`=`%s`,`COMMODITY`=`%s`,`VARIETY`=`%s`,`UNITS`=`%s`,`MIN_PRICE`=`%s`,`MAX_PRICE`=`%s`,`MODAL_PRICE`=`%s`,`UNITY_OF_PRICE`=`%s` WHERE `ID`=%s"%(d,ID,DISTRICT,MARKET,COMMODITY,VARIETY,UNITS,MIN_PRICE,MAX_PRICE,MODAL_PRICE,UNITY_OF_PRICE,c))
# UPDATE `mark_prices20180106` SET `ID`=ID,`DISTRICT`=DISTRICT,`MARKET`=MARKET,`COMMODITY`=COMMODITY,`VARIETY`=VARIETY,`UNITS`=UNITS,`MIN_PRICE`=MIN_PRICE,`MAX_PRICE`=MAX_PRICE,`MODAL_PRICE`=MODAL_PRICE,`UNITY_OF_PRICE`=UNITY_OF_PRICE WHERE `ID`=ID
# UPDATE `mark_prices20180106` SET `ID`=`%s`,`DISTRICT`=`%s`,`MARKET`=`%s`,`COMMODITY`=`%s`,`VARIETY`=`%s`,`UNITS`=`%s`,`MIN_PRICE`=`%s`,`MAX_PRICE`=`%s`,`MODAL_PRICE`=`%s`,`UNITY_OF_PRICE`=`%s` WHERE `ID`=`%s`
  
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
  dairyform = SelectMultipleField(u'', choices=[('Milk','Milk'), ('Ghee', 'Ghee'), ('Butter', 'Butter'), ('Cheese', 'Cheese'), ('Milk Powder', 'Milk Powder')], option_widget=widgets.CheckboxInput(),
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
    farmerEmail=form.email.data
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
    print (farmerFirstname, farmerLastname, farmerDateofBirth, farmerEmail, farmerContactNumber, farmeraadharNumber, farmerAddress, farmerCroptype, farmerAnimalHusbandryType, farmerDairyform, farmerState, farmerDistrict, farmerVillage, farmerTaluka, farmerPincode)
    return render_template('home1.html')
  return render_template('far_reg1.html', form=form)


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
    print (LTRfullname, LTRcontactnumber, LTRemail, LTRcompanyName, LTRvehicleType)
    return render_template('home1.html')
  return render_template('logistics_reg.html', form=form)

#==========================end registations=======================================

# #--------------------------foodprocesser register-----------------------

# class RegisterForm1(Form):
#   name=StringField('Name',[validators.Length(min=1,max=50)])
#   mobile = StringField('mobile',[validators.Length(min=10,max =13 )])
#   email=StringField('Email',[validators.Length(min=2,max=50)])
#   # course = SelectField(u'Course', choices=courseList)
  


# @app.route('/register12', methods = ['GET', 'POST'])


# def register12():
#    form = RegisterForm1(request.form)
#    print("h2")
#    if request.method == 'POST' and form.validate():
#        print("h3")
#        name = form.name.data
#        mobile = form.mobile.data
#        email = form.email.data  
#        course = form.course.data

#        status = 'register12'
#        cur = mysql.connection.cursor()

#        cur.execute("INSERT INTO register1s(name,email,mobile,course) VALUES(%s, %s, %s, %s)",(name,email,mobile,course))
#        cur.execute("INSERT INTO logins(username,password,status) VALUES(%s, %s, %s)",(name,email,status))
#        #commit to DB

#        mysql.connection.commit()

#        #close connection
#        cur.close()
       
#        return render_template('home.html')

#    return render_template('register1.html',form = form)


# #---------------------------wearhouse------------------
# class RegisterForm2(Form):
#   name=StringField('Name',[validators.Length(min=1,max=50)])
#   mobile = StringField('mobile',[validators.Length(min=10,max =13 )])
#   email=StringField('Email',[validators.Length(min=2,max=50)])
  

# @app.route('/register2', methods = ['GET', 'POST'])

# def register2():
#    form = RegisterForm2(request.form)
#    if request.method == 'POST' and form.validate(): 
#        name = form.name.data
#        mobile = form.mobile.data
#        email = form.email.data  
#        status = 'register2'
#        cur = mysql.connection.cursor()

#        cur.execute("INSERT INTO register2s(name,email,mobile) VALUES(%s, %s, %s)",(name,email,mobile))
#        cur.execute("INSERT INTO logins(username,password,status) VALUES(%s, %s, %s)",(name,email,status))
#        #commit to DB

#        mysql.connection.commit()

#        #close connection
#        cur.close()
       
#        return redirect(url_for('home'))

#    return render_template('register2.html',form = form)




# -----------------------------Login/logout-------------------------------- 


@app.route('/index')


def home():
    return render_template('home1.html')



#--------------------------neewsfeed-------------------------------
@app.route('/')
def scrape12():
    l = []
    base_url = 'https://economictimes.indiatimes.com/news/economy/agriculture/articlelist/msid-1202099874,contenttype-a.cms'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")
    all_product = soup.find_all('div', class_="eachStory")
    for item in all_product:
        d = { }
        
        # image
        product_image = item.find("img", {"class":"lazy"})
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
    print(l[0]['product_image'])
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
        rv2=rv1[i]['Tables_in_flaskappdb']
        if(str(rv2)==str(d)):
          z=1
    if(z==1):  
      cur.execute('''SELECT * FROM %s'''%d)
      dt=now
      rv=cur.fetchall()
    else:
      cur.execute('''SELECT * FROM %s'''%e)
      rv=cur.fetchall()
      dt=now1
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Paddy'AND `VARIETY`='Paddy'"%d)
      paddy=cur.fetchall()
      paddy=list(paddy)
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Paddy'AND `VARIETY`='Paddy'")
      paddy=cur.fetchall()
      paddy=list(paddy)
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Groundnut'AND `VARIETY`='Local'"%d)
      groundnut=cur.fetchall()
      groundnut=list(groundnut)
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Groundnut'AND `VARIETY`='Local'")
      groundnut=cur.fetchall()
      groundnut=list(groundnut)
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Dry Chillies'AND `VARIETY`='1st Sort'"%d)
      Chillies=cur.fetchall()
      Chillies=list(Chillies)
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Dry Chillies'AND `VARIETY`='1st Sort'")
      Chillies=cur.fetchall()
      Chillies=list(Chillies)
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Tamarind Fruit'AND `VARIETY`='Flower Ac'"%d)
      tamarindfruit=cur.fetchall()
      tamarindfruit=list(tamarindfruit)
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Tamarind Fruit'AND `VARIETY`='Flower Ac'")
      tamarindfruit=cur.fetchall()
      tamarindfruit=list(tamarindfruit)
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Cotton'AND `VARIETY`='MCU 5'"%d)
      cotton=cur.fetchall()
      cotton=list(cotton)
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Cotton'AND `VARIETY`='MCU 5'")
      cotton=cur.fetchall()
      cotton=list(cotton)

#==============vegitables=============
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Tomato'AND `VARIETY`='Local'"%d)
      tomato=cur.fetchall()
      tomato=list(tomato)
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Tomato'AND `VARIETY`='Local'")
      tomato=cur.fetchall()
      tomato=list(tomato)
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Banana - Green'AND `VARIETY`='Banana - Green'"%d)
      banana=cur.fetchall()
      banana=list(banana)
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Banana - Green'AND `VARIETY`='Banana - Green'")
      banana=cur.fetchall()
      banana=list(banana)
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Coconut'AND `VARIETY`='Coconut'"%d)
      Coconut=cur.fetchall()
      Coconut=list(Coconut)
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Coconut'AND `VARIETY`='Coconut'")
      Coconut=cur.fetchall()
      Coconut=list(Coconut)
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Onion'AND `VARIETY`='Local'"%d)
      Onion=cur.fetchall()
      Onion=list(Onion)
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Onion'AND `VARIETY`='Local'")
      Onion=cur.fetchall()
      Onion=list(Onion)
    if(z==1):   
      cur.execute("SELECT * FROM `%s` WHERE `COMMODITY`='Papaya'AND `VARIETY`='Papaya'"%d)
      Papaya=cur.fetchall()
      Papaya=list(Papaya)
    else:
      cur.execute("SELECT * FROM `updatetables` WHERE `COMMODITY`='Papaya'AND `VARIETY`='Papaya'")
      Papaya=cur.fetchall()
      Papaya=list(Papaya)
#================milk
#====endmilk========
 
        #commit to DB

    mysql.connection.commit()

       #close connection
    cur.close()

    return render_template('index1.html',l=l,a1=a1,rv=rv,dt=dt,paddy=paddy,groundnut=groundnut,Chillies=Chillies,cotton=cotton,tamarindfruit=tamarindfruit,Papaya=Papaya,Onion=Onion,tomato=tomato,banana=banana,Coconut=Coconut)           
    
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


# #--------------------------foodprocesser register-----------------------

# class RegisterForm1(Form):
#   name=StringField('Name',[validators.Length(min=1,max=50)])
#   mobile = StringField('mobile',[validators.Length(min=10,max =13 )])
#   email=StringField('Email',[validators.Length(min=2,max=50)])
#   course = SelectField(u'Course', choices=courseList)
  


# @app.route('/register12', methods = ['GET', 'POST'])


# def register12():
#    form = RegisterForm1(request.form)
#    print("h2")
#    if request.method == 'POST' and form.validate():
#        print("h3")
#        name = form.name.data
#        mobile = form.mobile.data
#        email = form.email.data  
#        course = form.course.data

#        status = 'register12'
#        cur = mysql.connection.cursor()

#        cur.execute("INSERT INTO register1s(name,email,mobile,course) VALUES(%s, %s, %s, %s)",(name,email,mobile,course))
#        cur.execute("INSERT INTO logins(username,password,status) VALUES(%s, %s, %s)",(name,email,status))
#        #commit to DB

#        mysql.connection.commit()

#        #close connection
#        cur.close()
       
#        return render_template('home.html')

#    return render_template('register1.html',form = form)


# #---------------------------wearhouse------------------
# class RegisterForm2(Form):
#   name=StringField('Name',[validators.Length(min=1,max=50)])
#   mobile = StringField('mobile',[validators.Length(min=10,max =13 )])
#   email=StringField('Email',[validators.Length(min=2,max=50)])
  

# @app.route('/register2', methods = ['GET', 'POST'])

# def register2():
#    form = RegisterForm2(request.form)
#    if request.method == 'POST' and form.validate(): 
#        name = form.name.data
#        mobile = form.mobile.data
#        email = form.email.data  
#        status = 'register2'
#        cur = mysql.connection.cursor()

#        # cur.execute("INSERT INTO register2s(name,email,mobile) VALUES(%s, %s, %s)",(name,email,mobile))
#        # cur.execute("INSERT INTO logins(username,password,status) VALUES(%s, %s, %s)",(name,email,status))
#        cur.execute("INSERT INTO logins(username,status) VALUES(%s,%s)",(name,status))
#        #commit to DB

#        mysql.connection.commit()

#        #close connection
#        cur.close()
       
#        return redirect(url_for('home'))

#    return render_template('register2.html',form = form)


#------------currentpage--------------------
@app.route('/currentstatus')


def currentstatus():
  cur=mysql.connection.cursor()
  cur.execute('''SELECT * FROM registers''')
  rv=cur.fetchall()
  return render_template('currentstatus.html',rv=rv)


#-------login 6 tables------------------------------------------


#---------------------------------------------------------



if __name__=='__main__':
  app.secret_key = os.urandom(12)
  app.run(host='localhost', port=8181, debug=True)

