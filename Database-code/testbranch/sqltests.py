import sqlite3

class Patient(object):
    """
    A Patient is a person who has come to see the doctor.
    they have name, age, weight, height, gender
    """

    def __init__(self, lname, fname, age, weight, height, bloodtype, sex):
        """
        Initializes a patient with patient number, last name, firstname, age, weight, height, bloodtype
        """
        
        #self.patnum = patnum
        self.lname = lname.capitalize()
        self.fname = fname.capitalize()
        self.age = age
        self.weight = weight
        self.height = height
        self.bloodtype = bloodtype
        self.sex = sex

def insert_pat(pat):
    try:
        with conn:
            c.execute("INSERT INTO patients VALUES (:fname, :lname, :age, :weight, :height, :bloodtype, :sex)", 
            {'lname': pat.lname, 'fname': pat.fname, 'age': pat.age, 'weight': pat.weight, 'height': pat.height, 'bloodtype': pat.bloodtype, 'sex': pat.sex})
    except sqlite3.IntegrityError:
        print('duplicate entry')




conn = sqlite3.connect('patients.db')

#create cursor
c = conn.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS patients (
                lname text,
                fname text,
                age text,
                weight text,
                height text,
                bloodtype text,
                sex text,
                UNIQUE (lname, fname, age, weight, height, bloodtype, sex)
)""")



pat1 = Patient('bezos', 'jeff', '24', '60.3', '160', 'A+', 'M')
insert_pat(pat1)

c.execute('SELECT * FROM patients')
print(c.fetchall())
conn.commit()
conn.close()