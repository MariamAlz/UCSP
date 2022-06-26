import sqlite3 as sqlite
import prettytable as prettytable
import random as rnd
POPULATION_SIZE = 20
NUM_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1
class DBMgr:
    def __init__(self):
        self._conn = sqlite.connect('class_schedule_2.db')
        self._c = self._conn.cursor()
        self._classrooms = self.select_classrooms()
        self._timeslots = self.select_timeslots()
        self._instructors = self.select_instructors()
        self._courses = self.select_courses()
        self._student_groups = self.select_student_groups()
        self._numberOfClasses = 0
        for i in range(0, len(self._student_groups)):
            self._numberOfClasses += len(self._student_groups[i].get_courses())
    def select_classrooms(self):
        self._c.execute("SELECT * FROM classroom")
        classrooms = self._c.fetchall()
        returnClassrooms = []
        for i in range(0, len(classrooms)):
            returnClassrooms.append(Classroom(classrooms[i][0], classrooms[i][1]))
        return returnClassrooms
    def select_timeslots(self):
        self._c.execute("SELECT * FROM timeslot")
        timeslots = self._c.fetchall()
        returnTimeslots = []
        for i in range(0, len(timeslots)):
            returnTimeslots.append(Timeslot(timeslots[i][0], timeslots[i][1]))
        return returnTimeslots
    def select_instructors(self):
        self._c.execute("SELECT * FROM instructor")
        instructors = self._c.fetchall()
        returnInstructors = []
        for i in range(0, len(instructors)):
            returnInstructors.append(Instructor(instructors[i][0], instructors[i][1]))
        return returnInstructors
    def select_courses(self):
        self._c.execute("SELECT * FROM course")
        courses = self._c.fetchall()
        returnCourses = []
        for i in range(0, len(courses)):
            returnCourses.append(
                Course(courses[i][0], courses[i][1], self.select_course_instructors(courses[i][0]), courses[i][2]))
        return returnCourses
    def select_student_groups(self):
        self._c.execute("SELECT * FROM student_group")
        student_groups = self._c.fetchall()
        returnStudentGroups = []
        for i in range(0, len(student_groups)):
            returnStudentGroups.append(Department(student_groups[i][0], self.select_student_group_courses(student_groups[i][0])))
        return returnStudentGroups
    def select_course_instructors(self, courseNumber):
        self._c.execute("SELECT * FROM course_instructor where course_number == '" + courseNumber + "'")
        dbInstructorNumbers = self._c.fetchall()
        instructorNumbers = []
        for i in range(0, len(dbInstructorNumbers)):
            instructorNumbers.append(dbInstructorNumbers[i][1])
        returnValue = []
        for i in range(0, len(self._instructors)):
           if  self._instructors[i].get_id() in instructorNumbers:
               returnValue.append(self._instructors[i])
        return returnValue
    def select_student_group_courses(self, studentGroupName):
        self._c.execute("SELECT * FROM student_group_course where name == '" + studentGroupName + "'")
        dbCourseNumbers = self._c.fetchall()
        courseNumbers = []
        for i in range(0, len(dbCourseNumbers)):
            courseNumbers.append(dbCourseNumbers[i][1])
        returnValue = []
        for i in range(0, len(self._courses)):
           if self._courses[i].get_number() in courseNumbers:
               returnValue.append(self._courses[i])
        return returnValue
    def get_classrooms(self): return self._classrooms
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_student_groups(self): return self._student_groups
    def get_timeslots(self): return self._timeslots
    def get_numberOfClasses(self): return self._numberOfClasses
class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes
    def get_numbOfConflicts(self): return self._numbOfConflicts
    def get_fitness(self):
        if (self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness
    def initialize(self):
        student_groups = self._data.get_student_groups()
        for i in range(0, len(student_groups)):
            courses = student_groups[i].get_courses()
            for j in range(0, len(courses)):
                newClass = Class(self._classNumb, student_groups[i], courses[j])
                self._classNumb += 1
                newClass.set_timeslot(data.get_timeslots()[rnd.randrange(0, len(data.get_timeslots()))])
                newClass.set_classroom(data.get_classrooms()[rnd.randrange(0, len(data.get_classrooms()))])
                newClass.set_instructor(courses[j].get_instructors()[rnd.randrange(0, len(courses[j].get_instructors()))])
                self._classes.append(newClass)
        return self
    def calculate_fitness(self):
        self._numbOfConflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            if (classes[i].get_classroom().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._numbOfConflicts += 1
            for j in range(0, len(classes)):
                if (j >= i):
                    if (classes[i].get_timeslot() == classes[j].get_timeslot() and
                    classes[i].get_id() != classes[j].get_id()):
                        if (classes[i].get_classroom() == classes[j].get_classroom()): self._numbOfConflicts += 1
                        if (classes[i].get_instructor() == classes[j].get_instructor()): self._numbOfConflicts += 1
        return 1 / ((1.0 * self._numbOfConflicts + 1))
    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes) - 1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes) - 1])
        return returnValue
class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0, size): self._schedules.append(Schedule().initialize())
    def get_schedules(self): return self._schedules
