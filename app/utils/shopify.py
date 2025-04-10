import os
import json
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ShopifyAPI:
    def __init__(self):
        self.shop_name = os.getenv('SHOPIFY_SHOP_NAME')
        self.access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')
        self.api_version = os.getenv('SHOPIFY_API_VERSION', '2024-01')
        
        if not self.shop_name:
            raise ValueError("SHOPIFY_SHOP_NAME environment variable is not set")
        if not self.access_token:
            raise ValueError("SHOPIFY_ACCESS_TOKEN environment variable is not set")
            
        self.base_url = f'https://{self.shop_name}.myshopify.com/admin/api/{self.api_version}/graphql.json'
        self.headers = {
            'X-Shopify-Access-Token': self.access_token,
            'Content-Type': 'application/json',
        }

    def _make_request(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Make a GraphQL request to Shopify"""
        try:
            payload = {
                'query': query,
                'variables': variables or {}
            }
            
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            
            # Check for HTTP errors
            if response.status_code == 401:
                raise Exception("Unauthorized: Invalid Shopify access token or shop name")
            elif response.status_code == 404:
                raise Exception(f"Shop not found: {self.shop_name}")
            elif response.status_code != 200:
                raise Exception(f"Shopify API error: {response.status_code} - {response.text}")
            
            data = response.json()
            
            # Check for GraphQL errors
            if 'errors' in data:
                error_message = data['errors'][0]['message']
                raise Exception(f"Shopify GraphQL error: {error_message}")
                
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to Shopify: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid response from Shopify: {str(e)}")
        except Exception as e:
            raise Exception(f"Shopify API error: {str(e)}")

    def get_products(self, first: int = 100) -> List[Dict]:
        """Fetch products from Shopify"""
        query = """
        query getProducts($first: Int!) {
            products(first: $first) {
                edges {
                    node {
                        id
                        title
                        descriptionHtml
                        variants(first: 1) {
                            edges {
                                node {
                                    price
                                    inventoryItem {
                                        sku
                                    }
                                }
                            }
                        }
                        images(first: 1) {
                            edges {
                                node {
                                    url
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        
        variables = {"first": first}
        result = self._make_request(query, variables)
        
        # Format the response to match the desired structure
        products = []
        for edge in result['data']['products']['edges']:
            product = edge['node']
            print("Product:", product)  # Debug print
            print("Variants:", product['variants'])  # Debug print
            
            # Extract numeric ID from the GID
            product_id = product['id'].split('/')[-1]
            
            # Get variant data
            variant = product['variants']['edges'][0]['node'] if product['variants']['edges'] else None
            print("Variant:", variant)  # Debug print
            price = float(variant['price']) if variant else 0.0
            sku = variant['inventoryItem']['sku'] if variant and variant.get('inventoryItem') else ''
            
            # Get image URL
            image = product['images']['edges'][0]['node']['url'] if product['images']['edges'] else ''
            
            formatted_product = {
                'shopify_id': product_id,
                'title': product['title'],
                'description': product['descriptionHtml'],
                'price': price,
                'sku': sku,
                'image_url': image
            }
            products.append(formatted_product)
            
        return products

    def create_product(self, product_data: Dict) -> Dict:
        """Create a new product in Shopify with variants and images"""
        # Step 1: Create the base product
        create_product_mutation = """
        mutation productCreate($input: ProductInput!) {
            productCreate(input: $input) {
                product {
                    id
                    title
                    descriptionHtml
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
        
        product_variables = {
            "input": {
                "title": product_data["title"],
                "descriptionHtml": product_data.get("description", "")
            }
        }
        
        product_result = self._make_request(create_product_mutation, product_variables)
        
        if product_result.get("errors"):
            raise Exception(f"Shopify API Error: {product_result['errors'][0]['message']}")
            
        product_id = product_result["data"]["productCreate"]["product"]["id"]
        
        # Step 2: Create or update variant
        create_variant_mutation = """
        mutation productVariantUpdate($input: ProductVariantInput!) {
            productVariantUpdate(input: $input) {
                productVariant {
                    id
                    price
                    inventoryItem {
                        sku
                    }
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
        
        print("Creating variant with data:", product_data)  # Debug print
        
        # First, get the existing variant ID
        get_variant_query = """
        query getProductVariants($productId: ID!) {
            product(id: $productId) {
                variants(first: 1) {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
        }
        """
        
        variant_query_variables = {
            "productId": product_id
        }
        
        variant_query_result = self._make_request(get_variant_query, variant_query_variables)
        variant_id = variant_query_result['data']['product']['variants']['edges'][0]['node']['id']
        
        variant_variables = {
            "input": {
                "id": variant_id,
                "price": str(product_data["price"]),
                "inventoryItem": {
                    "sku": product_data.get("sku", "")
                }
            }
        }
        
        print("Variant variables:", variant_variables)  # Debug print
        
        variant_result = self._make_request(create_variant_mutation, variant_variables)
        
        print("Variant creation result:", variant_result)  # Debug print
        
        if variant_result.get("errors"):
            raise Exception(f"Shopify API Error: {variant_result['errors'][0]['message']}")
        
        # Step 3: Add image if provided
        if product_data.get("image_url"):
            create_media_mutation = """
            mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
                productCreateMedia(productId: $productId, media: $media) {
                    media {
                        ... on MediaImage {
                            id
                            image {
                                url
                            }
                        }
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
            """
            
            media_variables = {
                "productId": product_id,
                "media": [{
                    "mediaContentType": "IMAGE",
                    "originalSource": product_data["image_url"]
                }]
            }
            
            media_result = self._make_request(create_media_mutation, media_variables)
            
            if media_result.get("errors"):
                raise Exception(f"Shopify API Error: {media_result['errors'][0]['message']}")
        
        # Return the complete product data
        return self.get_product(product_id)

    def update_product(self, product_id: str, product_data: Dict) -> Dict:
        """Update a product in Shopify"""
        # Step 1: Update the base product
        update_product_mutation = """
        mutation productUpdate($input: ProductInput!) {
            productUpdate(input: $input) {
                product {
                    id
                    title
                    descriptionHtml
                    variants(first: 1) {
                        edges {
                            node {
                                price
                                inventoryItem {
                                    sku
                                }
                            }
                        }
                    }
                    images(first: 1) {
                        edges {
                            node {
                                url
                            }
                        }
                    }
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
        
        # Convert numeric ID to full GID format if needed
        if not product_id.startswith("gid://"):
            product_id = f"gid://shopify/Product/{product_id}"
        
        product_variables = {
            "input": {
                "id": product_id,
                "title": product_data["title"],
                "descriptionHtml": product_data.get("description", "")
            }
        }
        
        product_result = self._make_request(update_product_mutation, product_variables)
        
        if product_result.get("errors"):
            raise Exception(f"Shopify API Error: {product_result['errors'][0]['message']}")
        
        # Step 2: Update variant
        update_variant_mutation = """
        mutation productVariantUpdate($input: ProductVariantInput!) {
            productVariantUpdate(input: $input) {
                productVariant {
                    id
                    price
                    inventoryItem {
                        sku
                    }
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
        
        # Get the existing variant ID
        get_variant_query = """
        query getProductVariants($productId: ID!) {
            product(id: $productId) {
                variants(first: 1) {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
        }
        """
        
        variant_query_variables = {
            "productId": product_id
        }
        
        variant_query_result = self._make_request(get_variant_query, variant_query_variables)
        variant_id = variant_query_result['data']['product']['variants']['edges'][0]['node']['id']
        
        variant_variables = {
            "input": {
                "id": variant_id,
                "price": str(product_data["price"]),
                "inventoryItem": {
                    "sku": product_data.get("sku", "")
                }
            }
        }
        
        variant_result = self._make_request(update_variant_mutation, variant_variables)
        
        if variant_result.get("errors"):
            raise Exception(f"Shopify API Error: {variant_result['errors'][0]['message']}")
        
        # Step 3: Update image if provided
        if product_data.get("image_url"):
            update_media_mutation = """
            mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
                productCreateMedia(productId: $productId, media: $media) {
                    media {
                        ... on MediaImage {
                            id
                            image {
                                url
                            }
                        }
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
            """
            
            media_variables = {
                "productId": product_id,
                "media": [{
                    "mediaContentType": "IMAGE",
                    "originalSource": product_data["image_url"]
                }]
            }
            
            media_result = self._make_request(update_media_mutation, media_variables)
            
            if media_result.get("errors"):
                raise Exception(f"Shopify API Error: {media_result['errors'][0]['message']}")
        
        # Return the complete updated product data
        return self.get_product(product_id)

    def delete_product(self, product_id: str) -> Dict:
        """Delete a product from Shopify"""
        mutation = """
        mutation productDelete($input: ProductDeleteInput!) {
            productDelete(input: $input) {
                deletedProductId
                userErrors {
                    field
                    message
                }
            }
        }
        """
        
        # Convert numeric ID to full GID format
        full_product_id = f"gid://shopify/Product/{product_id}"
        
        variables = {
            "input": {
                "id": full_product_id
            }
        }
        
        result = self._make_request(mutation, variables)
        
        if result.get("errors"):
            raise Exception(f"Shopify API Error: {result['errors'][0]['message']}")
        
        return result["data"]["productDelete"]

    def get_product(self, product_id: str) -> Dict:
        """Get a single product by ID"""
        query = """
        query GetProduct($id: ID!) {
            product(id: $id) {
                id
                title
                descriptionHtml
                variants(first: 1) {
                    edges {
                        node {
                            price
                            inventoryItem {
                                sku
                            }
                        }
                    }
                }
                images(first: 1) {
                    edges {
                        node {
                            url
                        }
                    }
                }
            }
        }
        """
        
        # Convert numeric ID to full GID format if needed
        if not product_id.startswith("gid://"):
            product_id = f"gid://shopify/Product/{product_id}"
        
        variables = {"id": product_id}
        result = self._make_request(query, variables)
        
        if result.get("errors"):
            raise Exception(f"Shopify API Error: {result['errors'][0]['message']}")
        
        product = result["data"]["product"]
        
        # Extract numeric ID from the GID
        numeric_id = product['id'].split('/')[-1]
        
        # Get variant data
        variant = product['variants']['edges'][0]['node'] if product['variants']['edges'] else None
        price = float(variant['price']) if variant else 0.0
        sku = variant['inventoryItem']['sku'] if variant and variant.get('inventoryItem') else ''
        
        # Get image URL
        image = product['images']['edges'][0]['node']['url'] if product['images']['edges'] else ''
        
        formatted_product = {
            'shopify_id': numeric_id,
            'title': product['title'],
            'description': product['descriptionHtml'],
            'price': price,
            'sku': sku,
            'image_url': image
        }
        
        print("Formatted product:", formatted_product)  # Debug print
        return formatted_product
