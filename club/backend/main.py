from fastapi import FastAPI, HTTPException, Header, Body
from pydantic import BaseModel, Field
import functions
from fastapi.middleware.cors import CORSMiddleware 
import E1_2_8
import E3
import E4
import E5
import E6
import E7
import E9
from datetime import datetime

app = FastAPI(
    title="Club Recruitment API",
    description="Manage clubs and student applications"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins={"http://localhost:5173", "http://127.0.0.1:5173"},
    allow_methods={"*"},
    allow_headers={"*"},
)

ROLES = ["coordinator", "student"]


def authorize(token, allowed_roles):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    if payload["role"] not in allowed_roles:
        raise HTTPException(status_code=403, detail="You do not have permission to do this")
    return payload


class ClubCreate(BaseModel):
    name: str = Field(min_length=1)
    category: str
    seats: int = Field(ge=1, le=30)
    deadline: str


class RecruitmentUpdate(BaseModel):
    recruiting: bool


class ApplicationCreate(BaseModel):
    roll_no: int = Field(gt=0)
    why_join: str = Field(min_length=20)


class StatusUpdate(BaseModel):
    status: str = Field(min_length=1)


class WithdrawRequest(BaseModel):
    roll_no: int = Field(gt=0)

@app.get("/clubs")
def clubs(category=None, token=Header(None)):
    authorize(token, ["coordinator", "student"])

    if category:
        if category not in ["technical", "cultural", "sports", "social", "literary"]:
            raise HTTPException(status_code=422, detail="Invalid category")

    return E1_2_8.get_all_clubs(category=category)

@app.get("/clubs/summary")
def club_summary(token=Header(None)):
    authorize(token, ["coordinator"])
    response = E9.get_summary()

    if response is None:
        raise HTTPException(status_code=404, detail="Summary not found")

    return response


@app.get("/clubs/{club_id}")
def club(club_id: int, token=Header(None)):
    authorize(token, ["coordinator", "student"])

    response = E1_2_8.get_club(id=club_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Club not found")

    return response

@app.post("/clubs")
def add_club(data: ClubCreate, token=Header(None)):
    authorize(token, ["coordinator"])
    name = data.name
    category = data.category
    seats = data.seats
    deadline = data.deadline

    if name == "" or category == "" or deadline == "":
        raise HTTPException(status_code=422, detail="Fields cannot be empty")

    if category not in ["technical", "cultural", "sports", "social", "literary"]:
        raise HTTPException(status_code=422, detail="Invalid category")

    if seats < 1 or seats > 30:
        raise HTTPException(status_code=422, detail="Seats must be between 1 and 30")

    try:
        dt = datetime.strptime(deadline,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as v:
        raise HTTPException(status_code=422, detail="Invalid DateTime Format")

    return E3.add_club(name=name, category=category, seats=seats, deadline=dt)

@app.patch("/clubs/{club_id}/recruitment")
def recruitment(club_id: int, data: RecruitmentUpdate, token=Header(None)):
    authorize(token, ["coordinator"])
    recruiting = data.recruiting

    response = E4.set_recruiting(id=club_id, recruiting=recruiting)

    if response is None:
        raise HTTPException(status_code=404, detail="Club not found")

    return response

@app.post("/clubs/{club_id}/applications")
def apply(club_id: int, data: ApplicationCreate, token=Header(None)):
    authorize(token, ["student"])
    roll_no = data.roll_no
    why_join = data.why_join

    club = E1_2_8.get_club(id=club_id)

    if club is None:
        raise HTTPException(status_code=404, detail="Club not found")

    if roll_no <= 0:
        raise HTTPException(status_code=422, detail="Invalid roll number")


    if len(why_join) < 20:
        raise HTTPException(status_code=422, detail="Reason must be at least 20 characters")
    
    deadline = datetime.strptime(club["deadline"], "%Y-%m-%d %H:%M:%S")

    if deadline < datetime.now():
        raise HTTPException(status_code=400, detail="Application deadline has passed")

    if club["recruiting"] == 0:
        raise HTTPException(status_code=400, detail="Recruitment is closed")

    applications = E1_2_8.get_student_applications(roll_no=roll_no)

    for application in applications:
        if application["club_id"] == club_id:

            if application["status"] == "applied":
                raise HTTPException(status_code=400, detail="Already applied to this club")

            if application["status"] == "shortlisted":
                raise HTTPException(status_code=400, detail="Already applied to this club")

            if application["status"] == "selected":
                raise HTTPException(status_code=400, detail="Already applied to this club")

            if application["status"] == "rejected":
                raise HTTPException(status_code=400, detail="Already applied to this club")

    active_applications = E5.get_active_application_count(roll_no=roll_no)

    if active_applications >= 3:
        raise HTTPException(status_code=400, detail="Maximum 3 active applications allowed")

    return E5.apply_to_club(club_id=club_id, roll_no=roll_no, why_join=why_join)


@app.patch("/applications/{application_id}/status")
def update_status(application_id: int, data: StatusUpdate, token=Header(None)):
    authorize(token, ["coordinator"])
    status = data.status

    application = E7.get_application(id=application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    allowed = {"applied": ["shortlisted", "rejected"], "shortlisted": ["selected", "rejected"]}

    if application["status"] not in allowed:
        raise HTTPException(status_code=400, detail="This move is not allowed")

    if status not in allowed[application["status"]]:
        raise HTTPException(status_code=400, detail="This move is not allowed")

    if status == "selected":

        club = E1_2_8.get_club(id=application["club_id"])

        selected_applications = E6.get_selected_count(club_id=application["club_id"])

        if selected_applications >= club["seats"]:
            raise HTTPException(status_code=400, detail="This club has already filled all its seats.")

        student_selected = E6.get_student_selected_count(roll_no=application["roll_no"])

        if student_selected >= 2:
            raise HTTPException(status_code=400, detail="Student is already selected by 2 clubs")

    return E6.update_application_status(application_id=application_id, status=status)


@app.patch("/applications/{application_id}/withdraw")
def withdraw(application_id: int, data: WithdrawRequest, token=Header(None)):
    authorize(token, ["student"])
    roll_no = data.roll_no

    application = E7.get_application(id=application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    if application["roll_no"] != roll_no:
        raise HTTPException(status_code=403, detail="This is not your application")

    if application["status"] != "applied":
        raise HTTPException(status_code=400, detail="Only applied applications can be withdrawn")

    return E7.withdraw_application(id=application_id)


@app.get("/students/{roll_no}/applications")
def student_applications(roll_no: int, token=Header(None)):
    authorize(token, ["coordinator", "student"])

    return E1_2_8.get_student_applications(roll_no=roll_no)


@app.post("/register")
def register_user(user_name=Body(), password=Body(), role=Body("student")):
    if role not in ROLES:
        raise HTTPException(status_code=400, detail="Role must be coordinator or student")
    if functions.register_user(user_name=user_name, password=password, role=role):
        return {"message": "user registered successfully"}
    raise HTTPException(status_code=400, detail="User already exists")


@app.post("/login")
def login(username=Body(), password=Body()):
    token = functions.verify_login(username=username, password=password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return token


@app.post("/refresh")
def refresh(refresh_token=Header(None)):
    payload = functions.verify_token(token=refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired refresh token")

    access_token = functions.create_token(username=payload["username"], token_type="access", role=payload["role"])
    return {"access_token": access_token}