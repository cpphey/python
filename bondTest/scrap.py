import pandas as pd

class Scrap:
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

def main():
    s = Scrap()
    s.read()
    pass

if __name__ == '__main__':
    main()