"""Add comprehensive campus complaints covering facility acronyms, natural phrasing, and classroom amenities."""

import pandas as pd

targeted_samples = [
    # Classroom facility & AC complaints
    ("Need AC in class", "Classroom"),
    ("Theres no AC in our class, please put it fast", "Classroom"),
    ("There is no AC in our classroom, please install it", "Classroom"),
    ("No AC in room 214, very hot inside", "Classroom"),
    ("AC is not working in the classroom", "Classroom"),
    ("Classroom AC stopped working during lecture", "Classroom"),
    ("The AC in room 302 is broken and leaking water", "Classroom"),
    ("Need new fan and AC in computer science class", "Classroom"),
    ("Fans and lights are not working in classroom 105", "Classroom"),
    ("Air conditioning unit in classroom 204 is blowing warm air", "Classroom"),
    ("Classroom 101 has no AC and suffocating heat during afternoon lecture", "Classroom"),
    ("Please fix the AC and fan in class BE Comps", "Classroom"),
    ("Classroom projector, AC, and mic are out of order", "Classroom"),
    ("No air conditioner or fan in lecture room 405", "Classroom"),
    ("Classroom desks and benches are broken", "Classroom"),
    ("Whiteboard markers and duster missing in room 208", "Classroom"),

    # Infrastructure facility
    ("AC in central auditorium is making loud noise", "Infrastructure"),
    ("Building main power generator is not turning on during power cuts", "Infrastructure"),
    ("Restroom flush and taps have no water on 2nd floor", "Infrastructure"),
    ("Main hallway ceiling is leaking dirty rainwater", "Infrastructure"),
    ("Elevator in academic block is stuck and not operational", "Infrastructure"),

    # IT & Wi-Fi
    ("Campus Wi-Fi is down in computer lab", "IT & Wi-Fi"),
    ("No internet connection or wifi in room 214", "IT & Wi-Fi"),
    ("College student portal login is failing", "IT & Wi-Fi"),
    ("Lab computer keyboards and mice are not working", "IT & Wi-Fi"),

    # Academics
    ("Professor is not taking lectures on time", "Academics"),
    ("Data structures syllabus is not completed by faculty", "Academics"),
    ("Lab practical assistant is unhelpful during coding session", "Academics"),
    ("Internal assessment assignment marks are not shared", "Academics"),
]

df = pd.read_csv('data/complaints_dataset.csv')
new_rows = pd.DataFrame(targeted_samples, columns=['text', 'category'])
updated_df = pd.concat([df, new_rows], ignore_index=True).drop_duplicates(subset=['text'])
updated_df.to_csv('data/complaints_dataset.csv', index=False)
print(f"Total dataset size: {len(updated_df)} samples.")
