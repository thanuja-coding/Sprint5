from sqlalchemy.orm import Session
import functions 

def add_club(name, category, seats, deadline):
    session = Session(functions.engine)
    club = functions.Clubs(name=name, category=category, seats=seats, deadline=deadline, recruiting=1)
    session.add(club)
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





