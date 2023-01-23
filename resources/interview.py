from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId

from db import interview_collection
from schemas import InterviewSchema, InterviewUpdateSchema

blp = Blueprint("interview", __name__, description="Operations on interview records")


@blp.route("/interview")
class InterviewCreate(MethodView):

    @blp.arguments(InterviewSchema)
    def post(self, interview_data):
        """Create the interview record in 'interview_db' database"""

        interviewer_name = interview_data["interviewer_name"]
        date_time_of_interview = interview_data["date_time_of_interview"].strftime("%Y-%m-%d %H:%M")

        # Check if Interviewer already has the appointment for this date and time.
        if interview_collection.find_one(
                {"interviewer_name": interviewer_name,
                 "date_time_of_interview": date_time_of_interview}):
            abort(404, message=f"{interviewer_name} already has an interview appointment at {date_time_of_interview}")

        # Create a record and save it to database.
        interview_record = {
            "interviewer_name": interviewer_name,
            "interviewee_name": interview_data["interviewee_name"],
            "date_time_of_interview": date_time_of_interview,
            "note": interview_data.get("note"),
            "date_time_created_record": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "date_time_updated_record": None
        }

        interview_collection.insert_one(interview_record)

        return {"message": f"Interview record created. Interviewer: {interviewer_name}"}


@blp.route("/interview/<id>")
class InterviewUpdateDelete(MethodView):

    @blp.arguments(InterviewUpdateSchema)
    def put(self, interview_data, id):
        """Update the existing interview record."""

        interview_to_update = {"_id": ObjectId(id)}

        # Check if interview record exists or not in database.
        if not interview_collection.find_one(interview_to_update):
            abort(404, message="Interview is not found.")

        # Update the interview record. Only note field is allowed to be updated
        new_interview_note = {"$set": {
            "note": interview_data["note"],
            "date_time_updated_record": datetime.now().strftime("%Y-%m-%d %H:%M")
        }}
        interview_collection.update_one(interview_to_update, new_interview_note)

        return {"message": "Interview record updated"}

    def delete(self, id):
        """Delete the existing interview record."""

        interview_to_update = {"_id": ObjectId(id)}

        # Check if interview record exists or not in database.
        if not interview_collection.find_one(interview_to_update):
            abort(404, message="Interview is not found.")

        # Delete the interview record.
        interview_collection.delete_one(interview_to_update)

        return {"message": "Interview record deleted"}
