# Club Recruitment

## Problem Statement

A new academic year brings new faces, fresh ambitions, and countless opportunities. But with dozens of clubs competing for attention and hundreds of students eager to join, where does the excitement end and the chaos begin?

The coder searches for a tech club, the dancer dreams of the stage, and the athlete looks for their team. Yet, between scattered announcements, missed deadlines, duplicate applications, limited seats, and endless follow-ups, finding the right club becomes harder than it should be.

While students are left wondering, "Did I get selected?", coordinators are buried in applications, struggling to track candidates and manage fair selections.
A campus full of connections shouldn't have a recruitment process full of confusion.

The challenge is simple: How can we bring every club, every applicant, and every opportunity under one roof, making recruitment transparent, organized, and fair?


## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What are you doing? |
|---|---|---|
| Day 1 | Jiken Pulinbhai Jasoliya | Doing the first 3 Endpoints (endpoints: 1, 2, 8) |
| Day 1 | Abhishek.N | doing endpoints 4, 9  |
| Day 1 | Thanuja | Doing 3rd and 7th end points |
| Day 1 | Sanghavi |working on clubs table, 5th and 6th endpoints  |
| Day 2 | Thanuja |Testing the Backend and debugging  |
| Day 2 | Sanghavi | working on main.py  |
| Day 2 | Jiken | Starting on the frontend  |
| Day 2 | Abhishek |Starting on the Frontend  |
| Day 3 | Thanuja | Debuggin backend, updating the endpoints |
| Day 3 | Sanghavi | Debuggin backend, updating the endpoints  |
| Day 3 | Jiken | adding the more to the frontend, updating the endpoints   |
| Day 3 | Abhishek |updating E9.py, working on frontend   |

## 2. Endpoint tracker

Fill in the method and path from your PRD's endpoint table. 

| # | Method  | path | Request Body | Success Code | Error Codes |
|---|---|---|---|---|---|
| E1 | GET | /clubs | Optional: category |200  |422  |
| E2 | GET | /clubs/{clubs.id} | /{clubs.id} | 200 | 404 |
| E3 |post  | /clubs |name , category ,seats,deadline  | 201 | 422 |
| E4 | PATCH  | clubs/{club_id}/recruiting  | recruiting  |200  |404,422  |
| E5 | POST | /clubs/{club_id}/applications | roll_no, why_join |201  | 400,404,422 |
| E6 | PATCH | /applications/{application_id}/status | status |200 |400,404,422  |
| E7 |patch |/applications/{applications_id}/withdraw |roll_no | 200 |400,403,404,422  |
| E8 | GET | /students | /{roll_no}/applications | 200| 422 |
| E9 | GET |  /summary |NONE  | 200 |  |
## File Structure

```text
full-stack-development-project/
│
├── backend/
│   ├── E1_2_8.py
│   ├── E3.py
│   ├── E4.py
│   ├── E5.py
│   ├── E6.py
│   ├── E9.py
│   ├── functions.py
│   ├── main.py
│   ├── recruitment.db
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       │   ├── AddClub.jsx
│       │   ├── ClubItem.jsx
│       │   ├── ClubList.jsx
│       │   └── MyApplications.jsx
│       │
│       ├── App.jsx
│       ├── main.jsx
│       └── index.css
│
└── README.md
```
## How to Run

Backend

Open a terminal and navigate to the backend folder:
cd backend
Install dependencies:
pip install fastapi uvicorn sqlalchemy

Start the FastAPI server:
python -m uvicorn main:app --reload --port 8000

Open the API documentation:
Swagger UI: http://127.0.0.1:8000/docs

Frontend

Navigate to the frontend folder:
cd frontend
Install dependencies:
npm install

Start the React development server:
npm run dev

Open the local URL displayed in the terminal.

### flow of the Project Presentation 

->	Problem statement 
->	Distribution of work 
->	API contracts 
->	Frontend Demo 
->	Swagger 
->	File structure 
->	Conclusion 
->	Interesting findings
->	QNA

