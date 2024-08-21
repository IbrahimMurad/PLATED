import matplotlib.pyplot as plt
from exams.models import Exam
from subjects.models import Lesson, Chapter, Unit, Subject

def avg(lst):
    if len(lst) == 0:
        return 0
    return sum(lst) / len(lst)


def avg_score_progress(user, condition):
    solved_exams = Exam.objects.filter(student=user.student, score__isnull=False, **condition)
    scores = [exam.score_percentage for exam in solved_exams]
    return [avg(scores[:i]) for i in range(1, len(scores) + 1)]


def plot(name, data, id):
    name = name.replace('_', ' ').upper()
    print(name)
    plt.figure(figsize=(12, 5))
    plt.plot(data, '-o', color='gray', alpha=0.4, linewidth=2)
    plt.stairs(data, linewidth=2)
    plt.xlabel("Number of Exams")
    plt.ylabel("Average Score (%)")
    plt.xlim(0, len(data))
    plt.ylim(0, 100)
    plt.xticks(range(0, len(data) + 1, 1))
    plt.yticks(range(0, 101, 10))
    plt.grid()
    plt.title(name)
    plt_url = f"/media/plots/{id}_{name}.jpg"
    plt.savefig(plt_url[1:], bbox_inches='tight')
    plt.close()
    return plt_url


def score_progress(user, focus, filter):
    model = {
        'lesson': Lesson,
        'chapter': Chapter,
        'unit': Unit,
        'subject': Subject,
    }
    focus_instances = model[focus].objects.filter(exams__student=user.student).distinct()
    focus_instances = focus_instances.filter(**filter)
    focus_scores = []
    for  instance in focus_instances:
        solved_exams = instance.exams.filter(student=user.student, score__isnull=False)
        scores = [exam.score_percentage for exam in solved_exams]
        focus_scores.append({
            'id': instance.id,
            'title': instance.title,
            'scores': scores
            })
    return focus_scores
