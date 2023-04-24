#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os.path
import click


def add_student(students, name, group, mark):
    """
    Добавление студента в список
    """
    students.append(
        {
            "name": name,
            "group": group,
            "mark": mark
        }
    )
    return students


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


@click.command()
@click.argument('command')
@click.argument('filename')
def main(command, filename):
    """
    Главная функция
    """
    is_dirty = False
    if os.path.exists(filename):
        students = load_students(filename)
    else:
        students = []

    if command == "add":
        name = click.prompt("Введите ФИО студета: ")
        group = int(click.prompt("Введите номер группы студета: "))
        mark = int(click.prompt("Введите оценку студета: "))
        students = add_student(
            students,
            name,
            group,
            mark
        )
        is_dirty = True

    elif command == "list":
        out_students(students)

    elif command == "filter":
        filter_list = students_filter(students)
        out_students(filter_list)

    if is_dirty:
        save_students(filename, students)


if __name__ == '__main__':
    main()
