import pandas

# pomodorotimer
# TODO record:
# TODO time started
# TODO time ended


class DatabaseManager():
    def __init__(self):
        # template - not strictly limited to this though
        self.data = {
            "hi" : ["hi"], # STRUCTURAL HI DO NOT REMOVE
            "Sessions_Worked" : [],
            "Minutes_Worked" : [],
            "Start_Time" : [],
            "End_Time": [],
        }
        return

    def append_memory_to_csv(self, file_name="database.csv"):
        csv_data = pandas.read_csv(file_name)
        df_data_to_append = pandas.DataFrame(self.data)
        data = pandas.concat([csv_data, df_data_to_append], ignore_index=True)
        data.to_csv(file_name, index=False)
        return

def db_demo():
    #read csv
    INPUT_VAR_1 = "Tunsday"
    INPUT_VAR_2 = 55
    INPUT_VAR_3 = "Gloomy"
    data = pandas.read_csv("database.csv")


    #add new input
    new_input = {
        "day" : [INPUT_VAR_1],
        "temp" : [INPUT_VAR_2],
        "condition": [INPUT_VAR_3]
    }




    new_input = pandas.DataFrame(new_input)
    # data += new_input
    #concat two df
    # print(data.head())
    # print(new_input.head())


    data = pandas.concat([data,new_input], ignore_index=True)
    # print(data)


    #write to csv
    data.to_csv("database.csv", index=False)
