from django.conf import settings

def pageNums(request):
    return {"HAYSTACK_SEARCH_RESULTS_PER_PAGE": settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE}
