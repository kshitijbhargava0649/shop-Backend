import json
from typing import Dict, List, Optional
import requests
from flask import current_app, request
from datetime import datetime
from .models import Product
from app.extensions import postgres_db
from app.events.models import Event
from .services import log_product_event

# servies.py

def get_all_products():
    """Get all products from MongoDB"""
    # // shopify thing
    products = Product.objects.all()
    print(products)
    return [product.to_dict() for product in products]

def create_product(product_data) :
    """Create a product in Shopify and sync to local DB"""
    print(product_data)
    try:
        user_id = request.headers.get('User-ID', 'System')

        if not all(key in product_data for key in ['shopify_id', 'title', 'price', 'sku']):
            raise ValueError("Missing required fields: shopify_id, title, price, and sku are required")

        # Create a new product instance
        product = Product(
            shopify_id=product_data['shopify_id'],
            title=product_data['title'],
            description=product_data.get('description', ''),
            price=float(product_data['price']),
            sku=product_data['sku'],
            image_url=product_data.get('image_url', ''),
        )
        
        # Save to MongoDB
        product.save()
        
        log_product_event('CREATE', product.shopify_id, user_id)
        return product
    
    except Exception as e:
        raise Exception(f"Failed to create product: {str(e)}")

def get_product_by_id(product_id):
    """Get a product by ID"""
    try:
        user_id = request.headers.get('User-ID', 'System')
        product = Product.objects(shopify_id=product_id).first()
        log_product_event('READ', product.shopify_id, user_id)
        return product
    except Exception as e:
        raise Exception(f"Failed to get product: {str(e)}")

def update_product(product_id, product_data):
    """Update a product"""
    try:
        # Find the product
        product = Product.objects(shopify_id=product_id).first()
        if not product:
            return None
        
        # Update fields if they exist in the request
        if 'title' in product_data:
            product.title = product_data['title']
        if 'description' in product_data:
            product.description = product_data['description']
        if 'price' in product_data:
            product.price = float(product_data['price'])
        if 'sku' in product_data:
            product.sku = product_data['sku']
        if 'image_url' in product_data:
            product.image_url = product_data['image_url']
        if 'variants' in product_data and isinstance(product_data['variants'], list):
            product.variants = product_data['variants']
        
        # Update the timestamp
        product.updated_at = datetime.utcnow()
        
        # Save the changes
        product.save()
        
        user_id = request.headers.get('User-ID', 'System')
        log_product_event('UPDATE', product.shopify_id, user_id)
        return product
    except Exception as e:
        raise Exception(f"Failed to update product: {str(e)}")

def delete_product(product_id):
    """Delete a product"""
    try:
        product = Product.objects(shopify_id=product_id).first()
        if not product:
            return False
        
        product.delete()
        user_id = request.headers.get('User-ID', 'System')
        log_product_event('DELETE', product.shopify_id, user_id)
        return True
    except Exception as e:
        raise Exception(f"Failed to delete product: {str(e)}")
    
