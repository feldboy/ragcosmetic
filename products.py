from pydantic import BaseModel, Field
from typing import List, Optional

class Product(BaseModel):
    id: str
    name: str
    category: str
    description: str
    benefits: str
    price: float
    target_skin_type: List[str] # e.g., ["Dry", "Oily", "Combination", "All"]
    target_concern: List[str] # e.g., ["Acne", "Aging", "Pigmentation", "Dehydration"]
    image_path: Optional[str] = None # Path to product image

# Mock Data
PRODUCTS = [
    Product(
        id="p1",
        name="Hydra-Boost Serum",
        category="Serum",
        description="A lightweight serum packed with hyaluronic acid.",
        benefits="Provides deep hydration and plumps the skin, eliminating dryness.",
        price=45.0,
        target_skin_type=["Dry", "Combination", "All"],
        target_concern=["Dehydration", "Aging"],
        image_path="images/products/serum.png"
    ),
    Product(
        id="p2",
        name="Clearify Gel Cleanser",
        category="Cleanser",
        description="A gentle foaming cleanser with salicylic acid.",
        benefits="Unclogs pores and reduces excess oil without stripping the skin.",
        price=25.0,
        target_skin_type=["Oily", "Combination"],
        target_concern=["Acne", "Blackheads"],
        image_path="images/products/cleanser.png"
    ),
    Product(
        id="p3",
        name="Anti-Age Gold Cream",
        category="Moisturizer",
        description="Rich cream with active retinol and peptides.",
        benefits="Smoothes fine lines and improves skin texture for a youthful look.",
        price=85.0,
        target_skin_type=["Dry", "Normal"],
        target_concern=["Aging", "Wrinkles"],
        image_path="images/products/face_cream.png"
    ),
    Product(
        id="p4",
        name="SunGuard SPF 50",
        category="Sunscreen",
        description="Broad-spectrum protection with a matte finish.",
        benefits="Protects against UV damage and prevents future pigmentation.",
        price=30.0,
        target_skin_type=["All"],
        target_concern=["Pigmentation", "Aging"]
    ),
    Product(
        id="p5",
        name="Brightening Vitamin C Drops",
        category="Serum",
        description="Potent Vitamin C serum.",
        benefits="Fades dark spots and evens out skin tone for a radiant glow.",
        price=55.0,
        target_skin_type=["All"],
        target_concern=["Pigmentation", "Dullness"],
        image_path="images/products/vitamin_c.png"
    )
]

def search_products(query: str) -> List[Product]:
    """
    Simple search function to find products based on a query string.
    Matches against name, category, benefits, or concerns.
    """
    query = query.lower()
    results = []
    for product in PRODUCTS:
        if (query in product.name.lower() or 
            query in product.category.lower() or 
            query in product.benefits.lower() or
            any(query in c.lower() for c in product.target_concern)):
            results.append(product)
    return results

def get_all_products() -> List[Product]:
    return PRODUCTS
