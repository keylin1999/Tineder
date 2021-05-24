from . import db

class User(db.Model):
    __tablename__ = 'users'

    id                          = db.Column(db.String(33), primary_key=True)
    name                        = db.Column(db.String(20))
    picture_id                  = db.Column(db.Integer)
    status_message              = db.Column(db.String(500))
    language                    = db.Column(db.String(8))
    activate                    = db.Column(db.Integer)
    paired_id                   = db.Column(db.String(33))
    gender                      = db.Column(db.String(6))
    age                         = db.Column(db.Integer)
    prefered_gender             = db.Column(db.String(6))
    prefered_age_range_start    = db.Column(db.Integer)
    prefered_age_range_end      = db.Column(db.Integer)

    def __init__(self, 
                 user_id                    : str,
                 name                       : str,
                 picture_id                 : int,
                 status_message             : str,
                 language                   : str,
                 activate                   : int,
                 paired_id                  : int,
                 gender                     : str = None,
                 age                        : int = None,
                 prefered_gender            : str = None,
                 prefered_age_range_start   : int = None,
                 prefered_age_range_end     : int = None) -> None:
        self.id                         = user_id
        self.name                       = name
        self.picture_id                 = picture_id
        self.status_message             = status_message
        self.language                   = language
        self.activate                   = activate
        self.paired_id                  = paired_id
        self.gender                     = gender
        self.age                        = age
        self.prefered_gender            = prefered_gender
        self.prefered_age_range_start   = prefered_age_range_start
        self.prefered_age_range_end     = prefered_age_range_end

"""
get_profile returns:
{
    "displayName":"LINE taro",
    "userId":"U4af4980629...", 33 character long (https://developers.line.biz/en/faq/#what-are-user-id-groupid-roomid)
    "language":"en",           8 BCP 47 language maximum length (https://stackoverflow.com/questions/17848070/what-data-type-should-i-use-for-ietf-language-codes)
    "pictureUrl":"https://obs.line-apps.com/...", 
    "statusMessage":"Hello, LINE!"
}

informations that are helpful in pairing:
    gender
    age
"""

