import traceback
from flask import request, jsonify
from marshmallow import ValidationError
from flask_restx import Namespace, Resource
from app.products.controller import create_product, get_all_products
from app.products.input_validation import ProductSchema, ProductUpdateSchema

api = Namespace('products', description='Product related endpoints')



@api.route('/')
class ProductList(Resource):

    def get(self):
        """Get all products with filtering and pagination"""
        try:
            products = get_all_products()
            return products
        except ValidationError as e:
            return {'error': e.messages}, 400
        except Exception as e:
            return {'error': str(e)}, 500


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

# @api.route('/<string:product_id>')
# class ProductResource(Resource):
    # @jwt_required()
    # def get(self, product_id):
    #     """Get a specific product by ID"""
    #     try:
    #         product = product_service.get_product(product_id)
    #         if not product:
    #             return {'error': 'Product not found'}, 404
    #         return product_schema.dump(product), 200
    #     except Exception as e:
    #         return {'error': str(e)}, 500

    # @jwt_required()
    # def put(self, product_id):
    #     """Update a product"""
    #     try:
    #         data = product_update_schema.load(request.json)
    #         product = product_service.update_product(product_id, data)
    #         EventLogger.log_event('UPDATE', 'product', product.id)
    #         return product_schema.dump(product), 200
    #     except ValidationError as e:
    #         return {'error': e.messages}, 400
    #     except Exception as e:
    #         return {'error': str(e)}, 500

    # @jwt_required()
    # def delete(self, product_id):
    #     """Delete a product"""
    #     try:
    #         product_service.delete_product(product_id)
    #         EventLogger.log_event('DELETE', 'product', product_id)
    #         return '', 204
    #     except Exception as e:
    #         return {'error': str(e)}, 500

# @api.route('/bulk')
# class ProductBulkOperations(Resource):
    # @jwt_required()
    # def post(self):
    #     """Bulk create products"""
    #     try:
    #         data = product_bulk_create_schema.load(request.json)
    #         products = product_service.bulk_create_products(data['products'])
    #         for product in products:
    #             EventLogger.log_event('CREATE', 'product', product.id)
    #         return products_schema.dump(products), 201
    #     except ValidationError as e:
    #         return {'error': e.messages}, 400
    #     except Exception as e:
    #         return {'error': str(e)}, 500

    # @jwt_required()
    # def put(self):
    #     """Bulk update products"""
    #     try:
    #         data = product_bulk_update_schema.load(request.json)
    #         products = product_service.bulk_update_products(data['products'])
    #         for product in products:
    #             EventLogger.log_event('UPDATE', 'product', product.id)
    #         return products_schema.dump(products), 200
    #     except ValidationError as e:
    #         return {'error': e.messages}, 400
    #     except Exception as e:
    #         return {'error': str(e)}, 500 