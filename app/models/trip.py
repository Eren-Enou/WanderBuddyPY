from app import db

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False) # Assuming the budget is a floating-point number to account for cents/dollars.
    will_fly = db.Column(db.Boolean, nullable=False, default=False) # True if "yes", False if "no"
    description = db.Column(db.Text, nullable=True) # Text type for longer descriptions
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Trip to {self.destination} from {self.start_date} to {self.end_date}>'
