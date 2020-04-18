# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 21:54:22 2020

@author: Ankit
"""

from flask import Flask, render_template
import sqlite3
from typing import Dict

app: Flask = Flask(__name__)

db_path = "C:/sqlite/810_startup.db"

@app.route('/')

def student_details():

    query = "select s.Name as Name, s.CWID, g.Course, g.Grade, i.Name as Instructor from students s, grades g, instructors i where s.CWID = g.StudentCWID and i.CWID = g.InstructorCWID order by s.Name"
    db: sqlite3.Connection = sqlite3.connect(db_path)
    result = db.execute(query)

    data: Dict[str, str] = [{ "name": name, "cwid": cwid, "course": course, "grade": grade, "instructor": instructor}
			                for name, cwid, course, grade, instructor in result]
    db.close()

    return render_template('student_details.html',
                            my_header = "Stevens Repository",
                            my_param = "Students Details",
                            students = data)

app.run(debug=True)