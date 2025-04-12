import unittest
from app.utils.shopify import ShopifyAPI

class TestShopifyAPI(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.shopify_api = ShopifyAPI()

    def test_get_products(self):
        """Test fetching products from Shopify"""
        try:
            # Test with default limit (10 products)
            result = self.shopify_api.get_products()
            
            # Verify the response structure
            self.assertIn('products', result)
            self.assertIn('edges', result['products'])
            
            # Print the number of products found
            products = result['products']['edges']
            print(f"\nNumber of products found: {len(products)}")
            
            # If there are products, verify their structure and print details
            if products:
                first_product = products[0]['node']
                self.assertIn('id', first_product)
                self.assertIn('title', first_product)
                self.assertIn('priceRangeV2', first_product)
                
                print("\nFirst product details:")
                print(f"Title: {first_product['title']}")
                print(f"ID: {first_product['id']}")
                
                # Print price if available
                price_range = first_product.get('priceRangeV2', {})
                if price_range and price_range.get('minVariantPrice'):
                    price = price_range['minVariantPrice']
                    print(f"Price: {price['amount']} {price['currencyCode']}")
                
                # Print image URL if available
                images = first_product.get('images', {}).get('edges', [])
                if images:
                    image_url = images[0]['node']['url']
                    print(f"Image URL: {image_url}")

        except Exception as e:
            self.fail(f"Failed to fetch products: {str(e)}")

if __name__ == '__main__':
    unittest.main() 