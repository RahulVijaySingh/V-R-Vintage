# bar graph

import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'output_flat_keywords_with_sentiment - Copy.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Convert 'Post_Date' to datetime
df['Post_Date'] = pd.to_datetime(df['Post_Date'], errors='coerce')

# Normalize 'Location' column
df['Location'] = df['Location'].astype(str).str.lower()

# Corrected keyword extraction function
def extract_location(text):
    if 'ecr' in text:
        return 'ecr'
    elif 'omr' in text:
        return 'omr'
    elif 'gst' in text:
        return 'gst'
    else:
        return None

df['Detected_Location'] = df['Location'].apply(extract_location)

# Filter only rows with valid locations
df = df[df['Detected_Location'].notnull()]

# Define quarter classification
def classify_quarter(date):
    if pd.isnull(date):
        return None
    if date >= pd.Timestamp('2025-04-01'):
        return 'Q6'
    elif date >= pd.Timestamp('2025-01-01'):
        return 'Q5'
    elif date >= pd.Timestamp('2024-10-01'):
        return 'Q4'
    elif date >= pd.Timestamp('2024-07-01'):
        return 'Q3'
    elif date >= pd.Timestamp('2024-04-01'):
        return 'Q2'
    elif date >= pd.Timestamp('2024-01-01'):
        return 'Q1'
    else:
        return None

df['Quarter'] = df['Post_Date'].apply(classify_quarter)

# Count posts per quarter and location
quarter_location_counts = df.groupby(['Quarter', 'Detected_Location']).size().unstack(fill_value=0)

# Ensure all quarters are represented
quarters_order = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']
quarter_location_counts = quarter_location_counts.reindex(quarters_order, fill_value=0)

# Plotting
quarter_location_counts.plot(kind='bar', figsize=(10, 6))
plt.title('Number of Demands by Location per Quarter')
plt.xlabel('Quarter')
plt.ylabel('Demands')
plt.xticks(rotation=0)
plt.legend(title='Location')
plt.grid(axis='y')
plt.tight_layout()
plt.show()




# import pandas as pd
# import matplotlib.pyplot as plt

# # Load the Excel file
# file_path = 'output_flat_keywords_with_sentiment - Copy.xlsx'
# df = pd.read_excel(file_path, sheet_name='Sheet1')

# # Convert 'Post_Date' to datetime
# df['Post_Date'] = pd.to_datetime(df['Post_Date'], errors='coerce')

# # Normalize 'Location' column
# df['Location'] = df['Location'].astype(str).str.lower()

# # Extract simplified location
# def extract_location(text):
#     if 'ecr' in text:
#         return 'ecr'
#     elif 'omr' in text:
#         return 'omr'
#     elif 'gst' in text:
#         return 'gst'
#     else:
#         return None

# df['Detected_Location'] = df['Location'].apply(extract_location)

# # Filter rows with valid detected locations
# df = df[df['Detected_Location'].notnull()]

# # Classify into quarters
# def classify_quarter(date):
#     if pd.isnull(date):
#         return None
#     if date >= pd.Timestamp('2025-04-01'):
#         return 'Q6'
#     elif date >= pd.Timestamp('2025-01-01'):
#         return 'Q5'
#     elif date >= pd.Timestamp('2024-10-01'):
#         return 'Q4'
#     elif date >= pd.Timestamp('2024-07-01'):
#         return 'Q3'
#     elif date >= pd.Timestamp('2024-04-01'):
#         return 'Q2'
#     elif date >= pd.Timestamp('2024-01-01'):
#         return 'Q1'
#     else:
#         return None

# df['Quarter'] = df['Post_Date'].apply(classify_quarter)

# # Group and count posts by quarter and location
# quarter_location_counts = df.groupby(['Quarter', 'Detected_Location']).size().unstack(fill_value=0)

# # Ensure all quarters are present
# quarters_order = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']
# quarter_location_counts = quarter_location_counts.reindex(quarters_order, fill_value=0)

# # Plot the line chart
# quarter_location_counts.plot(kind='line', marker='o', figsize=(10, 6))

# plt.title('Number of Demands by Location per Quarter')
# plt.xlabel('Quarter')
# plt.ylabel('Demands')
# plt.xticks(rotation=0)
# plt.grid(True)
# plt.legend(title='Location')
# plt.tight_layout()
# plt.show()