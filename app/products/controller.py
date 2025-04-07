import json
from typing import Dict, List, Optional
import requests
from flask import current_app
from datetime import datetime
from .models import Product


def get_all_products():
    """Get all products from MongoDB"""
    products = Product.objects.all()
    print(products)
    # Convert MongoDB documents to dictionaries and return as JSON
    
    return [product.to_dict() for product in products]

def create_product(product_data) :
    """Create a product in Shopify and sync to local DB"""
    print(product_data)
    try:
        # Validate required fields
        if not all(key in product_data for key in ['shopify_id', 'title', 'price', 'sku']):
            raise ValueError("Missing required fields: shopify_id, title, price, and sku are required")
        
        # Process variants if they exist
        variants = []
        if 'variants' in product_data and isinstance(product_data['variants'], list):
            variants = product_data['variants']
        
        # Create a new product instance
        product = Product(
            shopify_id=product_data['shopify_id'],
            title=product_data['title'],
            description=product_data.get('description', ''),
            price=float(product_data['price']),
            sku=product_data['sku'],
            image_url=product_data.get('image_url', ''),
            variants=variants,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Save to MongoDB
        product.save()
        
        return product
    
    except Exception as e:
        raise Exception(f"Failed to create product: {str(e)}")
    
