import pandas as pd
#
# login = pd.read_csv('login.csv')
# print(login)
# login.at[1,'id'] = 4
# print(login)

mukadam_data = pd.read_csv('mukadam.csv')
found_mukadam = mukadam_data[mukadam_data['aadhar']==2]

print(found_mukadam['name'][found_mukadam.index][1])
# print(mukadam_data.loc[found_mukadam.index,'current no of workers'])
# mukadam_data.at[found_mukadam.index,'current no of workers'] = 0
# current_no_of_workers = mukadam_data.loc[found_mukadam.index,'current no of workers']
#
# # mukadam_data.at[found_mukadam.index,'current no of workers']
# mukadam_data.at[found_mukadam.index,'current no of workers'] = current_no_of_workers+1
# print(mukadam_data['current no of workers'])
