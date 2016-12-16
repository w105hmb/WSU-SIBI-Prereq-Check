#! /opt/local/bin/python

import pandas as pd
import numpy as np
import math
import os.path, time
import sys, re, os


# check_report is the function that can be fed a filename and prereqdict to print out prereq test results.


# Course prerequisites are defined in one of three ways that handles all cases
# All course names must be in parentheses (sorry!) ans with no spaces
# Requirements are added per examples below as
# Course definitions are inside parentheses
# Definitions of requirements are made by adding a line of the form
# Course name: (definitions),
# The comma is necessary, as are the parentheses
#
# Definitions:
# A single course definition required is simply listed, for example
#       "ME2700"
# A list of multiple required courses is in square brackets, for example
#       ["ME1020", "ME2120"]
# Multiple methods of satisfying the requirement are created by multiple
# lists, each in square brackets.
# For instance, consider a situation where both ME1010 and ME 2120 are
# required for ME 2700. This is listed as
#       "ME2700":(["CHM1210","PHY2400"]),
# On the other hand, if either is sufficient, then they are listed instead as
#       "ME2700":(["CHM1210"],["PHY2400"]),
# Here the code will go through each list to see if is is satisfied.
# In the scenario where prerequisites can be satisfied by a single course or
# Two other courses, they must be definined as two separate lists, even though
# one of the lists is a list of length 1.
# Let's consider a complicated example, ME2120. In that case, the prerequisites are
# (EGR1010 or MTH2310) and ME1040 and PHY2400
# This construc really means that there are two possible solutions,
# EGR1010, ME1040 and PHY2400 or MTH2310, ME1040 and PHY2400
# This is written as
#       "ME2120":(["EGR1010", "ME1040", "PHY2400"],["MTH2310", "ME1040", "PHY2400"]),



