# random picks other user which only prefered age is met
import sqlalchemy
from model.user import User
import random

class RandomPicker:
    
    def pair(self, user_id:str, db_session:sqlalchemy.orm.Session) -> str:
        # None if no candidate
        user = db_session.query(User).filter_by(id=user_id).first()
        result = db_session.query(User).filter_by(
            paired_id=None,
            gender=user.prefered_gender,
            prefered_gender=user.gender
        )

        if result.count() > 0:
            paired_user_index = random.randint(1, result.count())
            paired_user_index = paired_user_index - 1
            paired_user = result.all()[paired_user_index]

            paired_user.paired_id = user_id
            user.paired_id = paired_user.id
            db_session.commit()
        else:
            return None

        return paired_user.id

# if __name__ == '__main__':
#     from test_use.return_db import db
#     print(RandomPicker().pair("Uaa379e85866bc38e672bbf641d77bc60", db.session))

    

