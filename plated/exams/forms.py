from django import forms


class GenerateExamForm(forms.Form):
    focus = forms.CharField(max_length=16, widget=forms.HiddenInput())
    id = forms.IntegerField(widget=forms.HiddenInput())


class ExamForm(forms.Form):
    def __init__(self, exam=None, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        q_number = 1
        for question in exam.questions.all():
            self.fields["question_%s" % question.id] = forms.ChoiceField(
                choices=[(answer.id, answer.body) for answer in question.answers.all()],
                widget=forms.RadioSelect,
                label=f"{q_number} ) {question.body}",
            )
            q_number += 1


class NewExamForm(forms.Form):
    grade = forms.IntegerField(widget=forms.HiddenInput())
    focus = forms.ChoiceField(
        choices=[
            (None, "Select focus"),
            ("subject", "subject"),
            ("unit", "unit"),
            ("chapter", "chapter"),
            ("lesson", "lesson"),
        ],
        required=True,
        label="Focus",
    )
    id = forms.ChoiceField(choices=(), required=True, disabled=True, label="Select")
