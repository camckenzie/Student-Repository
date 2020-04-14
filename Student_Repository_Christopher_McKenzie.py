"""Christopher McKenzie
The purpose of this program is to create a data repository of
majors, courses, students and instructors. It will track Student
CWIDs, names, majors, completed courses, remaining required courses,
remaining electives, grade, and cumulative GPA, as well as Instructor IDs,
departments, courses taught, and number of students taught.
Additionally, it will store Majors and their respective required
courses and electives.
"""

from typing import DefaultDict, Tuple, Iterator, List, Dict, IO
from collections import defaultdict
import os, sqlite3
from prettytable import PrettyTable
from HW08_Christopher_McKenzie import file_reader


class Student:
    
    
    """
    1. Stores information about a single student including:
        a. CWID
        b. Name
        c. Major
        d. Completed courses
        e. Remaining required courses
        f. Remaining electives
        g. Cumulative GPA
    2. Allows other classes to add a course and grade to the
    container of courses and grades.
    3. Returns the summary data about a single student needed in the
    pretty table.
    """


    PT_FIELD_NAMES: List[str] = ["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives", "GPA"]
    
    def __init__(self, cwid: str, name: str, major: str, required: List[str], electives: List[str]) -> None:

        """Initializes the student's CWID, Name, Major, remaining
        required and elective courses, and a dictionary of their
        completed courses and corresponding grades.
        """

        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        
        self._remaining_required: List[str] = required
        self._remaining_electives: List[str] = electives

        self._courses: Dict[str, str] = dict() #courses[course_name] = grade
        
    def store_course_grade(self, course: str, grade: str) -> None:

        """
        1. Notes that a student took a specific course and earned
        a grade.
        2. Removes completed courses from remaining
        required courses if grade is C or above.
        3. Sets required electives to empty list if student completes
        course with a grade C or above.
        4. To be utilized in class Repository, function read grades.
        """

        scores: Dict[str, int] = {"A" : 4.0, "A-": 3.75, "B+" : 3.25, "B" : 3.0, "B-" : 2.75, "C+" : 2.25, "C" : 2.0}

        if grade in scores:
            self._courses[course] = scores.get(grade)
            if course in self._remaining_required:
                self._remaining_required.remove(course)
            elif course in self._remaining_electives:
                self._remaining_electives = []

    def info(self) -> List[str]:

        """Returns a list of info about self needed for pretty table.
        Also calculates cumulative GPA.
        """

        total = sum(self._courses.values())
        classes = len(self._courses.values())

        if classes == 0:
            gpa = 0
        else:
            gpa = total/classes

        return [self._cwid, self._name, self._major, sorted(self._courses.keys()), self._remaining_required, self._remaining_electives, round(gpa, 2)]

