from flask import Blueprint, jsonify, render_template, url_for, redirect, flash,request
from api.forms import registrationForm, loginForm, postForm, editForm
# from flask_caching import Cache
from flask_login import login_user, current_user, logout_user
from api import app,db
from api.utils import save_picture
import datetime
from api.model import User,Post,Picture
import hashlib
import jwt

bp = Blueprint('',__name__,template_folder='templates')

def auth(func):
        def wrapper():
                content=request.get_json()
                token= content["token"]
                try:
                        data=jwt.decode(token, app.config['SECRET_KEY'])
                except Exception as e:
                        return ("not valid")
                return func()
        return wrapper

@bp.route("/",methods=['GET','POST'])
@bp.route("/index/",methods=['GET','POST'])
# @auth
def index():
        if current_user.is_authenticated:
                form=postForm()
                if form.validate_on_submit():
                        post=Post(story=form.story.data,user_id=current_user.id)
                        db.session.add(post)
                        db.session.commit()
                        if  str(form.picture.data[0].filename) != '':
                                for i in form.picture.data:
                                        picture=save_picture(i)
                                        pic=Picture(link=picture,post_id=post.id,user_id=current_user.id)
                                        db.session.add(pic)
                                        db.session.commit()
                        return redirect(url_for(".index"))
                posts = Post.query.all()
                return render_template("index.html",user=current_user.username,title='home',form=form,posts=posts)
        else:
                return redirect(url_for('.login'))

@bp.route("/registration",methods=['GET','POST'])
def registration():
        if current_user.is_authenticated:
                return redirect(url_for('.index'))
        form=registrationForm()
        if form.validate_on_submit():
                paswd=hashlib.sha224(form.password.data.encode())
                paswd=str(paswd.hexdigest())
                user=User(username=form.username.data,email=form.email.data,password=paswd)
                db.session.add(user)
                db.session.commit()
                flash('Your account has been created! You are now able to log in', 'success')
                return redirect(url_for(".login"))
        return render_template('registration.html',title='registration',form=form)

@bp.route("/login",methods=['GET','POST'])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('.index'))
        form = loginForm()
        if form.validate_on_submit():
                user = User.query.filter_by(username=form.username.data).first()
                try:
                        if user and user.password==str(hashlib.sha224(form.password.data.encode()).hexdigest()):
                                login_user(user, remember=form.remember.data)
                                return  redirect(url_for('.index'))
                        else:
                                return redirect(url_for('.login'))
                except:
                        return redirect(url_for('.login'))
        return render_template('login.html',title='login',form=form)

@bp.route("/logout")
def logout():
        logout_user()
        return redirect(url_for('.login'))

@bp.route("/profile")
def profile():
        if current_user.is_authenticated:
                posts = Post.query.filter_by(user_id=current_user.id)
                pictures = Picture.query.filter_by(user_id=current_user.id)
                return render_template("profile.html",title="profile",user=current_user.username,posts=posts,pictures=pictures)
        else:
                return redirect(url_for(".login"))

@bp.route("/delete/<id>")
def delete(id):
        if current_user.is_authenticated:
                post=Post.query.filter_by(id=id).first()
                db.session.delete(post)
                db.session.commit()
                return redirect(url_for('.profile'))

@bp.route("/edit/<id>",methods=['GET','POST'])
def edit(id):
        if current_user.is_authenticated:
                post=Post.query.filter_by(id=id).first()
                form=editForm()
                if form.validate_on_submit():   
                        post.story=form.story.data
                        db.session.add(post)
                        db.session.commit()
                        return redirect(url_for(".profile"))
                return render_template("edit.html",title='edit',form=form,post=post)

@bp.route("/GetToken",methods=['GET','POST'])
def GetToken():
        if request.method =='POST':
                content = request.get_json()
                username = content["username"]
                password = content["password"]
                user = User.query.filter_by(username=username).first()
                if user.username==username and user.password==str(hashlib.sha224(password.encode()).hexdigest()):
                        token=jwt.encode({'user':username,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=5)},app.config['SECRET_KEY'])
                        return jsonify({'token':token.decode('UTF-8')})
                else :
                        return ("???")

