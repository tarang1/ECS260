import pydriller as p
import subprocess
import json
count = 0
for commit in p.Repository('./').traverse_commits():
    count+=1
print(count)
