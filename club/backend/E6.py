from sqlalchemy.orm import Session
import functions

def update_application_status(application_id, status):
    session = Session(functions.engine)

    application = session.query(functions.Applications).filter(functions.Applications.id == application_id).first()
    if application is None:
        session.close()
        return None

    application.status = status

    response = {
        "id": application.id,
        "club_id": application.club_id,
        "roll_no": application.roll_no,
        "why_join": application.why_join,
        "status": application.status,
        "applied_on": application.applied_on
    }

    session.commit()
    session.close()

    return response

def get_selected_count(club_id):
    session = Session(functions.engine)
    count = session.query(functions.Applications).filter(functions.Applications.club_id == club_id, functions.Applications.status == "selected").count()
    session.close()
    return count


def get_student_selected_count(roll_no):
    session = Session(functions.engine)
    count = session.query(functions.Applications).filter(functions.Applications.roll_no == roll_no, functions.Applications.status == "selected").count()
    session.close()
    return count