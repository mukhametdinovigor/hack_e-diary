import random

from datacenter.models import Schoolkid, Mark, Subject, Chastisement, Lesson, Commendation
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def fix_marks(schoolkid):
    bad_child_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in bad_child_marks:
        mark.points = 5
        mark.save()


def get_subjects(year_of_study):
    subjects = [subject.title for subject in Subject.objects.filter(year_of_study=year_of_study)]
    return subjects


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(year_of_study, group_letter, schoolkid, subject):
    commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!'
    ]
    commendation = random.choice(commendations)
    try:
        lesson = random.choice(Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter,
                                                 subject__title=subject))
    except IndexError:
        print(f'Не существует такого урока - {subject}')
    else:
        Commendation.objects.create(text=commendation, created=lesson.date, schoolkid=schoolkid, subject=lesson.subject,
                                teacher=lesson.teacher)


def main():
    name = 'Фролов Иван'
    year_of_study = 6
    group_letter = 'А'
    schoolkid_subject = ''
    random_subject = random.choice(get_subjects(year_of_study))
    if schoolkid_subject:
        subject = schoolkid_subject
    else:
        subject = random_subject
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except ObjectDoesNotExist:
        print('Ученика с таким именем не существует')
    except MultipleObjectsReturned:
        print('Есть несколько учеников с таким именем')
    else:
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(year_of_study, group_letter, schoolkid, subject)


if __name__ == '__main__':
    main()
