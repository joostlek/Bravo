from app import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    zip_code = db.Column(db.String(6), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean)

    measurements = db.relationship("Measurement", back_populates="user")
    cards = db.relationship("Card", back_populates="user")
    exercises = db.relationship("Exercise", back_populates="user")

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

    def is_active(self):
        return True

    def construct_name(self):
        return self.first_name + ' ' + self.last_name or ''

    def construct_address(self):
        return "{0} {1} {2} {3}".format(self.street, self.house_number, self.zip_code, self.city)


class Measurement(db.Model):
    __tablename__ = 'measurement'
    measure_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    date = db.Column(db.Date, nullable=False)

    user = db.relationship("User", back_populates="measurements")


class Card(db.Model):
    __tablename__ = 'card'

    card_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    user = db.relationship("User", back_populates="cards")
    checks = db.relationship("Check", back_populates="card")


class Check(db.Model):
    __tablename__ = 'check'

    session_id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("card.card_id"), nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey("center.center_id"), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    in_out = db.Column(db.Boolean, nullable=False)

    card = db.relationship("Card", back_populates="checks")
    center = db.relationship("Center", back_populates="checks")


class Center(db.Model):
    __tablename__ = 'center'

    center_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    zip_code = db.Column(db.String(6), nullable=False)
    city = db.Column(db.String(255), nullable=False)

    checks = db.relationship("Check", back_populates="center")
    machines = db.relationship("Machine", back_populates="center")

    def construct_address(self):
        return "{0} {1} {2} {3}".format(self.street, self.house_number, self.zip_code, self.city)


class Machine(db.Model):
    __tablename__ = 'machine'

    machine_id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.activity_id"), nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey("center.center_id"), nullable=False)

    activity = db.relationship("Activity", back_populates="machines")
    center = db.relationship("Center", back_populates="machines")
    exercise = db.relationship("Exercise", back_populates="machine")


class Exercise(db.Model):
    __tablename__ = 'exercise'

    exercise_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    burnt_calories = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey("machine.machine_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    constant_id = db.Column(db.Integer, db.ForeignKey("constant.constant_id"), nullable=False)

    machine = db.relationship("Machine", back_populates="exercise")
    user = db.relationship("User", back_populates="exercises")
    constant = db.relationship("Constant", back_populates="exercise")


class Activity(db.Model):
    __tablename__ = 'activity'

    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    machines = db.relationship("Machine", back_populates="activity")
    constants = db.relationship("Constant", back_populates="activity")


class Constant(db.Model):
    __tablename__ = 'constant'

    constant_id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.activity_id"), nullable=False)
    speed = db.Column(db.Integer, nullable=True)
    constant = db.Column(db.Float, nullable=False)

    activity = db.relationship("Activity", back_populates="constants")
    exercise = db.relationship("Exercise", back_populates="constant")
