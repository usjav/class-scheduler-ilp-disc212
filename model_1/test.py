from pulp import LpProblem, LpVariable, LpBinary, lpSum, LpMinimize

# Data
courses = {}
with open("courses.csv") as f:
    for line in f:
        course = [x.strip() for x in line.strip().split(",")]  # Strip whitespace
        if course[0] == "Course Code":  # Skip the header row
            continue
        courses[str(course[0]) + " " + str(course[1])] = {
            "Duration": float(course[2]),
            "Instructor": course[3],
            "OriginalVenue": course[4],
            "Days": course[5],
        }

slots = {}
with open("slots.csv") as f:
    for idx, line in enumerate(f):
        if idx == 0:  # Skip the header row
            continue
        slot = [x.strip() for x in line.strip().split(",")]  # Strip whitespace
        slots[str(slot[0])] = {
            "StartTime": slot[1],
            "EndTime": slot[2],
            "Duration": float(slot[3]),
        }

venues = []
with open("venues.txt") as f:
    for line in f:
        venues.append(line.strip())

# Constants
venue_penalty = 10

# Model
model = LpProblem("Course_Scheduling", LpMinimize)

# Decision Variables
valid_course_slot_pairs = [
    (course, slot)
    for course, details in courses.items()
    for slot, slot_details in slots.items()
    if details["Duration"] == slot_details["Duration"]  # Match durations
]

x = LpVariable.dicts("AssignCourseSlot", valid_course_slot_pairs, cat=LpBinary)
y = LpVariable.dicts("AssignCourseVenue", ((course, venue) for course in courses for venue in venues), cat=LpBinary)
z = LpVariable.dicts("AssignCourseSlotVenue",((course, slot, venue) for (course, slot) in valid_course_slot_pairs for venue in venues),cat=LpBinary)


# Debugging
# print(list(x.keys())[:5])
# print(list(y.keys())[:5])

# Objective Function
model += lpSum(
    venue_penalty * y[(course, venue)]
    for course in courses
    for venue in venues
    if venue != courses[course]["OriginalVenue"]
)

# Constraints
# (a) Each course is assigned to exactly one slot
for course in courses:
    model += lpSum(x[(course, slot)] for (c, slot) in valid_course_slot_pairs if c == course) == 1

# (b) Each course is assigned to exactly one venue
for course in courses:
    model += lpSum(y[(course, venue)] for venue in venues) == 1

# Linking constraints to ensure z[(course, slot, venue)] behaves like x[(course, slot)] * y[(course, venue)]
for (course, slot) in valid_course_slot_pairs:
    for venue in venues:
        model += z[(course, slot, venue)] <= x[(course, slot)]
        model += z[(course, slot, venue)] <= y[(course, venue)]
        model += z[(course, slot, venue)] >= x[(course, slot)] + y[(course, venue)] - 1

# (c) No instructor overlap in the same slot
for slot in slots:
    for instructor in set(course["Instructor"] for course in courses.values()):
        model += (
            lpSum(
                x[(course, slot)]
                for (course, s) in valid_course_slot_pairs
                if s == slot and courses[course]["Instructor"] == instructor
            )
            <= 1
        )

# Avoid venue conflicts in the same slot
for slot in slots:
    for venue in venues:
        model += (
            lpSum(z[(course, slot, venue)] for (course, s) in valid_course_slot_pairs if s == slot)
            <= 1,
            f"NoVenueConflict_{venue}_{slot}",
        )


# Solve the model
status = model.solve()

# Check if a solution was found
if status == 1:  # 1 means solution found
    print("Optimal Schedule:")
    for course in courses:
        for slot in slots:
            if (course, slot) in valid_course_slot_pairs and x[(course, slot)].value() == 1:
                print(f"Course {course} is assigned to Slot {slot}")
        for venue in venues:
            if y[(course, venue)].value() == 1:
                print(f"Course {course} is assigned to Venue {venue}")
else:
    print("No feasible solution found.")
