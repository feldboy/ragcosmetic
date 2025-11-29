import os
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from dataclasses import dataclass
from typing import List
from products import Product, search_products, get_all_products
from appointments import check_availability, book_appointment
from date_parser import parse_datetime, parse_date_only

@dataclass
class BeautyAdvisorDependencies:
    # In a real app, this might hold a database connection or user session info
    pass

# הגדרת הפרומפט של המערכת
SYSTEM_PROMPT = """
את יועצת יופי דיגיטלית מקצועית למכון קוסמטיקה יוקרתי. 
את חמה, נעימה, מקצועית ומאוד שירותית! 💅✨

**כללים חשובים:**
1. **תמציתיות** - עד 30 מילים לתשובה (אלא אם מסבירים על מוצר).
2. **שאלה אחת בלבד** - לעולם לא לשאול 2+ שאלות בהודעה אחת.
3. **תראי, אל תספרי** - השתמשי בכלי `get_product_visual` כדי לשלוח תמונות במקום תיאורים ארוכים.
4. **ישר לעניין** - אחרי ההודעה הראשונה, ישר לעניין בלי דיבורים מיותרים.
5. **דברי בשפת הלקוחה** - אם היא אומרת "קמטים", אל תאמרי "קווי מתאר".
6. **כתב ויתור רפואי** - אם מזכירים מצבים חמורים (מוגלה, כוויות), להפנות לרופא.
7. **רק מוצרים אמיתיים** - השתמשי בכלים `lookup_products` או `list_all_products`. לעולם אל תמציאי מוצרים.
8. **התמחות בקוסמטיקה** - את מתמחה גם בלק ג'ל, פדיקור, מניקור, טיפולי פנים ועיצוב גבות.

**הכלים שלך:**
- `get_product_visual(product_name)` - שליחת תמונת מוצר
- `lookup_products(query)` - חיפוש מוצרים
- `check_appointment_availability(date)` - בדיקת תורים פנויים
- `book_consultation(date, time, name, contact)` - קביעת תור

**טיפים לתמציתיות:**
- השתמשי באימוג'ים במקום מילים (✅ במקום "כן, נכון")
- פצלי הודעות ארוכות לשתיים קצרות
- תני לתמונות לדבר בשבילך
- דלגי על ביטויי מעבר

**מתי להציע תור:**
- הלקוחה מבקשת להיפגש עם מישהו
- בעיות עור מורכבות
- חוסר החלטיות אחרי המלצות
- בקשה לטיפול לק ג'ל, פדיקור או מניקור

**דוגמאות:**
לקוחה: "יש לי עור יבש"
את: "הבנתי! זה מרגיש מתוח בבוקר? 💧"

לקוחה: "תראי לי קרמים נגד קמטים"
את: [השתמשי ב-get_product_visual + lookup_products] "מושלם לחליקת קווים ✨ את משתמשת לפני או אחרי ניקוי?"

לקוחה: "רוצה לקבוע תור ללק ג'ל"
את: "מעולה! איזה תאריך נוח לך? 💅"
"""

from pydantic_ai.models.openai import OpenAIModel

# Initialize the Agent
# Using OpenRouter
beauty_advisor_agent = Agent(
    OpenAIModel(
        'x-ai/grok-4.1-fast:free',
        provider='openrouter',
    ),
    deps_type=BeautyAdvisorDependencies,
    instructions=SYSTEM_PROMPT,
)

@beauty_advisor_agent.tool
def lookup_products(ctx: RunContext[BeautyAdvisorDependencies], query: str) -> List[Product]:
    """
    חיפוש מוצרים במאגר הידע לפי שאילתא (שם, קטגוריה, בעיה או תועלת).
    השתמשי בכלי זה כדי למצוא את המוצרים הנכונים להמליץ עליהם.
    """
    return search_products(query)

@beauty_advisor_agent.tool
def list_all_products(ctx: RunContext[BeautyAdvisorDependencies]) -> List[Product]:
    """
    קבלת רשימה של כל המוצרים הזמינים. שימושי אם רוצים לראות מה זמין באופן כללי.
    """
    return get_all_products()

@beauty_advisor_agent.tool
def check_appointment_availability(ctx: RunContext[BeautyAdvisorDependencies], date_text: str) -> List[str]:
    """
    בדיקת תורים פנויים לתאריך נתון.
    מקבל קלט בשפה טבעית בעברית או אנגלית.
    
    Args:
        date_text: תאריך בשפה טבעית כמו "מחר", "ביום חמישי הבא", "tomorrow".
    
    דוגמאות:
        - "מחר" / "tomorrow"
        - "ביום שני הבא" / "next Monday"
        - "2025-12-01" (מקבל גם פורמט סטנדרטי)
    """
    # Parse the natural language date
    date_str = parse_date_only(date_text)
    
    if not date_str:
        return [f"Error: Could not understand date '{date_text}'. Try 'tomorrow' or 'מחר'."]
    
    return check_availability(date_str)

@beauty_advisor_agent.tool
def book_consultation(ctx: RunContext[BeautyAdvisorDependencies], datetime_text: str, user_name: str, contact_info: str) -> str:
    """
    קביעת תור לייעוץ.
    מקבל קלט תאריך ושעה בשפה טבעית בעברית או אנגלית.
    
    Args:
        datetime_text: תאריך ושעה בשפה טבעית כמו "מחר בשעה 15:00", "tomorrow at 3pm".
        user_name: שם הלקוחה.
        contact_info: מספר טלפון או אימייל.
    
    דוגמאות:
        - "מחר בשעה 3 אחרי הצהריים" / "tomorrow at 3pm"
        - "ביום חמישי בשעה 14:00" / "Thursday at 14:00"
    """
    # Parse the natural language datetime
    date_str, time_str = parse_datetime(datetime_text)
    
    if not date_str or not time_str:
        return f"Error: Could not understand date/time '{datetime_text}'. Please include both date and time, e.g., 'tomorrow at 3pm'."
    
    return book_appointment(date_str, time_str, user_name, contact_info)

@beauty_advisor_agent.tool
def get_product_visual(ctx: RunContext[BeautyAdvisorDependencies], product_name: str) -> str:
    """
    קבלת נתיב התמונה של מוצר כדי להראות ללקוחה איך הוא נראה.
    השתמשי בכלי זה כאשר ממליצים על מוצר כדי לספק התייחסות ויזואלית.
    
    Args:
        product_name: שם המוצר.
        
    Returns:
        נתיב התמונה אם נמצא, או הודעת שגיאה.
    """
    from image_manager import get_product_image
    
    image_path = get_product_image(product_name)
    if image_path:
        return f"IMAGE:{image_path}"
    return "אין תמונה זמינה למוצר זה."
