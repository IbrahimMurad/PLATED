from .models import CURRENT_SEMESTER


def current_semester(request):
    return {'semester': CURRENT_SEMESTER}
