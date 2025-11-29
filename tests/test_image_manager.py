#!/usr/bin/env python3
"""
Quick test to verify image manager and product updates work correctly.
"""
import os
import sys

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.image_manager import get_product_image, get_all_product_images
from products import PRODUCTS

def test_image_manager():
    print("🧪 Testing Image Manager...")
    print("-" * 50)
    
    # Test 1: Check that all products have images
    print("\n1. Checking product image assignments:")
    for product in PRODUCTS:
        status = "✅" if product.image_path else "❌"
        print(f"   {status} {product.name}: {product.image_path}")
    
    # Test 2: Test get_product_image function
    print("\n2. Testing get_product_image():")
    test_products = ["Hydra-Boost", "Vitamin C", "Cleanser"]
    for product_name in test_products:
        image_path = get_product_image(product_name)
        if image_path and os.path.exists(image_path):
            print(f"   ✅ {product_name}: Found at {image_path}")
        else:
            print(f"   ❌ {product_name}: Not found or doesn't exist")
    
    # Test 3: Get all images
    print("\n3. Testing get_all_product_images():")
    all_images = get_all_product_images()
    print(f"   Found {len(all_images)} product images total")
    for name, path in all_images:
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"   {exists} {name}")
    
    print("\n" + "=" * 50)
    print("✅ Image Manager Tests Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_image_manager()
