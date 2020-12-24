import pandas as pd

login = pd.read_csv('login.csv')
print(login)
login.at[1,'id'] = 4
print(login)
