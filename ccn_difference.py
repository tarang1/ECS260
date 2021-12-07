#from pydriller.metrics.process.contributors_experience import ContributorsExperience
#metric = ContributorsExperience(path_to_repo='./exercism')
# from pydriller.metrics.process.contributors_experience import ContributorsExperience
import pydriller as p
import subprocess
import json
# metric = ContributorsExperience(path_to_repo='./exercism',
#                                 from_commit='90f07ec1f2d4c874d187995dff7b055e20d0f046',
#                                 to_commit='118d53b6098268e8bb0f9924e69ae9b3eaa4b4b5')
# # c = [] 
# import pdb
# pdb.set_trace()
contributors = set()
user_change = {}
#def get_modified_files()
file_name_extensions = tuple([".h", ".m", ".mm", ".M",".js",".java",".py",".c",".h",".cpp"])

k =subprocess.check_output("git branch".split()).decode("utf-8").split("\n")

branch_name = ""
for l in k:
    if "*" in l:
        branch_name = l

branch_name = branch_name.split("*")[1].strip()
# import pdb
# pdb.set_trace()
for commit in p.Repository('./').traverse_commits():

    if commit.author.name not in user_change:
        user_change[commit.author.name] = []
    modified_files = commit.modified_files

    all_files_new = ""
    all_files_old = ""
    if not modified_files:
        continue

    command_new = "lizard "
    command_old = "lizard "
    for f in modified_files:
        new_file_path = f.new_path
        old_file_path = f.old_path
        if not new_file_path:
            continue
        if not old_file_path:
            continue

        if not new_file_path.endswith(file_name_extensions):
            continue
        all_files_new+=f.new_path + " "
        all_files_old+=f.old_path + " "
    if not all_files_new:
        continue
    if not all_files_old:
        continue
    # import pdb
    # pdb.set_trace()
    _ = subprocess.check_output("git checkout {}".format(commit.hash).split())
    op = subprocess.check_output("{}{}".format(command_new,all_files_new).split())
    op = op.strip().decode('utf-8')

    temp = op.splitlines()[-1:]
    temp = temp[0].split(" ")
    final_list = []
    for i in range(len(temp)):
        if temp[i]:
            final_list.append(temp[i])
    final_ccn_1 = final_list[2]

    _ = subprocess.check_output("git checkout HEAD~1".split())
    op_1 = subprocess.check_output("{}{}".format(command_old,all_files_old).split())
    op_1 = op_1.strip().decode('utf-8')

    temp_1 = op_1.splitlines()[-1:]
    temp_1 = temp_1[0].split(" ")
    final_list_1 = []
    for i in range(len(temp_1)):
        if temp_1[i]:
            final_list_1.append(temp_1[i])
    final_ccn_2 = final_list_1[2]
    # import pdb
    # pdb.set_trace()
    user_change[commit.author.name].append(float(final_ccn_2)-float(final_ccn_1))

    _ = subprocess.check_output("git checkout {}".format(branch_name).split())

    #print(commit.hash, commit.modified_files)
    #c.append(commit.hash)
out_file = open("kafka.json", "w")
  
json.dump(user_change, out_file, indent = 6)
  
out_file.close()

print(json.dumps(user_change))
#print(contributors, c[0], c[-1])