prereqdict = {"ME1020":("EGR1010"),
              "ME2120":(["EGR1010", "ME1040", "PHY2400"],[ "MTH2310", "ME1040", "PHY2400"]), # Verified Aug-15-2016
              "ME2210":(["ME1020", "ME2120"]), # Verified Aug-15-2016
              "ME2600":("ME2700c"), # This is a pre or co requisite. How to code?
              "ME2700":(["CHM1210","PHY2400"]), # Recitation is a co-requisite
              "ME3120":("ME1020","ME2120"), # Verified Aug-15-2016
              "ME3210":(["EE2010","ME2210","ME3120","ME3350","MTH2350"]), # Verified Aug-16-2016
              "ME3310":(["EGR1010","MTH2310","ME2120"]),
              "ME3320":(["ME1020","ME3310"]), # Verified Aug-16-2016
              "ME3350":(["ME2210","ME3310"]), # Verified Aug-16-2016
              "ME3360":(["ME1020", "ME3350","MTH2350"]), # Verified Aug-15-2016
              "ME3600":(["EE2010","EGR3350","ME2120","MTH2350"]), # Verified Aug-15-2016
              "ME3750":("ME2700"), # Verified Aug-15-2016
              "ME3760":("ME3750"), # Verified Aug-15-2016
              "ME4010":(["ME3360", "ME3210"]), # Verified Aug-15-2016
              "ME4080":(["MTH2350","ME3210"],["MTH2530","ME3210"]), # Verified Aug-16-2016
              "ME4120":(["MTH2320","MTH2350","ME3120"],["MTH2320","MTH2330","MTH2530","ME3120"]), # Verified Aug-16-2016
              "ME4140":(["ME2700","ME3120"]), # Verified Aug-16-2016
              "ME4150":("ME4140"), # Verified Aug-16-2016
              "ME4160":(["ME2020","ME2210","ME3120"],["ME1040","ME2210","ME3120"]), # Verified Aug-16-2016
              "ME4180":("ME2700"), # Verified Aug-16-2016
              "ME4190":(["MTH2350", "MTH2320", "ME3350"], ["MTH2330", "MTH2530","MTH2320", "ME3350"]), # Verified Aug-16-2016
              "ME4210":("ME3210"), # Verified Aug-16-2016
              "ME4220":("ME3210"),
              "ME4240":("ME2210"), # Verified Aug-16-2016
              "ME4250":("ME2210"), # Verified Aug-16-2016
              "ME4260":(["MTH2350"],["MTH2530"]),
              "ME4330":("ME3350"), # Verified Aug-16-2016
              "ME4340":("ME3360"), # Verified Aug-16-2016
              "ME4350":("ME3350"), # Verified Aug-16-2016
              "ME4360":(["ME3320","ME3350","MTH2350"],["ME3320","ME3350","MTH2330"]), # Verified Aug-16-2016
              "ME4430":("ME3350"), # Verified Aug-16-2016
              "ME4440":("ME3350"), # Verified Aug-16-2016
              "ME4490":("ME3120"), # Verified Aug-16-2016
              "ME4520":("ME3350"), # Verified Aug-16-2016
              "ME4530":("ME3310"), # Verified Aug-16-2016
              "ME4540":("ME3360"), # Verified Aug-16-2016
              "ME4550":("ME3360"), # Verified Aug-16-2016
              "ME4560":("ME3350"), # Verified Aug-16-2016
              "ME4570":(["ME2700","ME3310"],["ME2700","ME3750"]), # Verified Aug-16-2016
              "ME4580":(["ME2700","ME3310"],["ME2700","ME3750"]), # Verified Aug-16-2016
              "ME4590":("ME3360"), # Verified Aug-16-2016
              "ME4610":(["ME3360","3600"]), # Verified Aug-16-2016
              "ME4620":(["ME2700","ME3120","ME3600"]), # Verified Aug-15-2016
              "ME4680":(["CHM1210","PHY2410"],["CHM1210","PHY1120"]), # Verified Aug-16-2016
              "ME4700":(["ME2700","MTH2320","MTH2350"]), # Verified Aug-16-2016
              "ME4720":("ME2700"), # Verified Aug-16-2016
              "ME4730":("ME2700"), # Verified Aug-16-2016
              "ME4740":(["ME2700","ME3120","ME4620"]), # Verified Aug-16-2016
              "ME4750":(["ME2600","ME2700"]), # Verified Aug-16-2016
              "ME4770":(["ME2700","ME3120"]), # Verified Aug-16-2016
              "ME4820":(["ME2700","ME3310"],["ME2700","ME3750"]), # Verified Aug-16-2016
              "ME4830":("ME2700"), # Verified Aug-16-2016
              "ME4840":(["ME2700","ME3120"]), # Verified Aug-16-2016
              "ME4850":(["ME2700","ME3310"],["ME2700","ME3750"]), # Verified Aug-16-2016
              "ME4860":(["ME2700","ME3120"]), # Verified Aug-16-2016
              "ME4870":(["ME2210"],["BME3212"],["ISE3212"]), # Verified Aug-15-2016
              "ME4880":(["ME2700","ME3310"],["ME2700","ME3750"]), # Verified Aug-16-2016
              "ME4910":(["ME2020","EGR3350","MTH2320","MTH2350","PHY2410","EE2010","ME2210","ME2700","ME3120","ME3310","ME4620c"]) }# Verified Aug-16-2016

majordict = {"ME4910": ["Mech Engineering - BSME","Materials Sci + Egr - BSMSE"],
             "ME2700":['Engineering - IECS','Materials Sci + Egr - BSMSE','Materials Sci + Egr - IECS','Materials Sci + Egr - Pre',
                           'Mathematics - BS','Mech Engineering - BSME','Mech Engineering - IECS','Mech Engineering - Pre']}
    
co_or_preqdict = {"ME2600":("ME2700")} # This co-or-prequisite is hard-coded in passed_class
    
def isC(grade):
    answer = grade == 'A' or grade == 'B' or grade =='C'
    return answer
def isD(grade):
    answer = grade == 'A' or grade == 'B' or grade =='C' or grade == 'D'
    return answer
def ispass(grade):
    answer = grade == 'A' or grade == 'B' or grade =='C' or grade == 'D'
    return answer    
