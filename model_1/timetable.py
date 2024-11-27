import pandas as pd
import os

# Function to read slot times from CSV
def load_slots(file_path):
    slots_df = pd.read_csv(file_path)
    slot_dict = {}
    for _, row in slots_df.iterrows():
        slot_id = row['SlotID']
        start_time = pd.to_datetime(row['StartTime'])
        end_time = pd.to_datetime(row['EndTime'])
        slot_dict[slot_id] = pd.date_range(start_time, end_time, freq='30min', inclusive="left").strftime('%I:%M %p').tolist()
    return slot_dict

# Function to read timetable from TXT and map courses to slots and venues
def load_timetable(file_path, slot_mapping):
    timetable = {}
    current_course = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if "assigned to Slot" in line:
                current_course = line.split("Course")[1].split("is")[0].strip()
                slot = int(line.split("Slot")[1].strip())
                timetable[current_course] = {'slot': slot}
            elif "assigned to Venue" in line and current_course:
                venue = line.split("Venue")[1].strip()
                timetable[current_course]['venue'] = venue
    return timetable

# Generate the timetable matrix
def generate_timetable(timetable, slot_mapping, venues, time_intervals):
    matrix = pd.DataFrame(columns=['Venues\\Slots'] + time_intervals)
    matrix['Venues\\Slots'] = venues
    matrix.set_index('Venues\\Slots', inplace=True)

    for venue in venues:
        matrix.loc[venue] = ''
        for course, details in timetable.items():
            if details['venue'] == venue:
                slot_times = slot_mapping[details['slot']]
                for time in slot_times:
                    if time in matrix.columns:
                        matrix.loc[venue, time] = course
    return matrix

# Main execution
slots_file = 'slots.csv'
timetable_file = 'solution_TR.txt'
venues_file = 'venues.txt'

# Validate files
if not os.path.exists(slots_file):
    raise FileNotFoundError(f"File not found: {slots_file}")
if not os.path.exists(timetable_file):
    raise FileNotFoundError(f"File not found: {timetable_file}")
if not os.path.exists(venues_file):
    raise FileNotFoundError(f"File not found: {venues_file}")

# Load data
slot_mapping = load_slots(slots_file)
timetable = load_timetable(timetable_file, slot_mapping)

# Load venues
venues = []
with open(venues_file, 'r') as f:
    for line in f:
        venues.append(line.strip())

if not venues:
    raise ValueError("No venues found in 'venues.txt'. Please check the file content.")

# Define time intervals
time_intervals = [
    "8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM",
    "11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM", "2:30 PM",
    "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM"
]

# Generate timetable matrix
final_timetable = generate_timetable(timetable, slot_mapping, venues, time_intervals)

# Save to CSV
output_file = 'final_timetable.csv'
final_timetable.reset_index().to_csv(output_file, index=False)
print(f"Timetable saved to '{output_file}'")
