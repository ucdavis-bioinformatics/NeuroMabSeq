



def averageLen(lst):
    lengths = [len(i) for i in lst]
    return 0 if len(lengths) == 0 else (float(sum(lengths)) / len(lengths))

 

file = open('test.csv', 'r')

vl = []
vr = []


for line in file:
    line = line.replace('/n', '')
    split = line.split(',')
    vl.append(split[1])
    vr.append(split[2])


print(averageLen(vl))
print(averageLen(vr))

print(max(vl, key=len))
print(max(vr, key=len))

print(len(max(vl, key=len)))
print(len(max(vr, key=len)))