def isbetterthan(grade_needed, grade_received):
    if grade_needed == 'C':
        answer = isC('grade_received')
    elif grade_needed == 'D':
        answer = isD('grade_received')
    else:
        print("Warning: Grade needed isn't a real grade: {}.".format(grade_needed))
        answer = 3
    return answer

# Check if single course was passed
def passed_class(class_name, classes_taken, course_name, data):
    '''class_name is a string of the course a student must pass to 
    complete the prerequisites. If the grade received is not sufficient, this function 
    must return a False
    course_name is the course the student is registered for. We are checking prerequisites for course_name
    '''

    co_or_preqdict = {"ME2600":("ME2700")}
    fail_text = ''
    answer = False
    shortages = ''
    if class_name in classes_taken:
        if class_name is "ME2120" or class_name is "ME3310" or class_name is "ME2700":
            answer = isC(classes_taken[class_name])
        elif course_name is "ME2600" and class_name is "ME2700":  #  I hate this hard coding of co-requisite exception. I believe it is now fixed, but this is left in just in case. 
            answer = True
        else:
            answer = isD(classes_taken[class_name])
        # will fall to this if no grade assigned, intercept corequisite exception
        if answer is False:
            if classes_taken[class_name] is 'No grade.':
                #print('Registered but has not completed {}.'.format(class_name))
                shortages = 'Registered but has not completed {}.\n'.format(class_name)
            else:
                #print('Failed {} with grade of {}'.format(class_name, classes_taken[class_name] ))
                fail_text = 'Failed {} with grade of {}\n.'.format(class_name, classes_taken[class_name] )
    elif (class_name[:class_name.find('c')] in classes_taken
              and classes_taken[class_name[:class_name.find('c')]] == '>')  or (class_name[:class_name.find('c')]
                in classes_taken and passed_class(class_name[:class_name.find('c')], classes_taken, course_name)[0], data): # corequisite taken earlier and passed?
        answer = True
    else:
        #print('Has not taken {}.'.format(class_name ))
        fail_text = 'Has not taken {}\n.'.format(class_name )
    return answer, shortages

# Check array of classes to return if all have been passed (sufficiently)
def pass_all(classes, classes_taken, course_name, data):
    '''classes is an array of all classes a student must pass to 
    complete the prerequisites. If the grade received is not sufficient in any course, this function 
    must return a False'''    
    answer = True
    short_text = ''
    for class_name in classes:
        class_answer, shortages = passed_class(class_name, classes_taken, course_name, data)
        print(answer)
        if not class_answer:
            answer = False and answer
            print('False and answer')
            print(answer)
            #print('Failed {} with grade of {}'.format(class_name, classes_taken[class_name] ))
            short_text = short_text + class_name + '- ' + classes_taken[class_name] + 'and '
        answer = answer and class_answer
    print('answer and return')
    print(answer)        
    return answer, short_text

# Check tuple of potential methods to satisfy class to see if any of them work. 
def satisfied_requirements(requirements, classes_taken, course_name, data):
    if type(requirements) is str:
        satisfied, shortages = passed_class(requirements, classes_taken, course_name, data)[0]
        shortages = requirements + '- ' + classes_taken[class_name]
    elif type(requirements) is list:
        print('list!')
        satisfied, shortages = pass_all(requirements, classes_taken, course_name, data)
        print('satisfied: {}'.format(satisfied))
        #a = input('satisfied')
    elif type(requirements) is tuple:
        satisfied = False
        short_text = ''
        for requirement in requirements:
            satisfied, shortages = satisfied_requirements(requirement, classes_taken, course_name, data)
            if satisfied is True:
                break
            else:
               short_text = short_text + ' or ' + shortages
        shortages = short_text[4:]
    print(shortages)
    return satisfied, shortages

