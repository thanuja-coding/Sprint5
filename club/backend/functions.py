from sqlalchemy import Integer, String, Column, create_engine , ForeignKey
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime, timedelta, timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

DB_PATH = "recruitment.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7*24*60
SECRET_KEY = "SECRETCODE"
ALGORITHM = "HS256"

class Clubs(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    seats = Column(Integer)
    deadline = Column(String)
    recruiting = Column(Integer)


class Applications(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    club_id = Column(Integer,ForeignKey("clubs.id"))
    roll_no = Column(Integer)
    why_join = Column(String)
    status = Column(String)
    applied_on = Column(String)


class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    password = Column(String)
    role = Column(String, default="student")

Base.metadata.create_all(engine)


def verify_login(username,password):
    session = Session(engine)
    user = session.query(User).filter_by(user_name=username).first()
    if user is None:
        session.close()
        return False
    try :
        ph.verify(user.password,password)
    except VerifyMismatchError:
        session.close()
        return False

    access_token = create_token(username=username,token_type="access",role=user.role)
    refresh_token= create_token(username=username,token_type="refresh",role=user.role)

    session.close()
    return {"access_token":access_token,"refresh_token":refresh_token}


def create_token(username,token_type,role):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload={
        "role":role,
        "username":username,
        "token_type":token_type,
        "exp":datetime.now(timezone.utc)+timedelta(minutes=time)
    }
    token =jwt.encode(payload=payload,key=SECRET_KEY,algorithm=ALGORITHM)
    return token


def verify_token(token,token_type):
    try:
        payload = jwt.decode(jwt=token,key=SECRET_KEY,algorithms=[ALGORITHM])
    except:
        return False

    if payload ["token_type"] == token_type:
        return payload
    return False


def register_user(user_name :str, password: str, role: str):
    session = Session(engine)
    user_exists = session.query(User).filter_by(user_name = user_name).first()
    if user_exists is not None:
        session.close()
        return False

    try:
        hashed_password = ph.hash(password)
    except Exception:
        session.close()
        return False

    session.add(User(user_name=user_name, password=hashed_password, role=role))
    session.commit()
    session.close()
    return True