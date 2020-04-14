"""Christopher McKenzie
Test that the Repository class accurately prints the information
required for the Major, Student, and Instructor Pretty Tables.
"""

import unittest
from typing import DefaultDict, Tuple, Iterator, List, Dict, IO
from collections import defaultdict
import os, sqlite3
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

        a = Repository(r"C:\Users\Chris\Desktop\HW11", False)   
        prd = {major: courses.info() for major, courses in a._majors.items()}
        exp = {'SFEN': ['SFEN', ['SSW 540', 'SSW 810', 'SSW 555'], ['CS 501', 'CS 546']],
            'CS': ['CS', ['CS 570', 'CS 546'], ['SSW 810', 'SSW 565']]
            }
        
        self.assertEqual(prd, exp)

    def test_students(self) -> None:

        """Verify that student information that goes into pretty
        table is set up correctly.
        """

        b = Repository(r"C:\Users\Chris\Desktop\HW11", False)   
        prd = {cwid: student.info() for cwid, student in b._students.items()}
        exp = {'10103': ['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], 3.38],
            '10115': ['10115', 'Bezos, J', 'SFEN', ['SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], 4.0],
            '10183': ['10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546'], 4.0],
            '11714': ['11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], [], [], 3.5]}
        self.assertEqual(prd, exp)

    def test_instructors(self) -> None:

        """Verify that instructor information that goes into pretty
        table is set up correctly.
        """

        c = Repository(r"C:\Users\Chris\Desktop\HW11", False)
        prd = {tuple(info) for instructor in c._instructors.values() for info in instructor.info()}
        exp = {('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
                ('98764', 'Cohen, R', 'SFEN', 'CS 546', 1),
                ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),
                ('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                ('98762', 'Hawking, S', 'CS', 'CS 570', 1)}
        self.assertEqual(prd, exp)

    def test_student_grades(self) -> None:

        """Verify that student grade information that goes into
        pretty table is set up correctly.
        """
        d = Repository(r"C:\Users\Chris\Desktop\HW11", False)
        
        DB_FILE: str = r"C:\Users\Chris\Desktop\HW11\HW11_Database.db"
        db: sqlite3.Connection = sqlite3.connect(DB_FILE)
        query: str = """select s.Name as Student, s.CWID, g.Course, g.Grade, i.Name as Instructor
                from students s
                    join grades g on s.CWID=g.StudentCWID
                    join instructors i on i.CWID=g.InstructorCWID
                    order by Student"""
                    
        prd = {row for row in db.execute(query)}
        exp = {('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J'),
                ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
                ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
                ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
                ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
                ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
                ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
                ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S')
                }

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)