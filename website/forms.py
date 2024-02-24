from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class ProductForm(FlaskForm):
    product = HiddenField()
    submit = SubmitField()
