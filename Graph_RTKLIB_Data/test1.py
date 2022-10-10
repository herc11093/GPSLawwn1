import pandas
mydata = [{'subid': 'B14-111', 'age': 75, 'fdg': 3}, {'subid': 'B14-112', 'age': 22, 
           'fdg': 2}, {'subid': 'B14-112', 'age': 40, 'fdg': 5}]

df = pandas.DataFrame(mydata)
df = df.sort(['age'])  # dict doesn't preserve order
df.plot(x='age', y='fdg', marker='.')