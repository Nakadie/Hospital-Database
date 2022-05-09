"""
This file inizilaizes the SQL database
"""
import sqlite3



conn = sqlite3.connect('patients.db')

#create cursor
c = conn.cursor()

#create table if doesnt exist
c.execute(""" 
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

c.execute("""CREATE TABLE IF NOT EXISTS comments (
                patnum integer,
                message text,
                UNIQUE (message),
                FOREIGN KEY (patnum) 
                    REFERENCES patients(patnum)
                )


""")


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

    @classmethod
    def get_all_pats(cls):
        """
        Get all the patients from the patients.db and initialize them to a class and put in a list.
        """
        c.execute('SELECT * FROM patients')
        return c.fetchall


class database(object):
    """
    Database is used to open and manipulate the sql file holding all the patient data.
    """

    def __init__(self):
        self.filename = "patients.db"

    def add_db(self, pat):
        """
        Add patient to patients.db

        pat: patient object
        """
        with conn:
                c.execute("INSERT OR REPLACE INTO patients VALUES (:patnum, :lname, :fname, :age, :weight, :height, :bloodtype, :sex)", 
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
        """
        with conn:
                c.execute("SELECT * FROM patients WHERE lname =:lname", {'lname': lname})
                return c.fetchall()

    def search_by_patnum(num):
        """
        Search by patient number.
        """
        with conn:
            c.execute("SELECT * FROM patients WHERE patnum =:patnum", {'patnum': num})
            return c.fetchall()

    def get_patnum(self):
        with conn:
            c.execute('SELECT MAX(patnum) AS maximum FROM patients')
            result = c.fetchall()
            if result[0][0] == None:
                return '1'
            else:
                return str(int(result[0][0]) + 1)

    def get_all_pats(self):
        with conn:
            c.execute("""SELECT patnum, lname, fname
            from patients
                        """)
            result = c.fetchall()
            return result

