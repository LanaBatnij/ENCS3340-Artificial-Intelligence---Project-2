import random

Random = []
Courses = {}
Instructors = {}


def PrintCourses(Courses):
    print("%-15s %-15s %-25s %-15s %-15s %-15s" % ("Course Code", "Section", "Instructor", "Days", "Time", "Fit"))

    print("=" * 100)
    for code in Courses:
        for section in Courses[code]:
            print("%-15s %-15s %-25s %-15s %-15s %-15s" % (
                code, section, Courses[code][section][1], Courses[code][section][0], Courses[code][section][2],
                not Courses[code][section][4]), end="")
            print()
        print("-" * 100)
    print("Fitness is : " + str(Fitness(Courses)))


def RandomGenerate(Random, Courses, Instructors):
    Times = ["8:00-9:15", "8:30-9:45", "10:00-11:15", "11:25-12:40", "12:50-2:05", "2:15-3:30", "3:40-4:55"]
    TimesL = ["8:00-11:15", "11:25-2:05", "2:15-4:55"]
    Days = ["T,R", "S,M", "M,W", "S,W"]
    DaysL = ["T", "R", "S", "M", "W"]
    for a in range(1000):
        Random.append({})
        # "ENCS2110": {1: ["T,R", "Ayman", "11:25-12:40", 2, False]
        for code in Courses:
            if int(code[5])==1:
                Names = []
                T = False
                for c in Instructors:
                    for b in Instructors[c]:
                        if code == b:
                            T = True
                            Names.append(c)

                Random[a][code] = {}
                if T:
                    for i in range(1, Courses[code][0] + 1):
                        Name = random.choice(Names).split(" ")
                        Random[a][code][i] = [random.choice(DaysL), Name[0] + " " + Name[-1], random.choice(TimesL),
                                              int(Courses[code][1]), False]
            else:
                Names = []
                T = False
                for c in Instructors:
                    for b in Instructors[c]:
                        if code == b:
                            T = True
                            Names.append(c)

                Random[a][code] = {}
                if T:
                    for i in range(1, Courses[code][0] + 1):
                        Name = random.choice(Names).split(" ")
                        Random[a][code][i] = [random.choice(Days), Name[0] + " " + Name[-1], random.choice(Times),
                                              int(Courses[code][1]), False]


def Crossover(Browser1, Browser2):
    stop = False
    for a in Browser1:
        if stop:
            break
        for b in Browser1[a]:
            if stop:
                break
            if Browser1[a][b][4] == True:
                stop = True
                temp = Browser2[a][b]
                Browser2[a][b] = Browser1[a][b]
                Browser1[a][b] = temp
                Browser1[a][b][4] = False


def Mutation(Browser, Courses, Instructors):
    Times = ["8:00-9:15", "8:30-9:45", "10:00-11:15", "11:25-12:40", "12:50-2:05", "2:15-3:30", "3:40-4:55"]
    Days = ["T,R", "S,M", "M,W", "S,W"]
    DaysL = ["T", "R", "S", "M", "W"]
    TimesL = ["8:00-11:15", "11:25-2:05", "2:15-4:55"]

    stop = False
    for a in Browser:
        if stop:
            break
        Names = []
        for c in Instructors:
            for b in Instructors[c]:
                if a == b:
                    Names.append(c)
        for b in Browser[a]:
            if stop:
                break
            if Browser[a][b][4]:
                if int(a[5])==1:
                    Name = random.choice(Names).split(" ")
                    Browser[a][b] = [random.choice(Days), Name[0] + " " + Name[-1], random.choice(Times),
                                     int(Courses[a][1]), False]
                else:
                    Name = random.choice(Names).split(" ")
                    Browser[a][b] = [random.choice(DaysL), Name[0] + " " + Name[-1], random.choice(TimesL),
                                     int(Courses[a][1]), False]
                stop = True
                break


def FileReaders(Courses, Instructors):
    try:
        fileInstructor = open("Instructors.txt", "r")
    except FileNotFoundError:
        print("There is no file for Instructors")

    try:
        fileCourses = open("Courses.txt", "r")
    except FileNotFoundError:
        print("There is no file for Courses")

    while True:
        line = fileCourses.readline()
        if len(line) < 8:
            break
        line = line.split(';')
        Courses[line[0]] = [int(line[1]), int(line[2])]
    while True:
        line = fileInstructor.readline()
        if len(line) < 8:
            break
        line = line.split(';')
        Name = line[0]
        line = line[1].split(',')
        Instructors[Name] = [a.strip() for a in line]

    # print(Courses)
    # print(Instructors)
    fileCourses.close()
    fileInstructor.close()


