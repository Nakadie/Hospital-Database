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
        
        self.lname = lname.capitalize()
        self.fname = fname.capitalize()
        self.age = age
        self.weight = weight
        self.height = height
        self.bloodtype = bloodtype
        self.sex = sex

def insert_pat(pat):
    with conn:
            c.execute("INSERT OR REPLACE INTO patients VALUES (:fname, :lname, :age, :weight, :height, :bloodtype, :sex)", 
            {'lname': pat.lname,
             'fname': pat.fname,
             'age': pat.age,
             'weight': pat.weight,
             'height': pat.height,
             'bloodtype': pat.bloodtype, 
             'sex': pat.sex}
             )




conn = sqlite3.connect('patients.db')

#create cursor
c = conn.cursor()




c.execute('DELETE FROM patients WHERE patnum=2')
c.execute("""SELECT patnum, lname, fname
            from patients
""")
all = c.fetchall()
print(all)
conn.commit()
conn.close()