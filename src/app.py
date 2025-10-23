"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")
        ADDITIONAL_ACTIVITIES = {
            # Sports (2)
            "Soccer Team": {
                "description": "Competitive soccer team that plays inter-school matches and practices tactical skills.",
                "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 6:00 PM",
                "max_participants": 25,
                "participants": ["liam@mergington.edu", "ava@mergington.edu"]
            },
            "Basketball Team": {
                "description": "Organized basketball team with practice sessions and weekend games.",
                "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:30 PM",
                "max_participants": 15,
                "participants": ["ethan@mergington.edu", "isabella@mergington.edu"]
            },

            # Artistic (2)
            "Art Club": {
                "description": "Explore drawing, painting, and mixed media projects in a collaborative studio environment.",
                "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
                "max_participants": 20,
                "participants": ["noah@mergington.edu"]
            },
            "Drama Club": {
                "description": "Acting, play production, and stagecraft for students interested in theater.",
                "schedule": "Mondays and Thursdays, 5:00 PM - 7:00 PM",
                "max_participants": 30,
                "participants": ["mia@mergington.edu"]
            },

            # Intellectual (2)
            "Debate Team": {
                "description": "Prepare for debate competitions, practice public speaking, and develop argumentation skills.",
                "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
                "max_participants": 16,
                "participants": ["noelle@mergington.edu"]
            },
            "Robotics Club": {
                "description": "Design, build, and program robots for challenges and competitions.",
                "schedule": "Thursdays, 3:30 PM - 5:30 PM",
                "max_participants": 18,
                "participants": ["alex@mergington.edu", "zoe@mergington.edu"]
            }
        }

        @app.on_event("startup")
        def merge_additional_activities():
            # Add the extra activities into the in-memory database at startup.
            # The 'activities' dict is defined later in the module, so this runs
            # after module import when the app starts.
            activities.update(ADDITIONAL_ACTIVITIES)
# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
# Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
