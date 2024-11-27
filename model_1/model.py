from pulp import LpMaximize, LpProblem, LpVariable, lpSum

import random

import random

auditoriums = [
    'Acad Block A-1', 'Acad Block A-10', 'Acad Block A-11', 'Acad Block A-12', 
    'Acad Block A-14', 'Acad Block A-15', 'Acad Block A-16', 'Acad Block A-2', 
    'Acad Block A-3', 'Acad Block A-4', 'Acad Block A-5', 'Acad Block A-6', 
    'Acad Block A-7', 'Acad Block A-8', 'Acad Block A-9', 
    'Acad Block MCB Acad Block A-13', 'Acad Block SS', 'LAB-1', 
    'LAW-FACLOU', 'Lib Bldg SOE 01', 'Lib Bldg SOE 02', 'Lib Bldg SOE 03', 
    'Lib Bldg SOE 04', 'SAHSOL ARDCR 0-07', 'SAHSOL CR 1-01', 
    'SAHSOL CR 1-06', 'SAHSOL CR 1-07', 'SAHSOL CR 2-01', 'SAHSOL CR 2-02', 
    'SAHSOL CR 2-06', 'SAHSOL CR 2-07', 'SAHSOL GHKCR 0-02', 
    'SAHSOL MMACR 1-02', 'SAHSOL SBACR 0-01', 'SAHSOL SIACR 0-06', 
    'SBASSE 10-201', 'SBASSE 10-202', 'SBASSE 10-204', 'SBASSE 10-301', 
    'SBASSE 10-302', 'SBASSE 10-304', 'SBASSE 9-B2', 'SBASSE PRGST', 
    'SDSB 101', 'SDSB 102', 'SDSB 103', 'SDSB 104', 'SDSB 105', 'SDSB 106', 
    'SDSB 201', 'SDSB 203', 'SDSB 204', 'SDSB 205', 'SDSB 305', 'SDSB B-1', 
    'SDSB B-2', 'SDSB B-3', 'SDSB TRDLB'
]

auditorium_capacities = {aud: random.randint(30, 200) for aud in auditoriums}


# Data (Simplified Example)
courses = [
    {"code": "ACCT 100", "section": "LEC 1", "days": "TR", "start": "11:00AM", "end": "12:15PM", "instructor": "Syed Zain ul Abidin"},
    {"code": "ACCT 100", "section": "LEC 2", "days": "TR", "start": "12:30PM", "end": "1:45PM", "instructor": "Syed Zain ul Abidin"},
    {"code": "ACCT 100", "section": "LEC 3", "days": "TR", "start": "2:00PM", "end": "3:15PM", "instructor": "Syed Zain ul Abidin"},
    {"code": "ACCT 100", "section": "LEC 4", "days": "TR", "start": "3:30PM", "end": "4:45PM", "instructor": "Zainab Mehmood"},
    {"code": "ACCT 100", "section": "LEC 5", "days": "TR", "start": "5:00PM", "end": "6:15PM", "instructor": "Zainab Mehmood"},
    {"code": "ACCT 100", "section": "LEC 6", "days": "MW", "start": "9:30AM", "end": "10:45AM", "instructor": "Saira Rizwan"},
    {"code": "ACCT 100", "section": "LEC 7", "days": "MW", "start": "11:00AM", "end": "12:15PM", "instructor": "Saira Rizwan"},
    {"code": "ACCT 130", "section": "LEC 1", "days": "TR", "start": "9:30AM", "end": "10:45AM", "instructor": "Ayesha Bhatti"},
    {"code": "ACCT 130", "section": "LEC 2", "days": "TR", "start": "11:00AM", "end": "12:15PM", "instructor": "Ayesha Bhatti"},
    {"code": "ACCT 130", "section": "LEC 3", "days": "TR", "start": "2:00PM", "end": "3:15PM", "instructor": "Ayesha Bhatti"}
]


# Restricted Time Slots
restricted_slots = [
    {"day": "Thursday", "start": "5:30PM", "end": "6:30PM"},
    {"day": "All", "start": "6:00AM", "end": "6:30AM"},
    {"day": "All", "start": "1:30PM", "end": "2:00PM"},
    {"day": "All", "start": "3:45PM", "end": "4:15PM"},
    
    {"day": "All", "start": "5:03PM", "end": "5:33PM"},
    {"day": "All", "start": "7:00PM", "end": "7:30PM"},
    {"day": "Friday", "start": "1:30PM", "end": "2:00PM"}
]


# LP Problem
model = LpProblem("Class_Scheduling", LpMaximize)

# Decision Variables
x = LpVariable.dicts("schedule", [(c["code"], aud, c["start"]) for c in courses for aud in auditoriums], cat='Binary')

# Objective: Minimize classes in restricted slots
restricted_time_penalty = 10
model += lpSum(restricted_time_penalty * x[(c["code"], aud, c["start"])] 
               for c in courses 
               for aud in auditoriums 
               if any(c["start"] in slot["start"] for slot in restricted_slots))

# Constraints
# 1. Each class must be scheduled exactly once
for c in courses:
    model += lpSum(x[(c["code"], aud, c["start"])] for aud in auditoriums) == 1

# 2. No overlap in auditoriums
for aud in auditoriums:
    for time in set(c["start"] for c in courses):
        model += lpSum(x[(c["code"], aud, time)] for c in courses if c["start"] == time) <= 1

# 3. Auditorium capacity constraint
for c in courses:
    for aud in auditoriums:
        if len(courses) <= auditorium_capacities[aud]:  # Assuming course size is available
            model += x[(c["code"], aud, c["start"])] <= 1

# Solve the model
model.solve()

# Print Results
for c in courses:
    for aud in auditoriums:
        if x[(c["code"], aud, c["start"])].value() == 1:
            print(f"Class {c['code']} is scheduled in Auditorium {aud} at {c['start']}")
