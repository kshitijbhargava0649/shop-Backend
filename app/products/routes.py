import traceback
from flask import request, jsonify
from marshmallow import ValidationError
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.products.controller import create_product, get_all_products, get_product_by_id, update_product, delete_product
from app.products.input_validation import ProductSchema, ProductUpdateSchema
from app.utils.event_logger import log_event


api = Namespace('products', description='Product related endpoints')

@api.route('/')
class ProductList(Resource):
    # @jwt_required()   
    @jwt_required()
    def get(self):
        """Get all products with filtering and pagination"""
        try:
            products = get_all_products()
            return products
        except ValidationError as e:
            return {'error': e.messages}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    # @jwt_required()
    @jwt_required()
    def post(self):
        """Create a new product"""
        try:

            data = request.json
            product = create_product(data)
            print(product)
            schema = ProductSchema()
            return schema.dump(product), 201
        except ValidationError as e:
            return {'error': e.messages}, 400
        except Exception as e:
            print(traceback.format_exc())
            return {'error': str(e)}, 500

@api.route('/<string:product_id>')
class ProductResource(Resource):
    @jwt_required()
    def get(self, product_id):
        """Get a specific product by ID"""
        try:
            product = get_product_by_id(product_id)
            print(product_id)
            if not product:
                return {'error': 'Product not found'}, 404
            schema = ProductSchema()
            return schema.dump(product), 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    def put(self, product_id):
        """Update a product"""
        try:
            # Get user ID from headers
            user_id = request.headers.get('User-ID', 'system')
            
            # Get product data from request
            data = request.json
            
            # Update the product
            updated_product = update_product(product_id, data)
            
            if not updated_product:
                return {'error': 'Product not found'}, 404
                
            # Return the updated product
            schema = ProductSchema()
            return schema.dump(updated_product), 200
        except ValidationError as e:
            return {'error': e.messages}, 400
        except Exception as e:
            print(traceback.format_exc())
            return {'error': str(e)}, 500

    @jwt_required()
    def delete(self, product_id):
        """Delete a product"""
        try:
            # Get user ID from headers
            user_id = request.headers.get('User-ID', 'system')
            
            # Delete the product
            result = delete_product(product_id)
            
            if not result:
                return {'error': 'Product not found'}, 404
                
            return '', 204
        except Exception as e:
            return {'error': str(e)}, 500

