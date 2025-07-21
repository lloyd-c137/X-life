from flask import Blueprint, render_template, request, redirect,session
from .form import RegisterForm,LoginForm
from utils import db
from werkzeug.security import generate_password_hash,check_password_hash
from models import UserModel
from LoginAuth import login_required
auth = Blueprint("auth",__name__,url_prefix="/auth")


@auth.route("/register",methods=["POST","GET"])
# @login_required
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = UserModel(username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect("/auth/login")
        else:
            print(form.errors)
            return redirect("/auth/register")




@auth.route("/login",methods=["POST","GET"])
# @login_required
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = UserModel.query.filter_by(username=username).first()
            if not user:
                print(form.errors)
                return redirect("/auth/login")
            else:
                if check_password_hash(user.password,password):
                    session['username'] = username
                    session['id'] = user.id
                    return redirect("/")
                else:
                    print(form.errors)
                    return redirect("/auth/login")
        else:
            print(form.errors)
            return redirect("/auth/login")







