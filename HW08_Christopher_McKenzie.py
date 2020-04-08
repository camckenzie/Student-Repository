"""Christopher McKenzie
The purpose of this program is to:
1. Find the date three days after Feb 27, 2020.
2. Find the date three days after Feb 27, 2019.
3. Find how many days passed between Feb 1, 2019 and Sept 30, 2019
4. Write a generator function to read field-separated text files and
yield a tuple with all of the values from a single line in the file.
5. Write a class, that given a directory name, searches that directory
for Python files. For each .py file in the directory, open each file
and calculate summaries of stats.
"""

from datetime import datetime, timedelta, date
from typing import Tuple, Iterator, List, Dict, IO
import os
from prettytable import PrettyTable


def date_arithmetic() -> Tuple[datetime, datetime, int]:

    """Function should be able to:
    1. Find the date three days after Feb 27, 2020.
    2. Find the date three days after Feb 27, 2019.
    3. Find how many days passed between Feb 1, 2019 and Sept 30, 2019.
    4. Return the above in a tuple
    """

    date1: str = "February 27, 2020"
    date2: str = "February 27, 2019"
    date3: str = "February 1, 2019"
    date4: str = "September 30, 2019"

    dt1: datetime = (datetime.strptime("February 27, 2020", "%B %d, %Y")
    + timedelta(days=3))
    dt2: datetime = (datetime.strptime("February 27, 2019", "%B %d, %Y")
    + timedelta(days=3))
    dt3: datetime = datetime.strptime("February 1, 2019", "%B %d, %Y")
    dt4: datetime = datetime.strptime("September 30, 2019", "%B %d, %Y")
    diff: int = (dt4 - dt3).days

    return dt1, dt2, diff


def file_reader(path: str, fields: int, sep: str = ",", header: bool = False) -> Iterator[List[str]]:

    """Generator function should read field-separated text files and
    yield a tuple with all of the values from a single line in the file
    on each call to next().
    """
    try:
        fp: IO = open(path, "r")
    except FileNotFoundError:
        raise FileNotFoundError(f"Unable to open {path}")

    else:
        with fp:
            for index, line in enumerate(fp):
                lines = line.rstrip("\n")
                tokens = (lines.split(sep))
                if len(tokens) == fields:
                    if header == True and index == 0:
                        continue
                    else:
                        yield tokens
                else:
                    raise ValueError(
                (f"{path} at line {index+1} expected {fields}"
                f" fields but found {len(tokens)} fields."))


                    
class FileAnalyzer:


    """Given a directory name, searches that directory for Python
    files. For each .py file in the directory, opens each file and
    calculates:
    1. The file name.
    2. The total number of lines in the file.
    3. The total number of characters in the file.
    4. The total number of functions in the file.
    5. The total number of classes in the file.
    """


    def __init__(self, directory: str) -> None:

        """Stores the directory and a dictionary of files with
        corresponding summary stats. Other functions will utilize
        directory and add to dictionary.
        """

        self.directory: str = directory
        self.files_summary: Dict[str, Dict[str, int]] = dict()

    def analyze_files(self) -> None:

        """Acquires python file names from directory as keys.
        File_stats uses these directories to pull summary data.  
        """

        try:
            files = os.listdir(self.directory)
        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to open: {self.directory}")
        for f in files:
            if f.endswith(".py") is True:
                self.file_stats(os.path.join(self.directory, f))

    def file_stats(self, path: str) -> str:

        """Using file names from analyze_files, acquires the total
        number of classes, functions, lines, and characters in each
        Python file.
        """
        
        classes = 0
        functions = 0
        lines = 0
        chars = 0

        try:
            fp: IO = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to open: {path}")
        else:
            with fp:
                for line in fp:
                    if line.startswith("class "):
                        classes += 1
                    elif line.lstrip().startswith("def "):
                        functions += 1
                    lines += 1
                    chars += len(line)

            self.files_summary[path] = {
                "class": classes,
                "function": functions,
                "line": lines,
                "char": chars
            }


    def pretty_print(self) -> None:

        """Creates a table from data stored in the self.files_summary
        """

        pt: PrettyTable = PrettyTable(field_names=[
            "File Name", "Classes",
            "Functions", "Lines", "Characters"]
            )
        for f, stats in self.files_summary.items():
            pt.add_row(
                [f, stats["class"], stats["function"], stats["line"],
                stats["char"]]
                )
        return pt

#fa = FileAnalyzer(r"Wrong")
#fa.analyze_files()