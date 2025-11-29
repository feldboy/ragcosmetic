import os
import sys
import asyncio
import re
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.products import PRODUCTS
from src.utils.image_manager import get_product_image

def test_product_images():
    print("Checking product images...")
    missing_images = []
    for product in PRODUCTS:
        print(f"Checking {product.name}...")
        image_path = get_product_image(product.name)
        if image_path:
            if os.path.exists(image_path):
                print(f"  [OK] Found image: {image_path}")
            else:
                print(f"  [FAIL] Path returned but file missing: {image_path}")
                missing_images.append(product.name)
        else:
            print(f"  [FAIL] No image path returned for {product.name}")
            missing_images.append(product.name)
    
    if missing_images:
        print(f"\nFAILED: Missing images for: {', '.join(missing_images)}")
    else:
        print("\nSUCCESS: All products have valid images.")

async def test_response_parsing():
    print("\nTesting response parsing logic...")
    
    # Simulate the logic from bot.py
    test_cases = [
        ("Here is the image IMAGE:/path/to/image.png", ["/path/to/image.png"]),
        ("Check this out IMAGE:/path/to/image.png.", ["/path/to/image.png"]),
        ("IMAGE:/path/to/image.png is the file", ["/path/to/image.png"]),
        ("Multiple images IMAGE:/path/1.png and IMAGE:/path/2.jpg", ["/path/1.png", "/path/2.jpg"]),
        ("With quotes 'IMAGE:/path/to/image.png'", ["/path/to/image.png"]),
    ]
    
    for text, expected in test_cases:
        print(f"Testing text: '{text}'")
        image_pattern = r'IMAGE:([^\s]+)'
        images = re.findall(image_pattern, text)
        
        cleaned_images = [img.rstrip('.,;!?)]}"\'') for img in images]
        
        if cleaned_images == expected:
            print(f"  [OK] Parsed correctly: {cleaned_images}")
        else:
            print(f"  [FAIL] Expected {expected}, got {cleaned_images}")

if __name__ == "__main__":
    test_product_images()
    asyncio.run(test_response_parsing())
