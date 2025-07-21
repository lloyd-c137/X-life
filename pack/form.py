import wtforms
from wtforms import Form
from wtforms.validators import Length,EqualTo
from models import UserModel

class RegisterForm(Form):
    username = wtforms.StringField(validators=[Length(min=3,max=10,message="用户名格式错误")])
    password = wtforms.StringField(validators=[Length(min=8,max=20,message="密码格式错误")])
    confirm_password = wtforms.StringField(validators=[EqualTo("password",message="两次输入的密码不一致")])
    def validate_username(self,field):
        username = field.data
        user = UserModel.query.filter_by(username=username).first()
        if user:
            raise wtforms.ValidationError(message="该用户名已被注册")
class LoginForm(Form):
    username = wtforms.StringField(validators=[Length(min=3,max=10,message="用户名格式错误")])
    password = wtforms.StringField(validators=[Length(min=8,max=20,message="密码格式错误")])
