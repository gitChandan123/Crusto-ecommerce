from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Items

@registry.register_document
class Product_Document(Document):
    
    class Index:
        name = 'items'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    # The Django class must be indented correctly
    class Django:
        model = Items
        fields = [
            'Item_name',
            'description', # Ensure this matches the field name in your model
            'price',
            'Image',
        ]
