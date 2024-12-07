from datetime import datetime
import pandas as pd

# Load the Google Sheets data
sheet_id = '1rpoTrB7wep7eA7MNyamobJ8ArYpNZ62iM5ufSQo75s0'
try:
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
except Exception as e:
    print(f"Failed to load Google Sheets data: {e}")
    exit()

# Initialize variables
weight = []
names = []
due_dates = []
priority = []

# Get the current time
current_time = datetime.now()

# Read and process the data from the DataFrame
try:
    for index, row in df.iterrows():
        names.append(row['Name'])
        weight.append(row['Weight'])

        # Parse the due date
        date = row['Due Date']
        try:
            due_dates.append(datetime.strptime(date, '%d/%m/%Y %H:%M'))
        except ValueError as e:
            print(f"Error parsing date for row {index + 1}: {date} - {e}")
            due_dates.append(None)  # Placeholder for invalid dates
except KeyError as e:
    print(f"Missing expected column: {e}")
    exit()

# Calculate priority scores
for i in range(len(names)):
    importance = 5  # Base importance score

    # Adjust importance based on weight
    if weight[i] == "major assessment":
        importance += 5
    elif weight[i] == "minor assessment":
        importance += 3
    else:
        importance += 1

    # Calculate days left
    if due_dates[i] is None:
        days_left = float('inf')  # Invalid dates get lowest priority
    else:
        days_left = (due_dates[i] - current_time).days

    # Adjust importance based on due date
    if days_left < 0:
        importance += 5  # Overdue tasks get extra points
    else:
        importance += max(0, 30 - days_left)  # Closer deadlines get higher priority

    # Append the calculated priority
    priority.append(importance)

# Combine tasks into a list and rank them by priority
tasks = list(zip(names, due_dates, weight, priority))
tasks.sort(key=lambda x: x[3], reverse=True)  # Sort by priority (highest first)

# Print the ranked tasks
print("Ranked Tasks:")
for task in tasks:
    print(f"Name: {task[0]}, Due Date: {task[1]}, Weight: {task[2]}, Priority: {task[3]}")

# Write to sorted.csv
with open("sorted.csv", "w") as f:
    f.write("Name,Weight,Due Date,Priority\n")
    for task in tasks:
        f.write(f"{task[0]},{task[2]},{task[1]},{task[3]}\n")

# Read sorted.csv and convert it to HTML
try:
    sd = pd.read_csv("sorted.csv")
    sd.to_html("sorted.html")
except Exception as e:
    print(f"Error processing sorted.csv: {e}")
    exit()

# Copy sorted.html to index.html
try:
    with open("sorted.html", "r", encoding="utf-8") as sorted_file:
        sorted_content = sorted_file.read()

    with open("index.html", "w", encoding="utf-8") as index_file:
        index_file.write(sorted_content)

    print("Content of sorted.html has been copied to index.html.")
except Exception as e:
    print(f"Error writing to index.html: {e}")