#Check if students in class meet prerequisites, report on failures
def check_class(course_name, student_list, data, prereqs, no_transfer_data):
    print('=======================================================')
    print('=======================================================')
    print('Start report for:')
    print('Course number {}'.format(course_name))
    print('Section number {}'.format(data["CourseSectionNumber"].iloc[1][:-1]))
    print('Prerequisites are')
    print(prereqs)
    print('=======================================================\n\n')

    email_list = ''
    for student in student_list:
        #print('-------------------------------------------')
        print('Begin {}'.format(student))
        satisfied, shortages = satisfied_requirements(prereqs, data["Pre_req_dic"].loc[student], course_name, data)
        print(satisfied)
        #a = input('hello:')
        if satisfied is False:
            data.loc[student,"Pre_req_status"] = "Missing prereqs"
            print('Begin {}'.format(student))
            if student in no_transfer_data:
                print('No transfer data for {}. ************************'.format(student))

            print(student)
            print('Section number {}'.format(data["CourseSectionNumber"].loc[student][:-1]))

            #print(student)
            print('Name: {}'.format(data.loc[student,["Name"]].values[0]))
            print('Email: {}'.format(data.loc[student,["Email"]].values[0]))
            phone_number = str(data.loc[student,["PhoneNumber"]].values[0])
            phone_number = '(' + phone_number[:3] + ')' + phone_number[3:6] + '-' + phone_number[6:]
            print('Phone number: {}'.format(phone_number))
            print('Program description: {}'.format(data.loc[student,["ProgramDescription"]].values[0]))
            if isinstance(data.loc[student,["PRIMARY_ADVISOR_NAME_LFMI"]].values[0],float):# is "nan":
                print('Advisor name: {}\n'.format("No Advisor On Record"))
            else:
                print('Advisor name: {}\n'.format(data.loc[student,["PRIMARY_ADVISOR_NAME_LFMI"]].values[0]))
            print(data.loc[student].iloc[6:-1])
            print('Has:\n{}'.format(data.loc[student,["Pre_req_dic"]].values[0]))
            #data.loc[student,'Has'] = data.loc[student,["Pre_req_dic"]].values[0]
            print('Needs any of the following combinations:')
            allprereqs = ''
            if type(prereqs) is tuple:
                for idx, set in enumerate(prereqs):
                    allprereqs = allprereqs + set + ', '
                    prereqs[i] = 'and '.join([str(x) for x in prereqs[i]]) 
                    print(set)
                allprereqs = allprereqs[:-2]
                allprereqs = ', or'.join([str(x) for x in prereqs]) 
            else:
                print(prereqs)
                allprereqs = prereqs
                allprereqs = ', '.join([str(x) for x in allprereqs]) 
            print(allprereqs)
            #Put needs in excel spreadsheet
            #data.loc[student,'Needs'] = allprereqs

            email_list = email_list + ';' + data.loc[student,["Email"]].values[0] 
            print('=====================================================\n\n')
    #print(email_list[1:])
    return data


def read_prereq_report(filename):
    data = pd.read_excel(filename, header = 11, index_col = 3, skip_footer = 1, sheetname = "Page1_1",converters={'PhoneNumber':str})
    Course_Name = data["CourseGrade"].iloc[1]
    Course_Name = data["CourseGrade"].iloc[1][:Course_Name.find('-')]

    num_prereqs = 0
    keep_cols = ['Name', 'Email', 'PhoneNumber', 'ProgramDescription', 'PRIMARY_ADVISOR_NAME_LFMI', 'CourseSectionNumber']
    base_cols = len(keep_cols)
    for i, c_name in enumerate(data.columns):
        if  c_name.find("Requisite") > 0:
            keep_cols.append(c_name)
            num_prereqs = num_prereqs + 1
    num_prereqs = num_prereqs/2
    data = data[keep_cols]
    lkk = len(keep_cols)
    student_list = data.index

    while not hasattr(student_list[-1],'encode'):
        student_list = student_list[:-1]
    data = data.loc[student_list,:]
    all_preqs = []
    for student in student_list:
        pre_reqs_taken = {}
        for i in range(base_cols, base_cols + 2 * int(num_prereqs),2):
            if hasattr(data.loc[student].iloc[i], 'encode'):
                pre_req_class = data.loc[student].iloc[i][0:(data.loc[student].iloc[i].find('-->'))]
                grade_str = data.loc[student].iloc[i+1]
                if data.loc[student].iloc[i+1].find(';') == -1:
                    grade = grade_str[-1]
                else:
                    grade = grade_str[data.loc[student].iloc[i+1].find(';')-1]
                if grade is '>':
                    grade = "No grade."
                pre_reqs_taken[pre_req_class] = grade
                grade = ''
        all_preqs.append(pre_reqs_taken)
    data['Pre_req_dic'] = all_preqs

    return data, student_list, Course_Name


