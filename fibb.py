


def fibb(n):
    if (n==0):
        return 0
    elif(n==1 or n==2):
        return 1
    else:
        (fibb(n-1)+fibb(n-2))
n = int(input("enter"))
for i in range(n):
      print("fibbi",i,fibb(i))
        
        
