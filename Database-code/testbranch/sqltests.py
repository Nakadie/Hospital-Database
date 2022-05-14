
import models


models.database().write_comment('here is a long list of various illnesses and issues that is causing trouble for this patient.', '1')
pats = models.database().get_all_comments('1')
for i in range(len(pats)):
    print((f"""----------{pats[i][1]}----------\n {pats[i][0]}\n"""))








