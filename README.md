# RAG Cosmetic - Digital Beauty Advisor 💅

בוט Telegram חכם למתן ייעוץ קוסמטי והזמנת תורים למכון "היפות של רותי".

## תכונות

- 🤖 עוזרת דיגיטלית חברותית ומקצועית
- 💬 שיחה טבעית בעברית
- 📸 המלצות מוצרים עם תמונות
- 📅 בדיקת זמינות וקביעת תורים
- 📲 שליחה אוטומטית של הזמנות ליומן

## דרישות מקדימות

- Python 3.8+
- חשבון Telegram Bot
- מפתח API של OpenRouter או Gemini

## התקנה

### 1. שכפול הפרויקט

```bash
cd /Users/yaronfeldboy/Documents/ragcosmetic
```

### 2. יצירת סביבה וירטואלית

```bash
python -m venv .venv
source .venv/bin/activate  # ב-Mac/Linux
```

### 3. התקנת תלויות

```bash
pip install -r requirements.txt
```

### 4. הגדרת משתני סביבה

העתק את קובץ התבנית:
```bash
cp .env.example .env
```

ערוך את `.env` והוסף את המפתחות שלך:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

> **⚠️ חשוב**: אל תשתף את קובץ `.env` או תעלה אותו ל-Git!

## הרצה

### הרצת הבוט

```bash
source .venv/bin/activate
python -m src.telegram.bot
```

### הרצת בדיקות

```bash
pytest tests/
```

## מבנה הפרויקט

```
ragcosmetic/
├── src/
│   ├── core/              # לוגיקה עסקית מרכזית
│   │   ├── agent.py       # AI agent עם Pydantic AI
│   │   ├── config.py      # ניהול הגדרות ומפתחות
│   │   ├── products.py    # קטלוג מוצרים וטיפולים
│   │   └── appointments.py  # ניהול תורים
│   ├── telegram/          # אינטגרציה עם Telegram
│   │   └── bot.py         # בוט Telegram
│   └── utils/             # עזרים כלליים
│       ├── date_parser.py    # פענוח תאריכים בעברית
│       ├── calendar_utils.py # יצירת קבצי ICS
│       └── image_manager.py  # ניהול תמונות מוצרים
├── tests/                 # בדיקות יחידה
├── data/                  # נתונים
│   ├── images/           # תמונות מוצרים
│   └── calendar_invites/ # קבצי ICS
├── docs/                 # תיעוד
├── .env                  # משתני סביבה (לא ב-Git!)
├── .env.example          # תבנית למשתני סביבה
├── .gitignore           # קבצים להתעלם מהם ב-Git
└── requirements.txt      # תלויות Python
```

## אבטחה

הפרויקט עוקב אחרי best practices של אבטחה:

- ✅ כל המפתחות והסודות נשמרים ב-`.env`
- ✅ קובץ `.env` לא מועלה ל-Git (מוגן ע"י `.gitignore`)
- ✅ ניהול מרכזי של הגדרות דרך `config.py`
- ✅ אין קוד קשיח (hardcoded) של מפתחות

## פיתוח

### הוספת מוצר חדש

ערוך את `src/core/products.py` והוסף מוצר חדש ל-`PRODUCTS`:

```python
Product(
    id="p4",
    name="שם המוצר",
    category="קטגוריה",
    description="תיאור",
    benefits="יתרונות",
    price=199.0,
    target_skin_type=["הכל"],
    target_concern=["בעיה"],
    image_path="data/images/products/product_image.png"
)
```

### עדכון הפרומפט

הפרומפט של ה-AI נמצא ב-`src/core/agent.py` במשתנה `SYSTEM_PROMPT`.

## רישיון

© 2025 היפות של רותי - כל הזכויות שמורות
