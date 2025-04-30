from django.core.management.base import BaseCommand
from Base_App.models import Items  # Replace 'Base_App' with your actual app name
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from ...documents import Product_Document

es = Elasticsearch(hosts=["http://localhost:9200"])

class Command(BaseCommand):
    help = 'Indexes existing data from the database into Elasticsearch'

    def handle(self, *args, **kwargs):
        products = Items.objects.all()
        actions = []

        for product in products:
            try:
                action = {
                    "_op_type": "index",
                    "_index": "products",
                    "_id": product.id,
                    "_source": {
                        "name": product.Item_name,
                        "description": product.description,
                        "price": product.price,
                        "category": product.Category.category_name if product.Category else "Unknown",
                        "Image": product.Image.url if product.Image else "",
                        "suggest": {
                            "input": [product.Item_name] + ([product.description] if isinstance(product.description, str) else []),  
                            "weight": 1  # Make sure this is always an integer
                        }
                    }
                }
                actions.append(action)
            except Exception as e:
                print(f"Error processing product {product.id}: {str(e)}")

        # Debugging: Print sample payload
        if actions:
            import json
            print(json.dumps(actions[0], indent=4))

        # Bulk index data
        try:
            bulk(es, actions)
            self.stdout.write(self.style.SUCCESS('Successfully indexed data into Elasticsearch.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error during indexing: {str(e)}"))
