"""Christopher McKenzie
Test that the Repository class accurately prints the information
required for the Student Pretty Table and the Instrucor Pretty
Table.
"""

import unittest
from typing import DefaultDict, Tuple, Iterator, List, Dict, IO
from collections import defaultdict
import os
from prettytable import PrettyTable
from HW08_Christopher_McKenzie import file_reader
from HW09_Christopher_McKenzie import Student, Instructor, Repository


class RepositoryTest(unittest.TestCase):


    """Verify that Repositroy class prints Student and Instructor
    info correctly.
    """


    def test_students(self) -> None:

        """Verify that student information that goes into pretty
        table is set up correctly.
        """

        a = Repository(r"C:\Users\Chris\Desktop\HW09", False)   
        prd = {cwid: student.info() for cwid, student in a._students.items()}
        exp = {'10103': ['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']],
                    '10115': ['10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']],
                    '10172': ['10172', 'Forbes, I', ['SSW 555', 'SSW 567']],
                    '10175': ['10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']],
                    '10183': ['10183', 'Chapman, O', ['SSW 689']],
                    '11399': ['11399', 'Cordova, I', ['SSW 540']],
                    '11461': ['11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']],
                    '11658': ['11658', 'Kelly, P', ['SSW 540']],
                    '11714': ['11714', 'Morton, A', ['SYS 611', 'SYS 645']],
                    '11788': ['11788', 'Fuller, E', ['SSW 540']]}
        self.assertEqual(prd, exp)

    def test_instructors(self) -> None:

        """Verify that student information that goes into pretty
        table is set up correctly.
        """

        b = Repository(r"C:\Users\Chris\Desktop\HW09", False)
        prd = {tuple(info) for instructor in b._instructors.values() for info in instructor.info()}
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