from import_export import resources
from app.models import Rating

class RatingResource(resources.ModelResource):
    class Meta:
        model = Rating