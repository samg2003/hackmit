import pandas as pd
a = []
with open("data.txt", 'r') as file:
    while file.readline():
        a.append(file.readline()[:-1].split())

for line in range(len(a)):
    for number in range(len(a[line])):
        a[line][number] = float(a[line][number])

print(a[1], a[102])
