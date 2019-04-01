import secrets
import os
from PIL import Image
from flask import render_template,url_for,flash,redirect, request
from deepbrain import app,db,bcrypt
from deepbrain.models import User,Post
from deepbrain.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required

posts = [
	{
		'author' : 'Ousseynou Dieng',
		'title' : 'Lorem',
		'content' : 'Lorem ipsum sit amel color',
		'date_posted' : 'January 28, 2018'
	},
	{
		'author' : 'Djily Dieye',
		'title' : 'Pixum',
		'content' : 'Siera que oulo, des estas',
		'date_posted' : 'January 27, 2019'
	},
	{
		'author' : 'Ousseynou Dieng',
		'title' : 'Lorem',
		'content' : 'Lorem ipsum sit amel color',
		'date_posted' : 'January 28, 2018'
	},
	{
		'author' : 'Ousseynou Dieng',
		'title' : 'Lorem',
		'content' : 'Lorem ipsum sit amel color',
		'date_posted' : 'January 28, 2018'
	},
	{
		'author' : 'Ousseynou Dieng',
		'title' : 'Lorem',
		'content' : 'Lorem ipsum sit amel color',
		'date_posted' : 'January 28, 2018'
	}
]


@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html", posts=posts)


@app.route("/about")
def about():
	return render_template('about.html',title="AI-About")

@app.route("/login",methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('index'))
		else:
			flash("Login Unsuccessful - Please check username or password ","warning")
	return render_template("login.html",title="login",form=form)


@app.route("/register",methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data,email=form.email.data,password=hashed_pwd)
		db.session.add(user)
		db.session.commit()
		flash("Your account has been created with success, You can now login! ",'warning')
		return redirect(url_for('login'))
	return render_template("register.html",title="register",form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index')) 


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
	#resize the image
	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	
	return picture_fn

@app.route("/account", methods=["GET","POST"])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Your account has been updated!","primary")
		return redirect(url_for('account'))
	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
	return render_template('account.html',title="account",image_file=image_file,form=form) 