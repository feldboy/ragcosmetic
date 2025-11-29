import os
from typing import Optional, List
from products import PRODUCTS, Product

def get_product_image(product_name: str) -> Optional[str]:
    """
    Get the image path for a specific product by name.
    
    Args:
        product_name: Name of the product (case-insensitive search)
        
    Returns:
        Absolute path to the product image, or None if not found
    """
    product_name_lower = product_name.lower()
    
    for product in PRODUCTS:
        if product_name_lower in product.name.lower():
            if product.image_path and os.path.exists(product.image_path):
                # Return absolute path
                return os.path.abspath(product.image_path)
            return None
    
    return None

def get_product_image_by_id(product_id: str) -> Optional[str]:
    """
    Get the image path for a specific product by ID.
    
    Args:
        product_id: Product ID
        
    Returns:
        Absolute path to the product image, or None if not found
    """
    for product in PRODUCTS:
        if product.id == product_id:
            if product.image_path and os.path.exists(product.image_path):
                return os.path.abspath(product.image_path)
            return None
    
    return None

def get_category_images(category: str) -> List[tuple[str, str]]:
    """
    Get all product images for a specific category.
    
    Args:
        category: Product category (e.g., "Serum", "Cleanser")
        
    Returns:
        List of tuples (product_name, image_path)
    """
    results = []
    category_lower = category.lower()
    
    for product in PRODUCTS:
        if category_lower in product.category.lower():
            if product.image_path and os.path.exists(product.image_path):
                results.append((product.name, os.path.abspath(product.image_path)))
    
    return results

def validate_image_exists(path: str) -> bool:
    """
    Check if an image file exists at the given path.
    
    Args:
        path: Path to the image file
        
    Returns:
        True if the file exists, False otherwise
    """
    return os.path.isfile(path) and os.path.exists(path)

def get_all_product_images() -> List[tuple[str, str]]:
    """
    Get all available product images.
    
    Returns:
        List of tuples (product_name, image_path)
    """
    results = []
    
    for product in PRODUCTS:
        if product.image_path and os.path.exists(product.image_path):
            results.append((product.name, os.path.abspath(product.image_path)))
    
    return results
