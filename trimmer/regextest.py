import re

result = re.findall("(A+|B+)A+(A+|B+)A+", "AAAAABBBBAAAA")
print(result)
