from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length

class PatientForm(FlaskForm):
    first_name = StringField("Ім'я", validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Прізвище', validators=[DataRequired(), Length(max=64)])
    date_of_birth = DateField('Дата народження', validators=[DataRequired()])
    gender = SelectField('Стать', choices=[('M', 'Чоловіча'), ('F', 'Жіноча'), ('O', 'Інша')])
    contact_number = StringField('Номер телефону', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    address = TextAreaField('Адреса', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Зберегти')

class MedicalHistoryForm(FlaskForm):
    diagnosis = StringField('Діагноз', validators=[DataRequired(), Length(max=200)])
    treatment = TextAreaField('Лікування', validators=[DataRequired()])
    prescription = TextAreaField('Призначення', validators=[Optional()])
    notes = TextAreaField('Нотатки', validators=[Optional()])
    next_appointment = DateField('Дата прийому', validators=[Optional()])
    submit = SubmitField('Зберегти запис') 