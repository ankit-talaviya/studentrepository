# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 08:33:50 2020

@author: Ankit
"""

from collections import defaultdict
from typing import Dict, DefaultDict, Iterator, Tuple, List, Set
from prettytable import PrettyTable
import os


class Major:
    """ class that represent majors """

    pt_field_names = ["Major", "Required Courses", "Electives"]

    def __init__(self, major: str, passing = None) -> None:
        self._major: str = major
        self._required = dict()
        self._electives = dict()
        if passing is None:
            self._grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
        else:
            self._grades = passing

    def add_course(self, flag: str, course: str) -> None:    
        if flag == 'R':
            self._required[course] = flag
        elif flag == 'E':
            self._electives[course] = flag
        else:
            print(f"Unknown Flag found {flag}")
        
    def remaining_course(self, cwid, completed_course) -> tuple:

        passed_courses = {course for course, grade in completed_course.items() if grade in self._grades}
        
        remaining_required = set(self._required) - passed_courses
        required = set(self._electives)

        if required.intersection(passed_courses):
            remaining_elective = []
        else:
            remaining_elective = required
        
        gpa: float = 0.0
        GPA: float = 0.0
        
        grade_point: Dict[str, int] = {'A':4.0, 'A-':3.75,'B+':3.25, 'B':3.0, 'B-':2.75, 'C+':2.75, 'C':2.0, 'C-':0, 'D+':0, 'D':0, 'D-':0, 'F':0}
        for grade in completed_course.values():
            for grd, pnt in grade_point.items():
                if grade == grd:
                    gpa += pnt

        if len(passed_courses) == 0:
            print(f"Student {cwid} has not passed with minimum grade point")
        else:
            GPA = round(gpa/len(passed_courses), 2)

        return self._major, passed_courses, remaining_required, remaining_elective, GPA

    def major_info(self) -> list:
        """display records"""

        return [self._major, sorted(self._required), sorted(self._electives)]


class Student:
    """ Class that represenrts students """

    pt_field_names = ["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives", "GPA"]

    def __init__(self, cwid: str, name: str, major: str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._course: Dict[str,str] = dict()
    
    def add_course_grade(self, course: str, grade: str) -> None:
        self._course[course] = grade
    
    def student_info(self) -> list:
        
        major, passed, remaining_req, remaining_ele, GPA = self._major.remaining_course(self._cwid, self._course)
        
        return [self._cwid, self._name, major, sorted(passed), remaining_req, remaining_ele, GPA]

class Instructor:
    """ Class that represent instructors """

    pt_field_names = ["CWID", "Name", "Dept", "Course", "Students"]

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
        self._majors: Dict[str, Major] = dict()
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()
        self.read_majors(path)
        self.read_students(path)
        self.read_instructors(path)
        self.read_grades(path)
        self.major_prettytable()
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


    def read_majors(self, path: str) -> None:
        """ Analyze the information from majors.txt file """
        try:
            for major, flag, course in self.file_reader(os.path.join(self._path, 'majors.txt'),3, sep = "\t", header = True):
                if major not in self._majors:
                    self._majors[major] = Major(major)
                self._majors[major].add_course(flag, course)
        except (FileNotFoundError, ValueError) as e:
            print(e)


    def read_students(self, path: str) -> None:
        """ Analyze the information from students.txt file """
        try:
            for cwid, name, major in self.file_reader(os.path.join(self._path, 'students.txt'), 3, sep = ";", header = True):
                if cwid in self._students:
                    print(f"{cwid} is already exists")
                else:
                    self._students[cwid] = Student(cwid, name, self._majors[major])
        except (FileNotFoundError, ValueError) as e:
            print(e)


    def read_instructors(self, path: str) -> None:
        """ Analyze the information from instructors.txt file """
        try:
            for cwid, name, dept in self.file_reader(os.path.join(self._path, 'instructors.txt'), 3, sep = "|", header = True):
                if cwid in self._instructors:
                    print(f"{cwid} is already exists")
                else:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
        except (FileNotFoundError, ValueError) as e:
            print(e)


    def read_grades(self, path: str) -> None:
        """ Analyze the information from grades.txt file """
        try:
            for student_cwid, course, grade, instructor_cwid in self.file_reader(os.path.join(self._path, 'grades.txt'), 4, sep ='|', header = True):
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


    def major_prettytable(self) -> None:
        """ Print prettytable with major information """
        pt = PrettyTable(field_names = Major.pt_field_names)
        for major in self._majors.values():
            pt.add_row(major.major_info())
        print("Majors Summary")
        print(pt)


    def student_prettytable(self) -> None:
        """ Print prettytable with student information """
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