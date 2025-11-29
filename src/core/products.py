from pydantic import BaseModel, Field
from typing import List, Optional

class Product(BaseModel):
    id: str
    name: str
    category: str
    description: str
    benefits: str
    price: float
    target_skin_type: List[str] # למשל: ["יבש", "שמן", "מעורב", "הכל"]
    target_concern: List[str] # למשל: ["אקנה", "אנטי אייג'ינג", "פיגמנטציה", "יובש"]
    image_path: Optional[str] = None # נתיב לתמונת מוצר
    duration_hours: Optional[float] = None # משך הטיפול בשעות

# נתוני דוגמה - טיפולים וקוסמטיקה
PRODUCTS = [
    Product(
        id="t1",
        name="לק ג'ל קלאסי",
        category="מניקור",
        description="לק ג'ל מקצועי עמיד עד 3 שבועות.",
        benefits="ציפורניים מושלמות ועמידות, צבע אחיד ומבריק שמחזיק שבועות.",
        price=120.0,
        target_skin_type=["הכל"],
        target_concern=["עיצוב ציפורניים"],
        image_path="data/images/products/gel_manicure.png",
        duration_hours=2.0
    ),
    Product(
        id="t2",
        name="פדיקור ספא מפנק",
        category="פדיקור",
        description="טיפול פדיקור מלא עם פילינג, מסכה ועיסוי רגליים.",
        benefits="רגליים רכות וחלקות, ציפורניים מעוצבות ומטופחות, הרגשת רעננות.",
        price=150.0,
        target_skin_type=["הכל"],
        target_concern=["טיפוח רגליים"],
        image_path="data/images/products/spa_pedicure.png",
        duration_hours=1.5
    ),
    Product(
        id="t3",
        name="טיפול פנים אנטי אייג'ינג",
        category="טיפולי פנים",
        description="טיפול פנים מתקדם עם סרום רטינול ומסכת קולגן.",
        benefits="החלקת קמטים וקווי הבעה, שיפור מרקם העור והחזרת גמישות.",
        price=350.0,
        target_skin_type=["יבש", "נורמלי"],
        target_concern=["אנטי אייג'ינג", "קמטים"],
        image_path="data/images/products/anti_aging_facial.png",
        duration_hours=1.5
    ),
    Product(
        id="t4",
        name="טיפול אקנה ופצעונים",
        category="טיפולי פנים",
        description="טיפול ממוקד לטיפול באקנה ופצעונים עם חומרים מרגיעים.",
        benefits="ניקוי עמוק של הנקבוביות, צמצום דלקות והפחתת אדמומיות.",
        price=280.0,
        target_skin_type=["שמן", "מעורב"],
        target_concern=["אקנה", "פצעונים"],
        image_path="data/images/products/acne_treatment.png",
        duration_hours=1.0
    ),
    Product(
        id="t5",
        name="טיפול הבהרה ואיחוד גוון",
        category="טיפולי פנים",
        description="טיפול מתקדם עם ויטמין C לאיחוד גוון והבהרת כתמים.",
        benefits="דעיכת כתמי פיגמנטציה, איחוד גוון העור וקבלת זוהר טבעי.",
        price=320.0,
        target_skin_type=["הכל"],
        target_concern=["פיגמנטציה", "כתמים"],
        image_path="data/images/products/brightening_facial.png",
        duration_hours=1.5
    ),
    Product(
        id="t6",
        name="עיצוב גבות בשעווה",
        category="עיצוב גבות",
        description="עיצוב מקצועי של הגבות בשעווה לקו מושלם.",
        benefits="גבות מעוצבות ומדויקות, מראה מסודר ונקי.",
        price=60.0,
        target_skin_type=["הכל"],
        target_concern=["עיצוב גבות"],
        image_path="data/images/products/eyebrow_wax.png",
        duration_hours=0.5
    ),
    Product(
        id="t7",
        name="מזותרפיה לפנים",
        category="טיפולי מזותרפיה",
        description="זריקות ויטמינים וחומצה היאלורונית לחידוש העור.",
        benefits="לחות עמוקה, מילוי קמטים דקים ושיפור מרקם העור.",
        price=450.0,
        target_skin_type=["הכל"],
        target_concern=["אנטי אייג'ינג", "יובש"],
        image_path="data/images/products/mesotherapy.png",
        duration_hours=1.0
    ),
    Product(
        id="p1",
        name="סרום היאלורון מרוכז",
        category="מוצרי טיפוח",
        description="סרום קל עם חומצה היאלורונית מרוכזת.",
        benefits="לחות עמוקה ומילוי העור, מראה נפוח וזוהר.",
        price=180.0,
        target_skin_type=["יבש", "מעורב", "הכל"],
        target_concern=["יובש", "אנטי אייג'ינג"],
        image_path="data/images/products/hyaluron_serum.png"
    ),
    Product(
        id="p2",
        name="קרם לילה מזין",
        category="מוצרי טיפוח",
        description="קרם עשיר עם ויטמינים ושמנים טבעיים.",
        benefits="הזנה עמוקה במהלך הלילה, החלקת קמטים ושיקום העור.",
        price=220.0,
        target_skin_type=["יבש", "נורמלי"],
        target_concern=["אנטי אייג'ינג", "יובש"],
        image_path="data/images/products/night_cream.png"
    ),
    Product(
        id="p3",
        name="קרם הבהרה עם ויטמין C",
        category="מוצרי טיפוח",
        description="קרם מבהיר עוצמתי עם ויטמין C ונגד כתמים.",
        benefits="דעיכת כתמים, איחוד גוון ומראה זוהר.",
        price=250.0,
        target_skin_type=["הכל"],
        target_concern=["פיגמנטציה", "כתמים"],
        image_path="data/images/products/vitamin_c_cream.png"
    )
]

def search_products(query: str) -> List[Product]:
    """
    פונקציית חיפוש פשוטה למציאת מוצרים וטיפולים לפי שאילתא.
    מחפשת בשם, קטגוריה, תיאור או דאגות.
    """
    query = query.lower()
    results = []
    for product in PRODUCTS:
        if (query in product.name.lower() or 
            query in product.category.lower() or 
            query in product.benefits.lower() or
            query in product.description.lower() or
            any(query in c.lower() for c in product.target_concern)):
            results.append(product)
    return results

def get_all_products() -> List[Product]:
    return PRODUCTS
