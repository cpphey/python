import pandas as pd

class Scrap:
    def __init__(self):
        pd.set_option('display.max_columns', None)  # or a large number like 100
        pd.set_option('display.width', None)  # Automatically adjust to terminal width
        pd.set_option('display.max_colwidth', None)  # Automatically adjust column width

    def age_to_string(row):
        print ("here")
        print(row)
        # row['asd']
        return f"Age: {row['Age']}"

    def read(self):
        df = pd.read_csv('newoutput.csv')
        pass

# data = {'Name': ['Alice', 'Bob', 'Charlie'],
#         'Age': [25, 30, 22],
#         'City': ['New York', 'London', 'Paris'],
#         'Country': ['USA', 'UK', 'France']}
# df = pd.DataFrame(data)
#
# df['Age_String'] = df.apply(age_to_string, axis=1)
#
# print(df)
    def test(self):
        # Sample DataFrames
        df1 = pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})
        df2 = pd.DataFrame({'col1': [1, 1, 2], 'col3': ['X', 'Y', 'Z']})

        # Perform the join to duplicate df1 rows for each corresponding df2 row
        df_new = df1.merge(df2, on='col1', how='left')

        # Print the result
        print(df_new)

    def


def main():
    s = Scrap()
    # s.read()
    s.test()
    pass

if __name__ == '__main__':
    main()