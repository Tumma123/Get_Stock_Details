from datetime import datetime
today = datetime.today()

from time import strptime
def GetDate():
    isValid=False
    while not isValid:
        userIn = input("Enter Start and End Date time: ")
        try: # strptime throws an exception if the input doesn't match the pattern
            #d = datetime.datetime.strptime(userIn, "%d/%m/%y")
#            d = datetime.strptime(userIn,"%d %b, %Y")
            d = datetime.strptime(userIn, '%b %d %Y %H %M')
            isValid=True
        except:
            print("Invalid")
    return d

#test the function
#print(GetDate())
start =  GetDate()
end   = GetDate()
