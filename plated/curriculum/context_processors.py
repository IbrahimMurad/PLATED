from django.utils import timezone
from .models import Semester


CURRENT_SEMESTER = Semester.objects.filter(
    starting_date__lte=timezone.now(),
    ending_date__gte=timezone.now()
    ).first()


def current_semester(request):
    """ sets the current semester in the context """
    return {'semester': CURRENT_SEMESTER}