class GeneticAlgorithm:
    def evolve(self, population): return self._mutate_population(self._crossover_population(population))
    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUM_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUM_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop
    def _mutate_population(self, population):
        for i in range(NUM_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population
    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if (rnd.random() > 0.5): crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else: crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule
    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(0, len(mutateSchedule.get_classes())):
            if(MUTATION_RATE > rnd.random()): mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule
    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop
class Course:
    def __init__(self, number, name, instructors, maxNumbOfStudents):
        self._number = number
        self._name = name
        self._maxNumbOfStudents = maxNumbOfStudents
        self._instructors = instructors
    def get_number(self): return self._number
    def get_name(self): return self._name
    def get_instructors(self): return self._instructors
    def get_maxNumbOfStudents(self): return self._maxNumbOfStudents
    def __str__(self): return self._name
class Instructor:
    def __init__(self, id, name):
        self._id = id
        self._name = name
    def get_id(self): return self._id
    def get_name(self): return self._name
    def __str__(self): return self._name
class Classroom:
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity
    def get_number(self): return self._number
    def get_seatingCapacity(self): return self._seatingCapacity
class Timeslot:
    def __init__(self, id, time):
        self._id = id
        self._time = time
    def get_id(self): return self._id
    def get_time(self): return self._time
class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses
    def get_name(self): return self._name
    def get_courses(self): return self._courses
class Class:
    def __init__(self, id, student_group, course):
        self._id = id
        self._student_group = student_group
        self._course = course
        self._instructor = None
        self._timeslot = None
        self._classroom = None
    def get_id(self): return self._id
    def get_student_group(self): return self._student_group
    def get_course(self): return self._course
    def get_instructor(self): return self._instructor
    def get_timeslot(self): return self._timeslot
    def get_classroom(self): return self._classroom
    def set_instructor(self, instructor): self._instructor = instructor
    def set_timeslot(self, timeslot): self._timeslot = timeslot
    def set_classroom(self, classroom): self._classroom = classroom
    def __str__(self):
        return str(self._student_group.get_name()) + "," + str(self._course.get_number()) + "," + \
               str(self._classroom.get_number()) + "," + str(self._instructor.get_id()) + "," + str(self._timeslot.get_id())
class DisplayMgr:
    def print_available_data(self):
        print("> All Available Data")
        self.print_student_group()
        self.print_course()
        self.print_classroom()
        self.print_instructor()
        self.print_timeslots()
    def print_student_group(self):
        student_groups = data.get_student_groups()
        availableStudentGroupsTable = prettytable.PrettyTable(['student_group', 'classes'])
        for i in range(0, len(student_groups)):
            courses = student_groups.__getitem__(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableStudentGroupsTable.add_row([student_groups.__getitem__(i).get_name(), tempStr])
        print(availableStudentGroupsTable)
    def print_course(self):
        availableCoursesTable = prettytable.PrettyTable(['id', 'class #', 'max #', 'instructors'])
        courses = data.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors) - 1].__str__()
            availableCoursesTable.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_maxNumbOfStudents()), tempStr])
        print(availableCoursesTable)
    def print_instructor(self):
        availableInstructorsTable = prettytable.PrettyTable(['id', 'instructor'])
        instructors = data.get_instructors()
        for i in range(0, len(instructors)):
            availableInstructorsTable.add_row([instructors[i].get_id(), instructors[i].get_name()])
        print(availableInstructorsTable)
    def print_classroom(self):
        availableClassroomsTable = prettytable.PrettyTable(['classroom #', 'max seating capacity'])
        classrooms = data.get_classrooms()
        for i in range(0, len(classrooms)):
            availableClassroomsTable.add_row([str(classrooms[i].get_number()), str(classrooms[i].get_seatingCapacity())])
        print(availableClassroomsTable)
    def print_timeslots(self):
        availableTimeslotTable = prettytable.PrettyTable(['id', 'timeslot'])
        timeslots = data.get_timeslots()
        for i in range(0, len(timeslots)):
            availableTimeslotTable.add_row([timeslots[i].get_id(), timeslots[i].get_time()])
        print(availableTimeslotTable)
    def print_generation(self, population):
        table1 = prettytable.PrettyTable(['schedule #', 'fitness', '# of conflicts', 'classes [student group,class,classroom,instructor,timeslot]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i+1), round(schedules[i].get_fitness(),3), schedules[i].get_numbOfConflicts(), schedules[i].__str__()])
        print(table1)
    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['Course #', 'Student Group', 'Course (number, max # of students)', 'Classroom (Capacity)', 'Instructor (Id)',  'Timeslot (Id)'])
        for i in range(0, len(classes)):
            table.add_row([str(i+1), classes[i].get_student_group().get_name(), classes[i].get_course().get_name() + " (" +
                           classes[i].get_course().get_number() + ", " +
                           str(classes[i].get_course().get_maxNumbOfStudents()) +")",
                           classes[i].get_classroom().get_number() + " (" + str(classes[i].get_classroom().get_seatingCapacity()) + ")",
                           classes[i].get_instructor().get_name() +" (" + str(classes[i].get_instructor().get_id()) +")",
                           classes[i].get_timeslot().get_time() +" (" + str(classes[i].get_timeslot().get_id()) +")"])
        print(table)
data = DBMgr()
displayMgr = DisplayMgr()
displayMgr.print_available_data()
generationNumber = 0
print("\n> Generation # "+str(generationNumber))
population = Population(POPULATION_SIZE)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
displayMgr.print_generation(population)
displayMgr.print_schedule_as_table(population.get_schedules()[0])
geneticAlgorithm = GeneticAlgorithm()
while (population.get_schedules()[0].get_fitness() != 1.0):
    generationNumber += 1
    print("\n> Generation # " + str(generationNumber))
    population = geneticAlgorithm.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    displayMgr.print_generation(population)
    displayMgr.print_schedule_as_table(population.get_schedules()[0])
print("\n\n")