class Major:
    
    
    """
    1. Stores information about students' majors including:
        a. Required courses
        b. Electives
        c. Major
    2. Allows other classes to add courses to the
    container of required courses and electives.
    3. Returns a list of all required and all elective courses
    needed in the Student class.
    4. Returns the summary data about a major needed in the
    pretty table.
    """


    PT_FIELD_NAMES: List[str] = ["Major", "Required Courses", "Electives"]
    
    def __init__(self, major: str) -> None:

        """Initializes the major, required courses, and electives.
        """

        self._major: str = major
        self._required = list()
        self._electives = list()

    def add_course(self, re: str, course: str) -> None:

        """Notes all required and elective courses for major in
        appropriate lists.
        """

        if re == "R":
            self._required.append(course)
        elif re == "E":
            self._electives.append(course)

    def info(self) -> List[str]:

        """Returns a list of info about major needed for pretty table.
        """
       
        return [self._major, self._required, self._electives]

    def get_required(self) -> List[str]:

        """Returns a copy of a list of all required courses for a
        major. To be utilized by Student class to track remaining
        required courses.
        """

        return list(self._required)

    def get_electives(self) -> List[str]:

        """Returns a copy of a list of all required electives for a
        major. To be utilized by Student class to track remaining
        required electives.
        """

        return list(self._electives)

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

        """Notes that instructor taught a course to one more student.
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
    2. Include a container for all instructors.
    3. Include a container for all majors.
    3. Specifies directory path to find txt files.
    4. Read majors.txt file, creating a new instance of class Major
    for each new major in the file, and add the new Major to the
    repository's container with all majors.
    5. Read students.txt file, creating a new instance of
    class Student for each line in the file, and add the new Student
    to the repository's container with all students.
    6. Read the instructors.txt file, creating a new instance of
    class Instructor for each line in the file, and add the new
    Instructor to the repository's container with all Instructors.
    7. Read the grades.txt file and process each grade:
        a. Use the student CWID, course, and grade, and ask the
        instance of class Student aassociated with the student CWID
        to add the grade to the student information.
        b. Use the instructor CWID and course to ask the instance of
        class Instructor to note that the instructor taught another
        student in the specific course.
    8. Print a major prettytable.
    9. Print a student prettytable.
    10. Print an instructor prettytable.
    11. Print a student grades pretty table using data from a table
    in an SQLite database file.
    """


    def __init__(self, path: str, print_tables: bool=True) -> None:
        
        """
        1. Stores the directory path to find appropriate text files.
        2. Reads the text files for students, instructors, and grades.
        3. Prints student and instructor pretty tables.
        """
        
        self._path: str = path
        self._majors: Dict[str, Major] = dict() #majors[major] = Major()
        self._students: Dict[int, Student] = dict() #students[cwid] = Student()
        self._instructors: Dict[int, Instructor] = dict() #instructors[cwid] = Student()

        self._read_majors(path)
        self._read_students(path)
        self._read_instructors(path)
        self._read_grades(path)
        
        if print_tables is True: #Will always print unless set to False
            self.major_pretty_table()
            self.student_pretty_table()
            self.instructor_pretty_table()
            self.student_grades_table_db()

    def _read_majors(self, path: str) -> None:

        """Reads each line in the majors.txt and creates an instance
        of the Major class for each new major. Otherwise, just adds
        new required courses and electives to existing instance of
        major. 
        """

        try:
            for major, re, course in file_reader(os.path.join(self._path, "majors.txt"), 3, sep="\t", header=True):
                if major not in self._majors:
                    self._majors[major] = Major(major)
                self._majors[major].add_course(re, course)

        except (FileNotFoundError, ValueError) as e:
            print(e)

    def _read_students(self, path: str) -> None:

        """Reads each line in the students.txt and creates an
        instance of the Student class for each line.
        """

        try:
            for cwid, name, major in file_reader(os.path.join(self._path, "students.txt"), 3, sep="\t", header=True):
                if major in self._majors:
                    required: List[str] = self._majors[major].get_required()
                    electives: List[str] = self._majors[major].get_electives()
                    self._students[cwid] = Student(cwid, name, major, required, electives)
                else:
                    self._students[cwid] = Student(cwid, name, major, "Unknown for this major", "Unknown for this major")
                    print(f"Unknown Major {major} found in students.txt")

        except (FileNotFoundError, ValueError) as e:
            print(e)
        
    def _read_instructors(self, path: str) -> None:        

        """Reads each line in the instructors.txt and creates an
        instance of the Instructor class for each line.
        """

        try:
            for cwid, name, dept in file_reader(os.path.join(self._path, "instructors.txt"), 3, sep="\t", header=True):
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
            for student_cwid, course, grade, instructor_cwid in file_reader(os.path.join(self._path, "grades.txt"), 4, sep="\t", header=True):

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

    def major_pretty_table(self) -> None:

        """Prints pretty table using info in Major class.
        """

        pt: PrettyTable = PrettyTable(field_names=Major.PT_FIELD_NAMES)
        
        for major in self._majors.values():
            pt.add_row(major.info())

        print("Majors Summary \n", pt)

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

    def student_grades_table_db(self) -> None:

        """Prints pretty table using info from table in SQLite
        database file.
        """

        DB_FILE: str = r"C:\Users\Chris\Desktop\HW11\HW11_Database.db"
        
        try: 
            db: sqlite3.Connection = sqlite3.connect(DB_FILE)
        except sqlite3.OperationalError:
            print("Missing SQLite database.")
        else:
            PT_FIELD_NAMES: List[str] = ["Name", "CWID", "Course", "Grade", "Instructor"]
            pt: PrettyTable = PrettyTable(field_names=Instructor.PT_FIELD_NAMES)
            
            query: str = """select s.Name as Student, s.CWID, g.Course, g.Grade, i.Name as Instructor
                            from students s
                                join grades g on s.CWID=g.StudentCWID
                                join instructors i on i.CWID=g.InstructorCWID
                                order by Student"""
        
            try:
                for row in db.execute(query):
                    pt.add_row(row)
                print("Student Grade Summary \n", pt)
            except sqlite3.OperationalError as e:
                print("Missing SQLite database.")
