from typing import Any
from django import forms
from .models import Exam


class ExamForm(forms.Form):
    class Meta:
        model = Exam
        fields = []
    def __init__(self, exam=None, *args, **kwargs): 
        super(ExamForm, self).__init__(*args, **kwargs)
        q_number = 1
        for question in exam.questions.all():
            self.fields['question_%s' % question.id] = forms.ChoiceField(
                choices=[(answer.id, answer.body) for answer in question.answers.all()],
                widget=forms.RadioSelect,
                label=f"{q_number} ) {question.body}",
            )
            q_number += 1
