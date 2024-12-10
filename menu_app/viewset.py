from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser




class CustomViewSet(ModelViewSet):
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    lookup_field = "name"


    def get_filtered_queryset(self, model, filter_field, lookup_field):
        queryset = model.objects.all()
        name = self.kwargs.get(lookup_field)
        if name:
            filter_param = f"{filter_field}__name"
            queryset = queryset.filter(**{filter_param: name, 'restaurant__is_active': True})
        return queryset