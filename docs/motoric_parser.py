import pandas as pd

file_extension=".xlsx"

if file_extension == '.xlsx':
    file = pd.read_excel('motoric1.xlsx')
elif file_extension == '.csv':
    file = pd.read_csv('motoric1.csv')

columns_pattern = ['Name', 'Field_Time', 'Exertion_Index', 'Exertion_Index_Per_Minute', 'Total_Player_Load', 'Total_Distance','Standing', 'Walking', 'Jogging', 'Running', 'HSR', 'Sprint', 'Meterage_Per_Minute', 'Acceleration', 'Deceleration']

columns =[i.rstrip().replace('\xa0', ' ').replace(' (m)', '').replace(' ', '_') for i in file.columns.values.tolist()]  #remove the trash content from the string

if columns_pattern == columns:
    print("Good pattern!")
else:
    print("not equal")


print(columns)


print("=-------------")

for index, row in file.iterrows():
    for i in range(len(row)):

        selected_row = row[i].rstrip() # delete las Character '\xa0'

        if i == 0:
            if ' ' in selected_row:
                new = selected_row.split(' ')
            elif '\xa0' in selected_row:
                new = selected_row.split('\xa0')

            first_name = new[0]
            last_name = new[-1]



'''
for index, row in file.iterrows():
    print(index, row)
'''