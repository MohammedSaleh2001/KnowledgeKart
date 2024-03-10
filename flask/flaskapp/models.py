from . import db
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user):
        self.id = user[0]
        self.email = user[1]
        self.password = user[2]
        self.name = user[3]
        self.datejoined = user[4]
        self.role = user[5] 
        self.verified = user[6] 
        self.blacklisted = user[7] 
        self.blacklisteduntil = user[8] 
        self.politeness = user[9] 
        self.honesty = user[10] 
        self.quickness = user[11] 
        self.numreviews = user[12]
