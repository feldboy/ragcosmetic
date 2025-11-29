from appointments import check_availability
from datetime import date, timedelta

def verify_ics():
    print("Checking availability for the next 3 days...")
    today = date.today()
    
    for i in range(3):
        check_date = today + timedelta(days=i)
        date_str = check_date.strftime("%Y-%m-%d")
        print(f"\n--- {date_str} ---")
        slots = check_availability(date_str)
        if not slots:
            print("No slots available (or error).")
        else:
            print(f"Available slots: {slots}")

if __name__ == "__main__":
    verify_ics()
