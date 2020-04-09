# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 08:33:50 2020

@author: Ankit
"""

from collections import defaultdict
from typing import Dict, DefaultDict, Iterator, Tuple
from prettytable import PrettyTable
import os

class Student:
    """ Class that represenrts students """

    pt_field_names = ["CWID", "Name", "Completed Courses"]

    def __init__(self, cwid: str, name: str, major: str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()

    def add_course_grade(self, course: str, grade: str) -> None:
        self._courses[course] = grade

    def student_info(self):
        return [self._cwid, self._name, sorted(self._courses.keys())]


class Instructor:
    """ Class that represent instructors """

    pt_field_names = ["CWID", "Name", "Dept", "Course", "Students"]

    def __init__(self, cwid: str, name: str, dept: str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int)

    def add_course_student(self, course: str) -> None:
        self._courses[course] += 1

    def instructor_info(self):
        for course, students in self._courses.items():
            yield (self._cwid, self._name, self._dept, course, students)

class Repository:
    """ Class that represent repository """
    def __init__(self, path): 
        self._path: str = path
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()
        self.read_students(path)
        self.read_instructors(path)
        self.read_grades(path)
        self.student_prettytable()
        self.instructor_prettytable()


    def file_reader( self, path: str, fields: int, sep: str, header: bool = False) -> Iterator[Tuple[str]]:
        """ Generator that read field-separated text files and returns one line at a time """
        try:
            file_path = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open {path} for reading!..")
        else:
            with file_path:
                line_num: int = 0
                if header:
                    if len(next(file_path).split(sep)) != fields:
                        raise ValueError(f"Header not valid")    
                    line_num = line_num + 1
                for line in file_path:
                    line = line.strip("\n").split(sep)
                    line_num = line_num + 1
                    if len(line) != fields:
                        raise ValueError(f"'{path}' has {len(line)} fields on line {line_num} but expected {fields}")
                    yield tuple(line)


    def read_students(self, path: str) -> None:
        """ Analyze the information from students.txt file """
        try:
            for cwid, name, major in self.file_reader(os.path.join(self._path, 'students.txt'), 3, sep = "\t", header = False):
                if cwid in self._students:
                    print(f"{cwid} is already exists")
                else:
                    self._students[cwid] = Student(cwid, name, major)
        except (FileNotFoundError, ValueError) as e:
            print(e)


    def read_instructors(self, path: str) -> None:
        """ Analyze the information from instructors.txt file """
        try:
            for cwid, name, dept in self.file_reader(os.path.join(self._path, 'instructors.txt'), 3, sep = "\t", header = False):
                if cwid in self._instructors:
                    print(f"{cwid} is already exists")
                else:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
        except (FileNotFoundError, ValueError) as e:
            print(e)


    def read_grades(self, path: str) -> None:
        """ Analyze the information from grades.txt file """
        try:
            for student_cwid, course, grade, instructor_cwid in self.file_reader(os.path.join(self._path, 'grades.txt'), 4, sep ='\t', header = False):
                if student_cwid in self._students:
                    self._students[student_cwid].add_course_grade(course, grade) 
                else:
                    print(f"Student cwid {student_cwid} is not in the students file")

                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_course_student(course) 
                else:
                    print(f"instructor cwid {instructor_cwid} is not in the instructor file")
        except ValueError as e:
            print(e)


    def student_prettytable(self) -> None:
        """ Print pretytable with student information """
        pt = PrettyTable(field_names = Student.pt_field_names)
        for stud in self._students.values():
            pt.add_row(stud.student_info())
        print("Student Summary")
        print(pt)


    def instructor_prettytable(self) -> None:
        """ print prettytable with instructor information """
        pt = PrettyTable(field_names = Instructor.pt_field_names)
        for inst in self._instructors.values():
            for inst_row in inst.instructor_info():
                pt.add_row(inst_row)
        print("Instructor Summary")
        print(pt)


def main():
    try:
        Repository("C:/Users/Ankit/Desktop/SSW810")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()