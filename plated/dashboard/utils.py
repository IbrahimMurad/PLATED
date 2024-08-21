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


def score_progress(user, focus):
    model = {
        'lesson': Lesson,
        'chapter': Chapter,
        'unit': Unit,
        'subject': Subject,
    }
    focus_instances = model[focus].objects.filter(exams__student=user.student).distinct()
    focus_scores = []
    for  instance in focus_instances:
        solved_exams = instance.exams.filter(student=user.student, score__isnull=False)
        scores = [exam.score_percentage for exam in solved_exams]
        focus_scores.append({
            'title': instance.title,
            'scores': scores
            })
    return focus_scores


# lessons_exams = all_solved_exams.filter(lesson__isnull=False)
# chapters_exams = all_solved_exams.filter(chapter__isnull=False)
# units_exams = all_solved_exams.filter(unit__isnull=False)
# subjects_exams = all_solved_exams.filter(subject__isnull=False)

# lessons_with_solved_exams = Lesson.objects.filter(id__in=lessons_exams.values_list('lesson', flat=True).distinct())
# chapters_with_solved_exams = Chapter.objects.filter(id__in=chapters_exams.values_list('chapter', flat=True).distinct())
# units_with_solved_exams = Unit.objects.filter(id__in=units_exams.values_list('unit', flat=True).distinct())
# subjects_with_solved_exams = Subject.objects.filter(id__in=subjects_exams.values_list('subject', flat=True).distinct())

# lessons = [
#     {
#         'title': lesson.title,
#         'solved_exams': lessons_exams.filter(lesson=lesson),
#     }
#     for lesson in lessons_with_solved_exams
# ]

# for lesson in lessons:
#     print(lesson['title'])
#     for exam in lesson['solved_exams']:
#         print(f"{str(exam)} : {exam.score}")

# chapters = [
#     {
#         'title': chapter.title,
#         'solved_exams': chapters_exams.filter(chapter=chapter),
#     }
#     for chapter in chapters_with_solved_exams
# ]

# for chapter in chapters:
#     print(chapter['title'])
#     for exam in chapter['solved_exams']:
#         print(f"{str(exam)} : {exam.score}")

# units = [
#     {
#         'title': unit.title,
#         'solved_exams': units_exams.filter(unit=unit),
#     }
#     for unit in units_with_solved_exams
# ]

# for unit in units:
#     print(unit['title'])
#     for exam in unit['solved_exams']:
#         print(f"{str(exam)} : {exam.score}")

# subjects = [
#     {
#         'title': subject.title,
#         'solved_exams': subjects_exams.filter(subject=subject),
#     }
#     for subject in subjects_with_solved_exams
# ]

# for subject in subjects:
#     print(subject['title'])
#     for exam in subject['solved_exams']:
#         print(f"{str(exam)} : {exam.score}")