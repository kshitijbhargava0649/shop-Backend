import os
from app import create_app
from flask_restx import Api

app = create_app()

# from app.auth.routes import api as auth_apis
# from app.events.routes import api as events_apis
from app.products.routes import api as products_apis


api = Api(app,version='1.0',title='Dookan App',description='API for Shopify')
# api.add_namespace(auth_apis)
# api.add_namespace(events_apis)
api.add_namespace(products_apis)

if __name__ == '__main__':
    app.run(debug=True)
