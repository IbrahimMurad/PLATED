""" Subject model
"""

from subjects.models.base import MaterialBaseModel


class Subject(MaterialBaseModel):
    """ subjects table """
    order_in_syllabus = None
    number = None
