select Name from students where CWID = 10115

select Major, count(Name) as Total_Student from students group by Major

select Grade, count(Grade) as Total_cnt from grades where Course = 'SSW 810'
    group by Grade order by Total_cnt desc limit 1

select distinct s.Name, s.CWID, count(g.Course) as Total_Course from students s join grades g on
    s.CWID = g.StudentCWID group by g.StudentCWID

select s.Name as Name, s.CWID, g.Course, g.Grade, i.Name as Instructor from students s, grades g, instructors i
    where s.CWID = g.StudentCWID and i.CWID = g.InstructorCWID order by s.Name