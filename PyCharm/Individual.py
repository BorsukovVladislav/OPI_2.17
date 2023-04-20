#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path


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
            if student.get('mark') > 4:
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


def main(command_line=None):
    """
    Главная функция
    """
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="Имя файла"
    )
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Добавление студента"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        type=str,
        required=True,
        help="ФИО студента"
    )
    add.add_argument(
        "-g",
        "--group",
        action="store",
        type=int,
        help="Номер группы"
    )
    add.add_argument(
        "-m",
        "--mark",
        action="store",
        type=int,
        required=True,
        help="Оценка студента"
    )

    _ = subparsers.add_parser(
        "list",
        parents=[file_parser],
        help="Отобразить список студентов"
    )

    __ = subparsers.add_parser(
        "filter",
        parents=[file_parser],
        help="Студенты с оценкой выше 4"
    )

    args = parser.parse_args(command_line)

    is_dirty = False
    if os.path.exists(args.filename):
        students = load_students(args.filename)
    else:
        students = []

    if args.command == "add":
        students = add_student(
            students,
            args.name,
            args.group,
            args.mark
        )
        is_dirty = True

    elif args.command == "list":
        out_students(students)

    elif args.command == "filter":
        filter_list = students_filter(students)
        out_students(filter_list)

    if is_dirty:
        save_students(args.filename, students)


if __name__ == '__main__':
    main()
