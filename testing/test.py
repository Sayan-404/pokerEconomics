
list=[1,2]
start=0
end=len(list)-1
i=0
while 1:
    print(i)
    if i == 1:
        end = i-1   
    if i == end:
        break
    i=(i+1)%len(list)   

