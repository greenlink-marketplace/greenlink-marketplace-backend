from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError

class NonEmptySearchFilter(SearchFilter):
    def get_search_terms(self, request):
        search_terms = super().get_search_terms(request)
        if not search_terms:
            raise ValidationError({"search": "This field is required."})
        return search_terms
