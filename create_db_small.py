import sqlite3 as sql
conn = sql.connect('class_schedule_2.db')
c = conn.cursor()
c.execute("""create table classroom (number text, capacity integer)""")
c.execute("insert into classroom Values ('R1', 25),"
                                  "('R2', 45),"
                                  "('R3', 35),"
                                  "('R4', 40)")
c.execute("""create table timeslot (id text, time text)""")
c.execute("insert into timeslot Values ('TS1', 'MW 09:30 - 10:45'),"
                                          "('TS2', 'MW 11:00 - 12:15'),"
                                          "('TS3', 'TR 09:30 - 10:45'),"
                                          "('TS4', 'TR 11:00 - 12:15')")
c.execute("""create table instructor (number text, name text)""")
c.execute("insert into instructor Values ('I1', 'Dr. Ahmed'),"
                                        "('I2', 'Dr. Mariam'),"
                                        "('I3', 'Dr. Amna'),"
                                        "('I4', 'Dr. Faisal'),"
                                        "('I5', 'Dr. Sara')")
c.execute("""create table course_instructor (course_number text, instructor_number text)""")
c.execute("insert into course_instructor Values ('C1', 'I1'),"
                                               "('C1', 'I2'),"
                                               "('C2', 'I1')," 
                                               "('C2', 'I2')," 
                                               "('C2', 'I3')," 
                                               "('C3', 'I1'),"
                                               "('C3', 'I2'),"
                                               "('C4', 'I3'),"
                                               "('C4', 'I4'),"
                                               "('C5', 'I4'),"
                                               "('C6', 'I1'),"
                                               "('C6', 'I3'),"
                                               "('C7', 'I2'),"
                                               "('C7', 'I4'),"
                                               "('C8', 'I5'),"
											   "('C9', 'I5'),"
											   "('C10','I1'),"
											   "('C10','I2')")
c.execute("""create table course (number text, name text, max_numb_of_students)""")
c.execute("insert into course Values ('C1', 'ESMA603', 25),"
                                    "('C2', 'ECCE610', 35)," 
                                    "('C3', 'ESMA610', 25),"
                                    "('C4', 'ECCE635', 30),"
                                    "('C5', 'ECCE673', 35),"
                                    "('C6', 'MEEN601', 45),"
                                    "('C7', 'MEEN613', 45),"
                                    "('C8', 'COSC604', 30),"
                                    "('C9', 'COSC606', 40),"
								    "('C10','ESMA617', 40)")


c.execute("""create table student_group (name text)""")
c.execute("insert into student_group Values ('ESM'),"
                                  "('ECE'),"
                                  "('ME'),"
                                  "('CS')")
c.execute("""create table student_group_course (name text, class_numb text)""")
c.execute("insert into student_group_course Values ('ESM', 'C1'),"
                                         "('ECE',  'C2'),"
                                         "('ESM', 'C3'),"
                                         "('ECE',  'C4'),"
                                         "('ECE',  'C5'),"
                                         "('ME',  'C6'),"
                                         "('ME',  'C7'),"
                                         "('CS',  'C8'),"
                                         "('CS',  'C9'),"
                                         "('ESM', 'C10')")
conn.commit()
c.close()
conn.close()