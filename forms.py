from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class SignUpForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField(
        "Email",
        validators=[
            Length(min=6),
            Email(message="Please enter a valid email."),
            DataRequired(),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            Length(min=6, message="Please select a stronger password"),
            DataRequired(),
        ],
    )
    password_confirm = PasswordField(
        "Confirm Your Password",
        validators=[
            EqualTo("password", message="Passwords must match"),
            DataRequired(),
        ],
    )

    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):

    email = StringField(
        "Email", validators=[DataRequired(), Email(message="Enter a valid email.")]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
