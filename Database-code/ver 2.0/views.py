"""
This is the file for initializing all GUI elements for the database.
"""
from PySide6.QtWidgets import *
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtSql import *
import models

class MainWindow(QMainWindow):
    """
    Main window for the database. You can search or create a new patient from here.
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        # self.w = None
        self.initUI()

    def initUI(self):
        # initialize ui for main window

        self.btn1 = QPushButton("New Patient", self)
        self.btn1.move(30, 50)
        self.btn1.clicked.connect(self.goto_newpat)

        self.btn2 = QPushButton("Search", self)
        self.btn2.move(150, 50)
        self.btn2.clicked.connect(self.goto_search)

        self.btn3 = QPushButton("List All", self)
        self.btn3.move(30, 100)
        self.btn3.clicked.connect(self.list_all)
        

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle("Patient Database")
        self.show()

    def goto_newpat(self):
        """
        Open new window to create a new patient.
        """
        self.newpat = NewPatientWindow()
        self.newpat.show()

    def goto_search(self):
        """
        Open new window for searching.
        """
        self.search = SearchWindow()
        self.search.show()
    
    def list_all(self):
        """
        Lists all patients. 
        """
        self.list = PatientsList()
        self.list.show()


class NewPatientWindow(QDialog):
    """
    This "window" is a QDialog.
    It will appear as a free-floating window.
    This window will allow entry for patient data then store it in the patient class
    then save to sql database.
    """

    def __init__(self):
        super().__init__()

        self.initUI()
        self.display_pat = DisplayPatient()

    def initUI(self):

        # variables
        self.lname = QLineEdit()
        self.fname = QLineEdit()
        self.age = QSpinBox()
        self.hgt = QLineEdit()
        self.weight = QLineEdit()
        self.blood = QComboBox()
        self.patnum = str(models.database().get_patnum())
        self.sex = QComboBox()
        layout = QFormLayout()
        self.decimals = QDoubleValidator(0, 3, 3)
        self.hgt.setValidator(self.decimals)
        self.weight.setValidator(self.decimals)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)

        # Design
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle("New Patient Entry")
        self.blood.addItems(["A+", "O+", "B+", "AB+", "A-", "O-", "B-", "AB-"])
        self.sex.addItems(["Male", "Female"])

        layout.addRow(("Patient #:"), QLabel(self.patnum))
        layout.addRow(("Last Name:"), self.lname)
        layout.addRow(("First Name:"), self.fname)
        layout.addRow(("Age:"), self.age)
        layout.addRow(("Height (cm):"), self.hgt)
        layout.addRow(("Weight (kgs):"), self.weight)
        layout.addRow(("Blood Type:"), self.blood)
        layout.addRow(QLabel("Sex:"), self.sex)
        layout.addRow(self.buttonBox)

        self.buttonBox.accepted.connect(self.create_pat)
        self.buttonBox.rejected.connect(self.reject)

        self.setLayout(layout)

    def create_pat(self):
        """
        Will create a new patient object and will display the page that lists patient info.
        """
        # initialize patient.
        new_pat = models.Patient(
            
            self.lname.text(),
            self.fname.text(),
            self.age.text(),
            self.weight.text(),
            self.hgt.text(),
            self.blood.currentText(),
            self.sex.currentText()
        )
        models.database().add_db(new_pat)

        # preparing variables for next window.
        self.display_pat.patnum.setText(self.patnum)
        self.display_pat.lname.setText(self.lname.text())
        self.display_pat.fname.setText(self.fname.text())
        self.display_pat.age.setText(self.age.text())
        self.display_pat.hgt.setText(self.hgt.text())
        self.display_pat.weight.setText(self.weight.text())
        self.display_pat.blood.setText(self.blood.currentText())
        self.display_pat.sex.setText(self.sex.currentText())

        self.display_pat.show()

        self.close()


class SearchWindow(QDialog):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window.
    This window will allow you to search through all patients in the patient class.
    """

    def __init__(self):
        super().__init__()
        self.display_pat = DisplayPatient()
        self.list_search = ListSearch()

        self.initUI()

    def initUI(self):

        # Variables.
        layout = QFormLayout()
        self.lname = QLineEdit()
        self.patnum = QLineEdit()
        backbtn = QDialogButtonBox.Cancel
        self.box = QDialogButtonBox(backbtn)
        self.search1 = QPushButton("Search")
        self.search2 = QPushButton("Search")
        self.namerr = QLabel()
        self.numerr = QLabel()
        self.onlyInt = QIntValidator()
        self.patnum.setValidator(self.onlyInt)

        # Layout.
        layout.addRow("", self.namerr)
        layout.addRow(("Last Name:"), self.lname)
        layout.addRow("", self.search1)
        layout.addRow("", self.numerr)
        layout.addRow(("Patient #:"), self.patnum)
        layout.addRow("", self.search2)
        layout.addRow("", self.box)
        self.setLayout(layout)
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle("Search")

        # Reactions
        self.box.rejected.connect(self.reject)
        self.search1.clicked.connect(self.name_search)
        self.search2.clicked.connect(self.patnum_search)

    def name_search(self):
        """
        Search by name.
        Will display new window of patient info if found.
        will display a message if not.
        """
        pat = models.database().search_by_lname(str(self.lname.text()))
        
        if pat == []:
            self.namerr.setText(self.lname.text().capitalize() + ": Not Found")
        elif len(pat) == 1:
            self.display_pat.patnum.setText(str(pat[0][0]))
            self.display_pat.lname.setText(str(pat[0][1]))
            self.display_pat.fname.setText(pat[0][2])
            self.display_pat.age.setText(str(pat[0][3]))
            self.display_pat.hgt.setText(str(pat[0][5]))
            self.display_pat.weight.setText(str(pat[0][4]))
            self.display_pat.blood.setText(pat[0][6])
            self.display_pat.sex.setText(pat[0][7])
            self.display_pat.list_comments()

            self.close()
            self.display_pat.show()
        elif len(pat) > 1:
            self.close()
            self.list_search.patname.setText(str(self.lname.text()))
            self.list_search.display()
            self.list_search.show()
   

    def patnum_search(self):
        """
        Searches by patient number
        Will display new window of patient info if found.
        will display a message if not.
        """
        pat = models.database.search_by_patnum(str(self.patnum.text()))
        if pat == []:
            self.numerr.setText("Patient #" + self.patnum.text() + ": Not Found")
        elif len(pat) == 1:
            self.display_pat.patnum.setText(str(pat[0][0]))
            self.display_pat.lname.setText(str(pat[0][1]))
            self.display_pat.fname.setText(pat[0][2])
            self.display_pat.age.setText(str(pat[0][3]))
            self.display_pat.hgt.setText(str(pat[0][5]))
            self.display_pat.weight.setText(str(pat[0][4]))
            self.display_pat.blood.setText(pat[0][6])
            self.display_pat.sex.setText(pat[0][7])
            self.display_pat.list_comments()

            self.close()
            self.display_pat.show()
     


