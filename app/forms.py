from wtforms import Form, StringField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import Length, InputRequired


class RegisterForm(Form):
    first_name = StringField('Voornaam', [Length(max=255), InputRequired('Voer alstublieft uw voornaam in')])
    last_name = StringField('Achternaam', [Length(max=255), InputRequired('Voer alstublieft uw achternaam in')])
    street = StringField('Straat', [Length(max=255), InputRequired('Voer alstublieft uw straat in')])
    house_number = IntegerField('Huisnummer', [InputRequired('Voer alstublieft uw huisnummer in')])
    zip_code = StringField('Postcode', [Length(min=6, max=6), InputRequired('Voer alstublieft uw postcode in')])
    city = StringField('Plaats', [Length(max=255), InputRequired('Voer alstublieft uw plaats in')])
    phone_number = IntegerField('Telefoonnummer', [InputRequired('Voer alstublieft uw telefoonnummer in')])
    email = EmailField('Email adres', [Length(max=255), InputRequired('Voer alstublieft uw email adres in')])
    password = PasswordField('Wachtwoord', [InputRequired('Voer alstublieft uw password in')])


class LoginForm(Form):
    email = EmailField('Email adres', [Length(max=255), InputRequired('Voer alstublieft uw email adres in')])
    password = PasswordField('Wachtwoord', [InputRequired('Voer alstublieft uw password in')])


class MeasurementForm(Form):
    weight = IntegerField('Gewicht', [InputRequired('Voer uw gewicht in')])
    height = IntegerField('Lengte', [InputRequired('Voer uw lengte in')])


class CenterForm(Form):
    name = StringField('Naam', [Length(max=255), InputRequired('Voer alstublieft de naam in')])
    street = StringField('Straat', [Length(max=255), InputRequired('Voer alstublieft het adres in')])
    house_number = IntegerField('Huisnummer', [InputRequired('Voer alstublieft het huisnummer in')])
    zip_code = StringField('Postcode', [Length(max=6), InputRequired('Voer alstublieft de postcode in')])
    city = StringField('Stad', [Length(max=255), InputRequired('Voer alstublieft de stad in')])


class CardForm(Form):
    user_id = SelectField('Gebruiker', [InputRequired('Voer alstublieft een gebruiker in')], coerce=int)


class ActivityForm(Form):
    name = StringField('Naam', [Length(max=255), InputRequired('Voer alstublieft de naam in')])


class MachineForm(Form):
    activity_id = SelectField('Activiteit', [InputRequired('Voer alstublieft de activiteit in')], coerce=int)
    center_id = SelectField('Center', [InputRequired('Voer alstublieft de locatie in')], coerce=int)