def Fitness(Courses):
    fit = [0, ""]
    for a in Courses:
        for b in Courses[a]:
            Courses[a][b][4] = False
    for code in Courses:
        for sections in Courses[code]:
            Days = Courses[code][sections][0]
            Instructor = Courses[code][sections][1]
            time = Courses[code][sections][2]
            lastSection = list(Courses[code].items())
            while int(lastSection[-1][0]) is not sections:
                Information = sections + 1
                if (Days == Courses[code][Information][0] or (
                        Days == "S,W" and Courses[code][Information][0] == "S,M") or
                    (Days == "S,M" and Courses[code][Information][0] == "S,W")) and time == Courses[code][Information][
                    2]:
                    fit[0] += 20
                    fit[1] += "ST,"
                    Courses[code][sections][4] = True
                    Courses[code][Information][4] = True
                if (Days == Courses[code][Information][0] or (
                        Days == "S,W" and Courses[code][Information][0] == "S,M") or
                    (Days == "S,M" and Courses[code][Information][0] == "S,W")) and time == Courses[code][Information][
                    2] \
                        and Instructor == Courses[code][Information][1]:
                    fit[0] += 40
                    fit[1] += "SI,"
                    Courses[code][Information][4] = True
                    Courses[code][sections][4] = True
                sections = sections + 1
    for code in Courses:
        lastCode = list(Courses.items())

        for sections in Courses[code]:
            Days = Courses[code][sections][0]
            Instructor = Courses[code][sections][1]
            time = Courses[code][sections][2]
            level = int(Courses[code][sections][3])

            nextCode = False
            for code2 in Courses:
                if code2 != code and not nextCode:
                    continue
                if not nextCode:
                    nextCode = True
                    continue
                for sections2 in Courses[code2]:
                    Days2 = Courses[code2][sections2][0]
                    Instructor2 = Courses[code2][sections2][1]
                    time2 = Courses[code2][sections2][2]
                    level2 = int(Courses[code2][sections2][3])
                    if Courses[code2][sections2] is not Courses[code][sections]:
                        if int(code[5])==1 or int(code2[5])==1:
                            if (Days == Days2 ) and time == time2 \
                                    and Instructor == Instructor2 and level == level2:

                                fit[0] += 80

                                fit[1] += "TIL,"
                                Courses[code][sections][4] = True
                                Courses[code2][sections2][4] = True
                            elif (Days == Days2 or (Days == "S,W" and Days2 == "S,M") or (
                                    Days == "S,M" and Days2 == "S,W")) and time == time2 and level == level2:
                                fit[0] += 50

                                fit[1] += "TL,"
                                Courses[code][sections][4] = True
                                Courses[code2][sections2][4] = True
                        else:
                            if (Days == Days2 or (Days == "S,W" and Days2 == "S,M") or (
                                    Days == "S,M" and Days2 == "S,W")) and time == time2 \
                                    and Instructor == Instructor2 and level == level2:

                                fit[0] += 80

                                fit[1] += "TIL,"
                                Courses[code][sections][4] = True
                                Courses[code2][sections2][4] = True
                            elif (Days == Days2 or (Days == "S,W" and Days2 == "S,M") or (
                                    Days == "S,M" and Days2 == "S,W")) and time == time2 and level == level2:
                                fit[0] += 50

                                fit[1] += "TL,"
                                Courses[code][sections][4] = True
                                Courses[code2][sections2][4] = True

                nextCode = False
    return fit


def copy(f, to):
    for a in f:
        to[a] = {}
        for b in f[a]:
            to[a][b] = []
            for c in f[a][b]:
                to[a][b].append(c)


FileReaders(Courses, Instructors)
RandomGenerate(Random, Courses, Instructors)
Min = 100000
min1 = 10000
min2 = 10000
CourseBrowser1 = {}
CourseBrowser2 = {}

best = {}
for a in range(100):
    Min = (Fitness(Random[a])[0])
    if Min < min1:
        min1 = Min
        CourseBrowser1 = Random[a]
        copy(CourseBrowser1, best)
    elif Min < min2:
        min2 = Min
        CourseBrowser2 = Random[a]
y = 0

PrintCourses(CourseBrowser1)
for x in range(10000):
    Min = (Fitness(CourseBrowser1)[0])
    if Min < min1:
        min1 = Min
        copy(CourseBrowser1, best)
    elif x % 17 == 0:
        Mutation(CourseBrowser1, Courses, Instructors)
    Crossover(CourseBrowser1, CourseBrowser2)
PrintCourses(best)
'''for a in Instructors:
    print(a + ":",end='')
    print(Instructors[a])
'''