class DisplayPatient(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window.
    This window will display patient information.
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Variables.
        self.patnum = QLabel()
        self.lname = QLabel()
        self.fname = QLabel()
        self.age = QLabel()
        self.hgt = QLabel()
        self.weight = QLabel()
        self.blood = QLabel()
        self.sex = QLabel()
        self.comments = QListWidget()
        self.layout = QFormLayout()
        self.commbut = QPushButton("New Comment")
        self.comments.setWordWrap(True)
        
        
 
        

        # layout.
        self.setLayout(self.layout)
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle("Patient info")

        self.layout.addRow(("Patient #:"), self.patnum)
        self.layout.addRow(("Last Name:"), self.lname)
        self.layout.addRow(("First Name:"), self.fname)
        self.layout.addRow(("Age:"), self.age)
        self.layout.addRow(("Height (cm):"), self.hgt)
        self.layout.addRow(("Weight (kgs):"), self.weight)
        self.layout.addRow(("Blood Type:"), self.blood)
        self.layout.addRow(("Sex:"), self.sex)
        self.layout.addRow(QLabel("Patient Notes:"))
        self.layout.addRow(self.comments)
        self.layout.addRow(self.commbut)


        self.commbut.clicked.connect(self.add_comment)

    def list_comments(self):
        """
        Will list all the comments in the comments box with the most recent comment at the top of the list.
        """
        self.comments.clear()
        allcomments = models.database().get_all_comments(self.patnum.text())
        for i in reversed(range(len(allcomments))):
            self.comments.addItem(QListWidgetItem(f"""----------{allcomments[i][1]}----------\n {allcomments[i][0]}\n"""))
            

    def add_comment(self):
        """
        This will add a new box to type a comment in and send the text to the sqldb.
        """
        self.newcomm = QPlainTextEdit()
        self.addcommbut = QPushButton("Add")
        self.commbut.setEnabled(False)
        self.layout.addRow(self.newcomm)
        self.layout.addRow(self.addcommbut)
        self.addcommbut.clicked.connect(self.restore)

    def restore(self):
        """
        This will delete the extra boxes and update the comment box with the new comment.
        """
        if self.newcomm.toPlainText() != '':
            models.database().write_comment(self.newcomm.toPlainText(), self.patnum.text())
        self.layout.removeRow(self.newcomm)
        self.layout.removeRow(self.addcommbut)
        self.commbut.setEnabled(True)
        self.list_comments()
        


class PatientsList(QListWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self): 
        #Resize width and height
        self.resize(300,120)
        
        for i in models.database().get_all_pats():
            self.addItem(QListWidgetItem(f"# {i[0]} : {i[1]}, {i[2]}."))
            
        self.setWindowTitle('Patients List')
        self.itemClicked.connect(self.open_patient)

    def open_patient(self,item):
        
        listedpat = item.text()
        
        for i in listedpat.split():
            if i.isdigit() == True:
                patnum = int(i)
                break
               
        self.display_pat = DisplayPatient()        
        pat = models.database().search_by_patnum(str(patnum))
        
        #set variables for the new window
        self.display_pat.patnum.setText(str(pat[0][0]))
        self.display_pat.lname.setText(str(pat[0][1]))
        self.display_pat.fname.setText(pat[0][2])
        self.display_pat.age.setText(str(pat[0][3]))
        self.display_pat.hgt.setText(str(pat[0][5]))
        self.display_pat.weight.setText(str(pat[0][4]))
        self.display_pat.blood.setText(pat[0][6])
        self.display_pat.sex.setText(pat[0][7])
        self.display_pat.list_comments()

        self.close()
        self.display_pat.show()

class ListSearch(QListWidget):
    def __init__(self):
        super().__init__()
        
        

        #temporary solution. Further research and optimization requred. 
        self.patname = QLabel()
        
    def display(self):
        #Resize width and height
        self.resize(300,120)
        
        for i in models.database().search_by_lname(self.patname.text()):
            self.addItem(QListWidgetItem(f"# {i[0]} : {i[1]}, {i[2]}."))
            
        self.setWindowTitle('Patients List')
        self.itemClicked.connect(self.open_patient)

    def open_patient(self,item):
        self.display_pat = DisplayPatient()
        listedpat = item.text()
        
        for i in listedpat.split():
            if i.isdigit() == True:
                patnum = int(i)
                
        pat = models.database().search_by_patnum(str(patnum))
        
        self.display_pat.patnum.setText(str(pat[0][0]))
        self.display_pat.lname.setText(str(pat[0][1]))
        self.display_pat.fname.setText(pat[0][2])
        self.display_pat.age.setText(str(pat[0][3]))
        self.display_pat.hgt.setText(str(pat[0][5]))
        self.display_pat.weight.setText(str(pat[0][4]))
        self.display_pat.blood.setText(pat[0][6])
        self.display_pat.sex.setText(pat[0][7])
        self.display_pat.list_comments()

        self.close()
        self.display_pat.show()