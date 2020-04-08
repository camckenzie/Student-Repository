"""Christopher McKenzie
Test that the Repository class accurately prints the information
required for the Major, Student, and Instructor Pretty Tables.
"""

import unittest
from typing import DefaultDict, Tuple, Iterator, List, Dict, IO
from collections import defaultdict
import os
from prettytable import PrettyTable
from HW08_Christopher_McKenzie import file_reader
from Student_Repository_Christopher_McKenzie import Student, Instructor, Major, Repository


class RepositoryTest(unittest.TestCase):


    """Verify that Repositroy class prints Major, Student and
    Instructor info correctly.
    """

    def test_majors(self) -> None:

        """Verify that major information that goes into pretty
        table is set up correctly.
        """

        a = Repository(r"C:\Users\Chris\Desktop\HW10", False)   
        prd = {major: courses.info() for major, courses in a._majors.items()}
        exp = {'SFEN': ['SFEN', ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'],['CS 501', 'CS 513', 'CS 545']],
                'SYEN': ['SYEN', ['SYS 671', 'SYS 612', 'SYS 800'], ['SSW 810', 'SSW 565', 'SSW 540']]}
        
        self.assertEqual(prd, exp)

    def test_students(self) -> None:

        """Verify that student information that goes into pretty
        table is set up correctly.
        """

        b = Repository(r"C:\Users\Chris\Desktop\HW10", False)   
        prd = {cwid: student.info() for cwid, student in b._students.items()}
        exp = {'10103': ['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], 3.44],
                '10115': ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], 3.81],
                '10172': ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'], ['CS 501', 'CS 513', 'CS 545'], 3.88],
                '10175': ['10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 513', 'CS 545'], 3.58],
                '10183': ['10183', 'Chapman, O', 'SFEN', ['SSW 689'], ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545'], 4.0],
                '11399': ['11399', 'Cordova, I', 'SYEN', ['SSW 540'], ['SYS 671', 'SYS 612', 'SYS 800'], [], 3.0],
                '11461': ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 671', 'SYS 612'], ['SSW 810', 'SSW 565', 'SSW 540'], 3.92],
                '11658': ['11658', 'Kelly, P', 'SYEN', [], ['SYS 671', 'SYS 612', 'SYS 800'], ['SSW 810', 'SSW 565', 'SSW 540'], 0],
                '11714': ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], ['SYS 671', 'SYS 612', 'SYS 800'], ['SSW 810', 'SSW 565', 'SSW 540'], 3.0],
                '11788': ['11788', 'Fuller, E', 'SYEN', ['SSW 540'], ['SYS 671', 'SYS 612', 'SYS 800'], [], 4.0]}
        self.assertEqual(prd, exp)

    def test_instructors(self) -> None:

        """Verify that student information that goes into pretty
        table is set up correctly.
        """

        c = Repository(r"C:\Users\Chris\Desktop\HW10", False)
        prd = {tuple(info) for instructor in c._instructors.values() for info in instructor.info()}
        exp = {('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                    ('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                    ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3)}
        self.assertEqual(prd, exp)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)