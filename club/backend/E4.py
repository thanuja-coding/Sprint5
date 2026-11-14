from sqlalchemy .orm import Session 
import functions

def set_recruiting(id, recruiting):
    session = Session(functions.engine)
    club = session.query(functions.Clubs).filter(functions.Clubs.id == id).first()
    response = None
    if club:
        club.recruiting = recruiting
        session.commit()
        response = {
            "id": club.id,
            "name": club.name,
            "category": club.category,
            "seats": club.seats,
            "deadline": club.deadline,
            "recruiting": club.recruiting
        }
    session.close()
    return response

