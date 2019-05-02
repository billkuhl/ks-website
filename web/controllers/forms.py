from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import BooleanField, PasswordField, StringField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from web import db
from web.models import User, Role


class LoginForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class ResetPasswordForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Reset password')

    def validate_email(self, field): 
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class RequestResetPasswordForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Reset password')

    # We don't validate the email address so we don't confirm to attackers
    # that an account with the given email exists.


class CreatePasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])
    submit = SubmitField('Set password')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        'Old password',
            validators=[InputRequired(),
                        Length(8,20)]
    )
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            Length(8,20),
            EqualTo('new_password2', 'Passwords must match.')]
    )

    new_password2 = PasswordField(
        'Confirm new password', 
            validators=[InputRequired(),
                        Length(8,20)]
    )

    submit = SubmitField('Update password')


class ChangeEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Update email')

    def validate_email(self, field): 
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeUserEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field): 
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(FlaskForm):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField('Update role')


class InviteUserForm(FlaskForm):
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field): 
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewUserForm(InviteUserForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')

class UpdateUserForm(FlaskForm):
    first_name = StringField(
        'First name', 
            validators=[Optional(),
                        Length(1, 64)]
    )

    middle_initial = StringField(
        'Middle Initial',
            validators=[Optional(),
                        Length(1, 1)],
    )

    last_name = StringField(
        'Last name',
            validators=[Optional(),
                        Length(1, 64)])

    kerberos = StringField(
        'Kerberos',
            description="Enter your MIT Kerberos without '@mit.edu'. If you are \
                        an alum, just use whatever goes before '@alum.mit.edu'.",
            validators=[Optional(),
                        Length(1, 64)]
    )

    email = EmailField(
        'Email',
            validators=[Optional(),
                        Length(1, 64),
                        Email()]
    )

    class_year = IntegerField(
        'Class Year',
            validators=[Optional()])
    
    rook = IntegerField(
        'Rook Number',
            validators=[Optional()]
    )

    graduation_year = IntegerField(
        'Graduation Year',
            validators=[Optional()])

    submit = SubmitField('Update Profile')

    def validate_kerberos(self, field):
        if '@mit.edu' in str(field.data):
            raise ValidationError('Enter Kerberos without \'@mit.edu\'.')
    
    def validate_class_year(form, field):
        if len(str(field.data)) != 4:
            raise ValidationError('Please enter your full year. If you\'re a \'20, enter 2020.')

    def validate_graduation_year(form, field):
        if len(str(field.data)) != 4:
            raise ValidationError('Please enter your full year. If you\'re a \'20, enter 2020.')

    def validate_email(self, field): 
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
