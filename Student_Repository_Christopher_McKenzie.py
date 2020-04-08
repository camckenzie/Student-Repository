"""Christopher McKenzie
The purpose of this program is to create a data repository of
ourses, students and instructors. It will track Student CWIDs,
courses, grades, majors, GPAs, as well as Instructor IDs,
departments, courses taught, and number of students taught.
"""

from typing import DefaultDict, Tuple, Iterator, List, Dict, IO
from collections import defaultdict
import os
from prettytable import PrettyTable
from HW08_Christopher_McKenzie import file_reader

class Student:
    
    
    """
    1. Stores information about a single student including:
        a. CWID
        b. Name
        c. Major
        d. Container of courses and grades
    2. Allows other classes to add a course and grade to the
    container of courses and grades.
    3. Returns the summary data about a single student needed in the
    pretty table.
    """


    PT_FIELD_NAMES: List[str] = ["CWID", "Name", "Completed Courses"]
    
    def __init__(self, cwid: str, name: str, major: str) -> None:

        """Initializes the student's CWID, Name, Major, and a
        dictionary of their completed courses and corresponng grades.
        """

        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict() #courses[course_name] = grade
    
    def store_course_grade(self, course: str, grade: str) -> None:

        """Notes that a student took a specific course and earned
        a grade. To be utilized in class Repository, function
        read grades.
        """

        self._courses[course] = grade
    
    def info(self) -> List[str]:

        """Returns a list of info about self needed for pretty table.
        """
       
        return [self._cwid, self._name, sorted(self._courses.keys())]



class Instructor:


    """
    1. Stores information about a single instructor including:
        a. CWID
        b. Name
        c. Department
        d. Container of classes taught and number of students in each
        course.
    2. Allows other classes to specify a course, and update the
    container of courses taught to increment the number of students
    by 1.
    3. Returns the summary data needed by Instructor Pretty table.
    """


    PT_FIELD_NAMES: List[str] = ["CWID", "Name", "Dept", "Course", "Students"]

    def __init__(self, cwid: str, name: str, dept: str) -> None:

        """Initializes the instructors's CWID, Name, Dept, and a
        dictionary of courses taught and number of students taught
        for those specific classes.
        """

        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int) #courses[course_name] = #students

    def store_course_student(self, course: str) -> None:

        """Notes that instruuctor taught a course to one more student.
        To be utilized in class Repository, function read grades.
        """

        self._courses[course] += 1

    def info(self) -> Iterator[List[str]]:

        """Returns a list of info about self needed for pretty table.
        """

        for course, count in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, count]

class Repository:


    """
    1. Includes a container for all students.
    2. Include a container for all instructors
    3. Specifies directory path to find txt fles.
    4. Read students.txt file, creating a new instance of
    class Student for each line in the file, and add the new Student
    to the repository's container with all students.
    5. Read the instructors.txt file, creating a new instance of
    class Instructor for each line in the file, and add the new
    Instructor to the repository's container with all Instructors.
    6. Read the grades.txt file and process each grade:
        a. Use the student CWID, course, and grade, and ask the
        instance of class Student aassociated with the student CWID
        to add the grade to the student information.
        b. Use the instructor CWID and course to ask the instance of
        class Instructor to note that the instructor taught another
        student in the specific course.
    7. Print a student prettytable.
    8. Print an instructor prettytable.
    """


    def __init__(self, path: str, print_tables: bool=True) -> None:
        
        """
        1. Stores the directory path to find appropriate text files.
        2. Reads the text files for students, instructors, and grades.
        3. Prints student and instructor pretty tables.
        """
        
        self._path: str = path
        self._students: Dict[int, Student] = dict() #students[cwid] = Student()
        self._instructors: Dict[int, Instructor] = dict() #instructors[cwid] = Student()
        
        self._read_students(path)
        self._read_instructors(path)
        self._read_grades(path)

        if print_tables is True: #Will always print unless set to False
            self.student_pretty_table()
            self.instructor_pretty_table()

    def _read_students(self, path: str) -> None:

        """Reads each line in the studentss.txt and creates an
        instance of the Student class for each line.
        """

        try:
            for cwid, name, major in file_reader(os.path.join(self._path, "students.txt"), 3, sep="\t", header=False):
                self._students[cwid] = Student(cwid, name, major)
        except (FileNotFoundError, ValueError) as e:
            print(e)


    def _read_instructors(self, path: str) -> None:        

        """Reads each line in the instructors.txt and creates an
        instance of the Instructor class for each line.
        """

        try:
            for cwid, name, dept in file_reader(os.path.join(self._path, "instructors.txt"), 3, sep="\t", header=False):
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except (FileNotFoundError, ValueError) as e: 
            print(e)
  

    def _read_grades(self, path: str) -> None:

        """
        1. Reads grades.txt
        2. Searches for student associated with the student_cwid and updates
        the Student dictionary with the student's courses and grades.
        3. Searches for instructor associated with the instructor_cwid and
        notes that the instructor taught one more student in a course. 
        """

        try:
            for student_cwid, course, grade, instructor_cwid in file_reader(os.path.join(self._path, "grades.txt"), 4, sep="\t", header=False):

                if student_cwid not in self._students:
                    print(f"Unknown Student CWID {student_cwid} found in grades.txt")
                else:
                    s: Student = self._students[student_cwid]
                    s.store_course_grade(course, grade)

                if instructor_cwid not in self._instructors:
                    print(f"Unknown Instructor CWID {instructor_cwid} found in grades.txt")
                else:
                    inst: Instructor = self._instructors[instructor_cwid]
                    inst.store_course_student(course)

        except (FileNotFoundError, ValueError) as e:
            print(e)

    def student_pretty_table(self) -> None:

        """Prints pretty table using info in Student class.
        """

        pt: PrettyTable = PrettyTable(field_names=Student.PT_FIELD_NAMES)

        for stu in self._students.values():
            pt.add_row(stu.info())
            
        print("Student Summary \n", pt)
    
    def instructor_pretty_table(self) -> None:

        """Prints the pretty table using info in Instructor class.
        """

        pt: PrettyTable = PrettyTable(field_names=Instructor.PT_FIELD_NAMES)

        for inst in self._instructors.values():
            for info in inst.info():
                pt.add_row(info)

        print("Instructor Summary\n",pt)
