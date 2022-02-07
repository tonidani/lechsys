import pandas as pd


class ImportedFile:

    ALLOWED_EXTENSIONS = ['.xlsx', '.csv']

    columns_pattern=['Name' , 'Field_Time' , 'Exertion_Index' , 'Exertion_Index_Per_Minute' , 'Total_Player_Load' ,
                     'Total_Distance' , 'Standing' , 'Walking' , 'Jogging' , 'Running' , 'HSR' , 'Sprint' ,
                     'Meterage_Per_Minute' , 'Acceleration' , 'Deceleration']

    file = ''

    @staticmethod
    def check_if_valid_structure(self, file):
        if self.columns_pattern == file.columns:
            return True
        return False


    @staticmethod
    def open_file(self, filename):
        if '.xlsx' in filename:
            self.file = pd.read_excel()
            return self.file
        elif '.csv' in filename:
            self.file = pd.csv()
            return self.file
        else:
            return False

    @staticmethod
    def remove_blank(self):
        columns =[i.rstrip().replace('\xa0', ' ').replace(' (m)', '').replace(' ', '_') for i in
                  self.file.columns.values.tolist()]
        return columns





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