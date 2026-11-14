from sqlalchemy.orm import Session
from datetime import datetime
import functions

def apply_to_club(club_id, roll_no, why_join):
    session = Session(functions.engine)

    application = functions.Applications(club_id=club_id, roll_no=roll_no, why_join=why_join, status="applied", applied_on=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    session.add(application)
    session.commit()

    response = {
        "id": application.id,
        "club_id": application.club_id,
        "roll_no": application.roll_no,
        "why_join": application.why_join,
        "status": application.status,
        "applied_on": application.applied_on
    }
    session.close()
    return response
    
def get_active_application_count(roll_no):
    session = Session(functions.engine)
    applied = session.query(functions.Applications).filter(functions.Applications.roll_no == roll_no, functions.Applications.status == "applied").count()
    shortlisted = session.query(functions.Applications).filter(functions.Applications.roll_no == roll_no, functions.Applications.status == "shortlisted").count()
    session.close()
    return applied + shortlisted