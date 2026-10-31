import docx
import shutil
import os
from weekly_report_builder import TEMPLATE_PATH, WEEKLY_DATA, build_weekly_report_section

OUTPUT_PATH_1 = r"d:\AI INTERNSHIP\Summer_Internship_Weekly_Reports_Week1_to_6.docx"
OUTPUT_PATH_DOWNLOADS_1 = r"C:\Users\Himanshu Pathak\Downloads\Summer_Internship_Weekly_Reports_Week1_to_6.docx"

# Load the original template so headers and logos are preserved
doc = docx.Document(TEMPLATE_PATH)

# Clear body elements except the last sectPr
body = doc._element.body
for child in list(body)[:-1]:
    body.remove(child)

# Now add all 6 weeks
for idx, data in enumerate(WEEKLY_DATA):
    build_weekly_report_section(doc, data, is_first=(idx == 0))

# Save document
doc.save(OUTPUT_PATH_1)
shutil.copy(OUTPUT_PATH_1, OUTPUT_PATH_DOWNLOADS_1)
print(f"Document 1 successfully saved to:\n1. {OUTPUT_PATH_1}\n2. {OUTPUT_PATH_DOWNLOADS_1}")
