from sqlalchemy.orm import Session
import functions

def get_application(id):
    session = Session(functions.engine)
    application = session.query(functions.Applications).filter(functions.Applications.id == id).first()
    response = None
    if application:
        response={
            "id": application.id,
            "club_id": application.club_id,
            "roll_no": application.roll_no,
            "why_join": application.why_join,
            "status": application.status,
            "applied_on": application.applied_on
        }
    session.close()
    return response

def withdraw_application(id):
    session = Session(functions.engine)
    application = session.query(functions.Applications).filter(functions.Applications.id == id).first()
    response = None
    if application:
        application.status = "withdrawn"
        session.commit()
        response={
            "id": application.id,
            "club_id": application.club_id,
            "roll_no": application.roll_no,
            "why_join": application.why_join,
            "status": application.status,
            "applied_on": application.applied_on
        }
    session.close()
    return response