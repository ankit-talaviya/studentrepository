# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 10:57:18 2020

@author: Ankit
"""

import unittest
from HW10_Ankit_Talaviya import Major, Student, Instructor, Repository

class TestRepository(unittest.TestCase):

    def test_major_summary(self):
        """ Testing the major summary """
        test = Repository("C:/Users/Ankit/Desktop/SSW810")
        major_list = {mjr: Major.major_info() for mjr, Major in test._majors.items()}
        expected = {'SFEN': ['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'] ,['CS 501', 'CS 513', 'CS 545']],
                    'SYEN': ['SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']]}
        self.assertEqual(major_list, expected)

    def test_student_summary(self):
        """ Testing the student summary """
        test = Repository("C:/Users/Ankit/Desktop/SSW810")
        student_list = list()
        for cwid, Student in test._students.items():
            student_list.append(Student.student_info())
        expected = [['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 540', 'SSW 555'}, [], 3.44],
                    ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 540', 'SSW 555'}, [], 3.81], 
                    ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], {'SSW 540', 'SSW 564'}, {'CS 501', 'CS 513', 'CS 545'}, 3.88], 
                    ['10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], {'SSW 540', 'SSW 555'}, {'CS 501', 'CS 513', 'CS 545'}, 3.58], 
                    ['10183', 'Chapman, O', 'SFEN', ['SSW 689'], {'SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'},{'CS 501', 'CS 513', 'CS 545'}, 4.0], 
                    ['11399', 'Cordova, I', 'SYEN', ['SSW 540'], {'SYS 612', 'SYS 671', 'SYS 800'}, [], 3.0], 
                    ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], {'SYS 612', 'SYS 671'}, {'SSW 540', 'SSW 565', 'SSW 810'}, 3.92],
                    ['11658', 'Kelly, P', 'SYEN', [], {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 540', 'SSW 565', 'SSW 810'}, 0], 
                    ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 540', 'SSW 565', 'SSW 810'}, 3.0], 
                    ['11788', 'Fuller, E', 'SYEN', ['SSW 540'],{'SYS 612', 'SYS 671', 'SYS 800'}, [], 4.0]]
        self.assertEqual(student_list, expected)


    def test_instructor_summary(self):
        """ Testing the instructor summary """
        test = Repository("C:/Users/Ankit/Desktop/SSW810")
        instructor_list = {tuple(i) for instructor in test._instructors.values() for i in instructor.instructor_info()}
        expected = {('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                    ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)}
        self.assertEqual(instructor_list, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)