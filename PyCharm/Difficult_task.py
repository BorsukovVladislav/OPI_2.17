#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os.path
import click


def add_student(studs, n, g, m):
    """
    Добавление студента в список
    """
    studs.append(
        {
            "name": n,
            "group": g,
            "mark": m
        }
    )
    return studs


def out_students(list_stud):
    """
    Вывод списка студентов
    """
    if list_stud:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 14,
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^14} |'.format(
                "№",
                "Ф.И.О.",
                "Номер группы",
            )
        )
        print(line)

        for idx, student in enumerate(list_stud, 1):
            print(
                '| {:>4} | {:<30} | {:<14} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                )
            )
        print(line)
    else:
        print("Список студентов пустой.")


def students_filter(list_s):
    """
    Вывод списка студентов со средним баллом больше 4
    """
    if len(list_s) > 0:
        filter_s = []
        for student in list_s:
            if int(student.get('mark')) > 4:
                filter_s.append(student)
        return filter_s
    else:
        print("Список студентов пустой.")


def save_students(file_name, students):
    """
    Сохранение всех студентов в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    """
    Загрузка всех студентов из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


@click.group()
@click.pass_context
def main(students):
    """
    Главная функция
    """
    students.ensure_object(dict)


@main.command()
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
@click.option('--name', prompt='Введите ФИО студента')
@click.option('--group', prompt='Введите группу студента')
@click.option('--mark', prompt='Введите оценку студента', type=float)
def add(students, name, group, mark, filename):
    """
    Добавить новый товар.
    """
    if os.path.exists(filename):
        students = load_students(filename)
    else:
        students = []

    students = add_student(students, name, group, mark)
    save_students(filename, students)


@main.command()
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
def list(students, filename):
    """
    Отобразить список студентов.
    """
    if os.path.exists(filename):
        students = load_students(filename)
        out_students(students)


@main.command()
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
def filter(students, filename):
    """
    Выбрать товары из магазина.
    """
    if os.path.exists(filename):
        students = load_students(filename)
        out_students(students_filter(students))


if __name__ == '__main__':
    main()
