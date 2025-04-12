import json
from typing import Dict, List, Optional
import requests
from flask import current_app, request
from datetime import datetime
from .models import Product
from app.extensions import db
from app.events.models import Event
from .services import log_product_event
from app.utils.shopify import ShopifyAPI
from flask_jwt_extended import get_jwt_identity

# Initialize Shopify API
shopify_api = ShopifyAPI()

def get_all_products():
    """Get all products directly from Shopify"""
    try:
        user_id = get_jwt_identity()
        if not user_id:
            user_id = 'System'
        
        # Get products directly from Shopify
        products = shopify_api.get_products()
        
        # Log read event in PostgreSQL
        log_product_event('READ', 'ALL_PRODUCTS', str(user_id))
        
        return products
    
    except Exception as e:
        current_app.logger.error(f"Failed to get products: {str(e)}")
        raise Exception(f"Failed to get products: {str(e)}")

def create_product(product_data):
    """Create a product in Shopify and sync to local DB only if successful"""
    try:
        user_id = get_jwt_identity()
        if not user_id:
            user_id = 'System'

        # First create in Shopify
        shopify_product = shopify_api.create_product(product_data)
        if not shopify_product:
            raise Exception("Failed to create product in Shopify")
        
        # If Shopify creation successful, create in local DBs
        try:
            # Create product in our database
            print("hi there ther eht herfnefwefewf")
            print(shopify_product)
            product = Product(
                shopify_id=str(shopify_product['shopify_id']),
                title=shopify_product['title'],
                description=shopify_product['description'],
                price=shopify_product['price'],
                sku=shopify_product['sku'],
                image_url=product_data['image_url']
            )
            product.save()
            
            # Log event in PostgreSQL
            log_product_event('CREATE', shopify_product['shopify_id'], str(user_id))
            
            return product
            
        except Exception as db_error:
            # If local DB operations fail, log the error but don't rollback Shopify
            current_app.logger.error(f"Failed to sync with local DB: {str(db_error)}")
            return shopify_product
    
    except Exception as e:
        current_app.logger.error(f"Failed to create product: {str(e)}")
        raise Exception(f"Failed to create product: {str(e)}")

def get_product_by_id(product_id):
    """Get a product directly from Shopify"""
    try:
        user_id = get_jwt_identity()
        if not user_id:
            user_id = 'System'
        
        # Get product directly from Shopify
        product = shopify_api.get_product(product_id)
        
        if not product:
            raise Exception("Product not found in Shopify")
        
        # Log read event in PostgreSQL
        log_product_event('READ', product_id, str(user_id))
        
        return product
        
    except Exception as e:
        current_app.logger.error(f"Failed to get product: {str(e)}")
        raise Exception(f"Failed to get product: {str(e)}")

def update_product(product_id, product_data):
    """Update a product in Shopify and sync to local DB only if successful"""
    try:
        user_id = get_jwt_identity()
        if not user_id:
            user_id = 'System'

        # First update in Shopify
        shopify_product = shopify_api.update_product(product_id, product_data)
        
        if not shopify_product:
            raise Exception("Failed to update product in Shopify")
        
        # If Shopify update successful, update local DBs
        try:
            # Update in MongoDB
            product = Product.objects(shopify_id=product_id).first()
            if not product:
                product = Product(
                    shopify_id=str(shopify_product['shopify_id']),
                    title=shopify_product['title'],
                    description=shopify_product['description'],
                    price=shopify_product['price'],
                    sku=shopify_product['sku'],
                    image_url=product_data['image_url']
                )
            else:
                product.title = shopify_product['title']
                product.description = shopify_product['description']
                product.price =shopify_product['price']
                product.sku = shopify_product['sku']
                product.image_url = product_data['image_url']
            
            product.updated_at = datetime.utcnow()
            product.save()
            
            # Log event in PostgreSQL
            log_product_event('UPDATE', product_id, str(user_id))
            
            return product
            
        except Exception as db_error:
            # If local DB operations fail, log the error but don't rollback Shopify
            current_app.logger.error(f"Failed to sync with local DB: {str(db_error)}")
            return shopify_product
        
    except Exception as e:
        current_app.logger.error(f"Failed to update product: {str(e)}")
        raise Exception(f"Failed to update product: {str(e)}")

def delete_product(product_id):
    """Delete a product from Shopify and local DB only if successful"""
    try:
        user_id = get_jwt_identity()
        if not user_id:
            user_id = 'System'

        # First delete from Shopify
        result = shopify_api.delete_product(product_id)
        
        if not result or 'deletedProductId' not in result:
            raise Exception("Failed to delete product in Shopify")
        
        # If Shopify deletion successful, delete from local DBs
        try:
            # Delete from MongoDB
            product = Product.objects(shopify_id=product_id).first()
            if product:
                product.delete()
            
            # Log event in PostgreSQL
            log_product_event('DELETE', product_id, str(user_id))
            
            return True
            
        except Exception as db_error:
            # If local DB operations fail, log the error but don't rollback Shopify
            current_app.logger.error(f"Failed to sync with local DB: {str(db_error)}")
            return True
    
    except Exception as e:
        current_app.logger.error(f"Failed to delete product: {str(e)}")
        raise Exception(f"Failed to delete product: {str(e)}")
    