# Append transfered data to student record
def append_transfer(data, student_list):
    filename = "Student_prerequisite_data.xlsx"
    while True:
        try:
            transfer_data = pd.read_excel(filename, index_col = 0, skip_footer = 1)
            break
        except IOError:
            print("Oops!  Cannot find {}".format(filename))
            filename = input("Try using the full path: ")
    print('\n\n*****************************************************************************')
    print("Transfer prerequisite file last modified: %s" % time.ctime(os.path.getmtime(filename)))
    print('*****************************************************************************\n\n')

    transfer_data = pd.read_excel("Student_prerequisite_data.xlsx", index_col = 0, skip_footer = 1)
    all_preqs = []
    pre_reqs_taken = {}
    no_transfer_data = []
    for student in student_list:
        pre_reqs_taken = data['Pre_req_dic'].loc[student]
        completed_courses = []
        if student in transfer_data.keys():
            completed_courses = transfer_data[student].loc[transfer_data[student] == "Satisfied"].keys()
        else:
            no_transfer_data.append(student)

        grades = ["C"]* len(completed_courses)
        trans_classes = dict(zip(completed_courses,grades))

        if type(pre_reqs_taken) is dict and type(trans_classes) is dict:

            pre_reqs_taken.update(trans_classes)
        elif type(trans_classes) is dict:
            pre_reqs_taken = trans_classes

        all_preqs.append(pre_reqs_taken)    
    data['Pre_req_dic'] = all_preqs        

    return data, no_transfer_data

def check_majors(major_requirement, data, student_list):
    print('\n\nMajor Checking\n-----------------------------------------\n\n')
    for student in student_list:
        #print(student)
        #print(data)
        #print(data["ProgramDescription"].loc[student])
        if data.loc[student, "ProgramDescription"] not in major_requirement:
            print('{} ({}) major is {}. Must be {}.\n'.format( data["Name"].loc[student], data["Email"].loc[student], data["ProgramDescription"].loc[student], major_requirement))
            data.loc[student, "Major"] = "Wrong major"
    print('That\'s it!')
    return data

def check_report(filename, prereqdict, majordict):
    data, student_list, course_name = read_prereq_report(filename)
    prereqs = prereqdict[course_name]
    data, no_transfer_data = append_transfer(data, student_list)
    data = check_class(course_name, student_list, data, prereqs, no_transfer_data)
    if course_name in majordict:
        data = check_majors(majordict[course_name], data, student_list)
        data  = data[data.Major.notnull() and data.Pre_req_status.notnull()]
        cols = data.columns.tolist()
        cols = cols[:1] + cols[-2:] + cols[1:-2]
        data = data[cols]
                
    else:
        print(data)
        data  = data[data.Pre_req_status.notnull()]
        cols = data.columns.tolist()
        cols = cols[:1] + cols[-1:] + cols[1:-1]
        data = data[cols]

    data.sort_values(by = ('PRIMARY_ADVISOR_NAME_LFMI'))
    writer = pd.ExcelWriter(course_name + '_report.xlsx')
    data.to_excel(writer, 'Checks')
    writer.save()
    print('\a')
    return data

    
    
#! /usr/bin/env python

"Find string in file, show file name, line number, and line"

os.environ['PATH']=os.path.normpath(os.environ['PATH']+':opt.local/bin:/usr/texbin:/usr/local/bin:/usr/bin:/bin:')
str2find=sys.argv[-1]

#print(sys.argv[1])

for file in sys.argv:
    #print(file[-2:])
    if ".py" in file:
        #print(file[-2:])
        print('\n')
        #print("Ignoring {}".format(file))
    elif "Student_prerequisite_data.xlsx" in file or '~' in file:
        print('\n')
    else:
        print(file)
        print('**************')
        data = check_report(file,prereqdict, majordict)
        
        #print(data)
