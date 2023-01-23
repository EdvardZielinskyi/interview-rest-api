import unittest
import requests


class TestInterviewAPI(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/interview"
    INTERVIEW_VALID_OBJECT = {
        "interviewer_name": "John",
        "interviewee_name": "Alex",
        "date_time_of_interview": "2023-02-26 14:35"
    }
    INTERVIEW_PAST_DATE_OBJECT = {
        "interviewer_name": "John",
        "interviewee_name": "Alex",
        "date_time_of_interview": "2023-01-14 14:35"
    }

    INTERVIEW_INCORRECT_DATE_OBJECT = {
        "interviewer_name": "John",
        "interviewee_name": "Alex",
        "date_time_of_interview": "2023-02-26-14-35"
    }

    INTERVIEW_NAME_FIELD_INT_OBJECT = {
        "interviewer_name": 64,
        "interviewee_name": "Alex",
        "date_time_of_interview": "2023-02-26 14:35"
    }

    INTERVIEW_WITH_NOTE_OBJECT = {
        "interviewer_name": "John",
        "interviewee_name": "Alex",
        "date_time_of_interview": "2023-02-27 14:35",
        "note": "This is note"
    }

    UPDATED_INTERVIEW_OBJECT = {
       "note": "Update this note"
    }

    # Test post method of valid interview record.
    def test_1_post_valid_interview(self):
        response = requests.post(self.API_URL, json=self.INTERVIEW_VALID_OBJECT)
        name = self.INTERVIEW_VALID_OBJECT["interviewer_name"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], f"Interview record created. Interviewer: {name}")

    # Test post method of already created interview record.
    # The same interviewer is unable to have two interviews at the same time.
    def test_2_post_existing_interview(self):
        response = requests.post(self.API_URL, json=self.INTERVIEW_VALID_OBJECT)
        name = self.INTERVIEW_VALID_OBJECT["interviewer_name"]
        date_time = self.INTERVIEW_VALID_OBJECT["date_time_of_interview"]
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], f"{name} already has an interview appointment at {date_time}")

    # Test post method of interview record with past date.
    def test_3_post_past_time_interview(self):
        response = requests.post(self.API_URL, json=self.INTERVIEW_PAST_DATE_OBJECT)
        response_message = response.json()["errors"]["json"]["date_time_of_interview"]
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response_message, ["Input upcoming date and time only"])

    # Test post method of interview record with incorrect format of date and time.
    def test_4_post_incorrect_format_date_of_interview(self):
        response = requests.post(self.API_URL, json=self.INTERVIEW_INCORRECT_DATE_OBJECT)
        response_message = response.json()["errors"]["json"]["date_time_of_interview"]
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response_message, ["Not a valid datetime."])

    # Test post method of interview record with incorrect format of name.
    def test_5_post_name_as_int(self):
        response = requests.post(self.API_URL, json=self.INTERVIEW_NAME_FIELD_INT_OBJECT)
        response_message = response.json()["errors"]["json"]["interviewer_name"]
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response_message, ["Not a valid string."])

    # Test post method of interview record with note.
    def test_6_post_interview_with_note(self):
        response = requests.post(self.API_URL, json=self.INTERVIEW_WITH_NOTE_OBJECT)
        name = self.INTERVIEW_VALID_OBJECT["interviewer_name"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], f"Interview record created. Interviewer: {name}")

    # Test put method of existing interview record.
    def test_7_update_existing_interview(self):
        id = "/63cea8ad096d9e1f9d683b4c"
        response = requests.put(self.API_URL + id, json=self.UPDATED_INTERVIEW_OBJECT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Interview record updated")

    # Test put method of not existing interview record.
    def test_8_update_not_existing_interview(self):
        id = "/63ca900fc22d3b9d078afa30"
        response = requests.put(self.API_URL + id, json=self.UPDATED_INTERVIEW_OBJECT)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "Interview is not found.")

    # Test delete method of existing interview record.
    def test_9_delete_existing_interview(self):
        id = "/63cea8ad096d9e1f9d683b4c"
        response = requests.delete(self.API_URL + id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Interview record deleted")

    if __name__ == "__main__":
        unittest.main()

