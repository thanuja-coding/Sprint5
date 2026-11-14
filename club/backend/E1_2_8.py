from sqlalchemy.orm import Session
import functions

#E1
def get_all_clubs(category=None):
    session = Session(functions.engine)
    if category is None:
        clubs = session.query(functions.Clubs).all()
    else:
        clubs = session.query(functions.Clubs).filter(functions.Clubs.category == category).all()
    response = []
    for club in clubs:
        temp_club = {
            "id": club.id,
            "name": club.name,
            "category": club.category,
            "seats": club.seats,
            "deadline": club.deadline,
            "recruiting": club.recruiting,
            "applications": session.query(functions.Applications).filter(functions.Applications.club_id == club.id, functions.Applications.status != "withdrawn").count()
        }
        
        response.append(temp_club)

    session.close()
    return response

#E2
def get_club(id):
    session = Session(functions.engine)

    club = session.query(functions.Clubs).filter(functions.Clubs.id == id).first()

    if club is None:         
        session.close()       
        return None           

    applications = session.query(functions.Applications).filter(functions.Applications.club_id == id).all()

    application_list = []

    for application in applications:
        temp_application = {
            "id": application.id,
            "roll_no": application.roll_no,
            "why_join": application.why_join,
            "status": application.status,
            "applied_on": application.applied_on
        }
        application_list.append(temp_application)

    response = {
        "id": club.id,
        "name": club.name,
        "category": club.category,
        "seats": club.seats,
        "deadline": club.deadline,
        "recruiting": club.recruiting,
        "applications": application_list
    }

    session.close()
    return response

#E8
def get_student_applications(roll_no):
    session = Session(functions.engine)

    applications = session.query(functions.Applications).filter(functions.Applications.roll_no == roll_no).all()

    response = []

    for application in applications:
        club = session.query(functions.Clubs).filter(functions.Clubs.id == application.club_id).first()

        temp_application = {
            "id": application.id,
            "roll_no": application.roll_no,
            "club_id": application.club_id,
            "club_name": club.name,
            "why_join": application.why_join,
            "status": application.status,
            "applied_on": application.applied_on
        }

        response.append(temp_application)

    session.close()
    return response