import random
from flask import Blueprint, render_template,request,redirect,jsonify,g
from LoginAuth import login_required
from models import TaskModel,UserModel
from utils import db
view = Blueprint("view",__name__)


@view.route("/failed")
@login_required
def failed():
    if g.user.money < 0:
        return render_template("failed.html")
    else:
        return redirect("/")
@view.route("/",methods=["POST","GET"])
@login_required
def index():
    return render_template("test.html")

@view.route("/gettask")
@login_required
def get_task():
    last_task = db.session.query(TaskModel).order_by(TaskModel.id.desc()).first()
    # 随机生成任务id
    task_id = random.randint(1,last_task.id)
    # 根据生成的任务id去数据库中取对象
    task_obj = TaskModel.query.filter_by(id=task_id).first()
    # 得到task对象的名字
    task_name = task_obj.task
    return jsonify({"id":task_id,"task_name":task_name})

@view.route("/task_upgrade",methods=["POST"])
@login_required
def upgrade():
    data = request.get_json()
    task_id = data.get('task_id')
    user_id = data.get('user_id')
    success = data.get('status')
    task_obj = TaskModel.query.filter_by(id=task_id).first()
    reward = task_obj.value
    user = UserModel.query.filter_by(id=user_id).first()
    if success:
        user.money += reward
    else:
        user.money -= reward/2
    db.session.commit()
    return jsonify({"reward":reward})

@view.route("/admin",methods=["POST","GET"])
@login_required
def admin():
    if request.method == "GET":
        return render_template("admin.html")
    else:
        root = "root"
        name = request.form.get('name')
        task = TaskModel.query.filter_by(task=name).first()
        if task:
            return "任务已存在"
        else:
            value = request.form.get('value')
            key = request.form.get('key')
            if key != root:
                return "校验错误"
            else:
                task = TaskModel(task=name,value=value)
                db.session.add(task)
                db.session.commit()
                return redirect('/admin')
        return redirect('/admin')