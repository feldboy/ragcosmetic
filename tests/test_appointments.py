import pytest
from src.core.appointments import check_availability, book_appointment, booked_slots

class TestAppointments(unittest.TestCase):
    def setUp(self):
        booked_slots.clear()

    def test_check_availability(self):
        slots = check_availability("2023-10-27")
        self.assertIn("10:00", slots)
        self.assertIn("18:00", slots)

    def test_book_appointment_success(self):
        result = book_appointment("2023-10-27", "10:00", "Alice", "1234567890")
        self.assertIn("Success", result)
        self.assertIn("10:00", booked_slots["2023-10-27"])

    def test_book_appointment_double_booking(self):
        book_appointment("2023-10-27", "10:00", "Alice", "1234567890")
        result = book_appointment("2023-10-27", "10:00", "Bob", "0987654321")
        self.assertIn("Error", result)

    def test_book_appointment_invalid_date(self):
        result = book_appointment("invalid-date", "10:00", "Alice", "1234567890")
        self.assertIn("Error", result)

if __name__ == '__main__':
    unittest.main()
