#import fi
#f = open('my_file.txt', 'r+')
#my_file_data = f.read()
#f.close()
import GV
from csv import reader
# iterate over each line as a ordered dictionary and print only few column by column Number
with open('field1.csv', 'r') as read_obj:#Simulator file
#with open('field2.csv', 'r') as read_obj:
#with open('Field3.csv', 'r') as read_obj:
#with open('Field5.csv', 'r') as read_obj:#bottom lawn
#with open('Field5c.csv', 'r') as read_obj:#near goal
#print ("Loading Field6.csv")
#with open('Field6.csv', 'r') as read_obj:#Rear garden 3 sections
    csv_reader = reader(read_obj)
    
    for row in csv_reader:
        
        a = row[0]
        b = row[1]
        print(a,b)
        aa = float(a)
        bb = float(b)
        print(aa,bb)

        GV.PointX.append(aa)
        GV.PointY.append(bb)
        
        print(a, b)

print (GV.PointY)


