"""
This file inizilaizes the SQL database
"""
import sqlite3
import datetime

class Patient(object):
    """
    A Patient is a person who has come to see the doctor.
    they have patient number, last name, firstname, age, weight, height, bloodtype, sex.
    """

    def __init__(self, lname, fname, age, weight, height, bloodtype, sex):
        """
        Initializes a patient with patient number, last name, firstname, age, weight, height, bloodtype, sex.
        """
        
        
        self.lname = lname.capitalize()
        self.fname = fname.capitalize()
        self.age = age
        self.weight = weight
        self.height = height
        self.bloodtype = bloodtype
        self.sex = sex

    # @classmethod
    # def get_all_pats(cls):
    #     """
    #     Get all the patients from the patients.db and initialize them to a class and put in a list.
    #     """
    #     c.execute('SELECT * FROM patients')
    #     return c.fetchall


class database(object):
    """
    Database is used to open and manipulate the sql file holding all the patient data.
    """

    def __init__(self):
        #various file connections.
        self.patfile = "patients.db"
        self.comfile = "comments.db"
        self.patconn = sqlite3.connect('patients.db')
        self.comconn = sqlite3.connect('comments.db')

        #create cursor
        self.patc = self.patconn.cursor()
        self.comc = self.comconn.cursor()

        #create dbs if needed
        self.init_patdb()
        self.init_commentdb()

    def init_patdb(self):
        """
        Will create the patient database automatically if doesnt exist.
        """
    
        self.patc.execute(""" 
                    CREATE TABLE IF NOT EXISTS patients (
                        patnum INTEGER PRIMARY KEY AUTOINCREMENT,
                        lname text,
                        fname text,
                        age text,
                        weight text,
                        height text,
                        bloodtype text,
                        sex text,
                        UNIQUE (lname, fname, age, weight, height, bloodtype, sex)
                        );

                            
                
                """)

    def init_commentdb(self):
        """
        Will create the comments database automatically if doesnt exist.
        """

        self.comc.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patnum integer,
                comment text,
                date_time text,
                FOREIGN KEY (patnum) 
                    REFERENCES patients(patnum)
                )


                """)
        
    def add_db(self, pat):
        """
        Add patient to patients.db

        pat: patient object
        """
        with self.patconn:
                self.patc.execute("INSERT OR REPLACE INTO patients VALUES (:patnum, :lname, :fname, :age, :weight, :height, :bloodtype, :sex)", 
            {
                'patnum': None,
                'lname': pat.lname,
                'fname': pat.fname,
                'age': pat.age,
                'weight': pat.weight,
                'height': pat.height,
                'bloodtype': pat.bloodtype, 
                'sex': pat.sex
                }
                )

    def search_by_lname(self, lname):
        """
        Search by name.

        lname: string
        """
        with self.patconn:
                self.patc.execute("SELECT * FROM patients WHERE lname =:lname", {'lname': lname})
                return self.patc.fetchall()

    def search_by_patnum(self, num):
        """
        Search by patient number.

        num: string
        """
        with self.patconn:
            self.patc.execute("SELECT * FROM patients WHERE patnum =:patnum", {'patnum': num})
            return self.patc.fetchall()

    def get_patnum(self):
        """
        Will find the maximum pat number, if none will start the list with 1. 
        It is independent of the SQL autokey so that if a patient is deleted it will not change the patient numbers.
        """
        with self.patconn:
            self.patc.execute('SELECT MAX(patnum) AS maximum FROM patients')
            result = self.patc.fetchall()
            if result[0][0] == None:
                return '1'
            else:
                return str(int(result[0][0]) + 1)

    def get_all_pats(self):
        """
        Will retrieve all patietents from the database
        """
        with self.patconn:
            self.patc.execute("""SELECT patnum, lname, fnamefrom patients """)
            result = self.patc.fetchall()
            return result

    def get_all_comments(self, num):
        """
        Retrieve all comments from the linked comment database
        num: a string of the patient number.
        """
        with self.comconn:
            self.comc.execute("""SELECT comment, date_time FROM patients WHERE patnum =:patnum""", {'patnum': num})

    def write_comment(self, comment, num):
        """
        Will write a comment to the database and automatically time stamp it. 
        comment: a string.
        num: patient number as a string.
        """
        now = datetime.datetime.now()
        # print(f"""----------{now.month}/{now.day}/{now.year} {now.hour}:{now.minute}----------\n {comment}""")
        with self.comconn:
            self.comc.execute("INSERT INTO comments ( comment, patnum, date_time) VALUES (:comment, :patnum, :datetime)",
            {
                'comment': comment,
                'patnum': num,
                'date_time': f"{now.month}/{now.day}/{now.year} {now.hour}:{now.minute}"
            }
            )
