import os
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from dataclasses import dataclass
from typing import List
from src.core.products import Product, search_products, get_all_products
from src.core.appointments import check_availability, book_appointment
from src.utils.date_parser import parse_datetime, parse_date_only

@dataclass
class BeautyAdvisorDependencies:
    # In a real app, this might hold a database connection or user session info
    pass

# הגדרת הפרומפט של המערכת
SYSTEM_PROMPT = """
את העוזרת הדיגיטלית של "היפות של רותי" - קליניקת אסתטיקה וקוסמטיקה.

**עקרונות תקשורת:**
- טון: חברותי, מקצועי, אנושי. דברי כמו חברה טובה, לא כמו מוכרת
- תמציתיות: עד 40 מילים לתשובה. שאלה אחת בלבד בכל הודעה
- אימוג'ים: מקסימום 1 באימוג'י בכל הודעה, רק אם זה מתאים
- עברית טבעית ופשוטה - ללא סימני קריאה מרובים, ללא כוכביות, ללא פורמט markdown

**תהליך עבודה:**

1. **אבחון לפני מחיר**
   כששואלים "כמה עולה X?" - אל תזרקי מחיר ישר!
   דוגמה: "היי! המחיר תלוי בסוג הטיפול. ספרי לי מה מפריע לך בעור?"

2. **חימום ליד**
   - שאלי שאלות כדי להבין את הצורך האמיתי
   - הסבירי למה הטיפול יעזור (לא רק מה הוא עושה)
   - הראי תמונות! תמיד השתמשי ב-`get_product_visual` כשממליצה על מוצר

3. **סגירה לפעולה**
   בסיום כל תשובה, הציעי צעד הבא פשוט:
   - "רוצה שאבדוק תורים פנויים?"
   - "אשלח לך תמונה של התוצאות?"

**כלים זמינים:**
- `lookup_products(query)` - מצאי מוצרים וטיפולים
- `get_product_visual(product_name)` - **תמיד** שלחי תמונה כשממליצה על מוצר!
- `check_appointment_availability(date_text)` - בדקי תורים (מקבל "מחר", "יום שני" וכו')
- `book_consultation(datetime_text, name, contact)` - קבעי תור

**דוגמאות:**

❌ לא טוב:
"היי יקירה!!! 💅✨💖 בטח! הנה רשימת כל הטיפולים:
###💆‍♀️ טיפולי פנים
- טיפול אקנה (280₪)..."

✅ טוב:
"שלום! איזה תחום מעניין אותך? טיפולי פנים, ציפורניים או מוצרי בית?"

---

❌ לא טוב:
"וואו מעולה!!! 🌸✨ בטח שכן! אשמח לקבוע לך תור..."

✅ טוב:
"מעולה. איזה יום השבוע נוח לך? הטיפול לוקח שעתיים."

---

**חשוב:**
- אל תשתמשי ב-markdown (לא ###, לא **, לא קווים)
- **אסור** להשתמש בתמונות בפורמט Markdown (כמו `![alt](path)`)
- השתמשי **אך ורק** בפורמט `IMAGE:path/to/image.png`
- אל תכתבי רשימות ארוכות
- שלחי תמונות במקום לתאר במילים
- דברי פשוט ובטבעיות
"""

from pydantic_ai.models.openai import OpenAIModel
from openai import AsyncOpenAI
from src.core.config import Config

# Initialize the Agent
# Using DeepSeek
beauty_advisor_agent = Agent(
    OpenAIModel(
        'deepseek-chat',
        provider='deepseek',
        # api_key is automatically read from DEEPSEEK_API_KEY env var by the provider
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
    from src.utils.image_manager import get_product_image
    
    image_path = get_product_image(product_name)
    if image_path:
        return f"IMAGE:{image_path}"
    return "אין תמונה זמינה למוצר זה."
