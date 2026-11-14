from sqlalchemy import func
from sqlalchemy.orm import Session
import functions


def get_summary():
    session = Session(functions.engine)

    rows = session.query(functions.Clubs.id, functions.Clubs.name, functions.Applications.status, func.count(functions.Applications.id)).outerjoin(functions.Applications).group_by(functions.Clubs.id, functions.Applications.status).all()

    summary = {}

    for row in rows:
        club_id = row[0]
        if club_id not in summary:
            summary[club_id] = {"club_id": row[0], "club_name": row[1], "applied": 0, "shortlisted": 0, "selected": 0, "rejected": 0}
        if row[2] in ["applied", "shortlisted", "selected", "rejected"]:
            summary[club_id][row[2]] = row[3]

    session.close()
    return list(summary.values())
