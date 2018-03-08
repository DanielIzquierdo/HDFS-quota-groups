import os
import json

# this script ASSUMES that you are using the default version of python which hadoop works with (python 2.7.X) and
# you MUST be a superuser for hdfs on the node to execute the following commands
# NOTE: 
# superuser group to hdfs is configured in dfs.permissions.superusergroup in hdfs-site.xml
# to add an existent user to the default superuser group do: `usermod -a -G hdfs <username>`

os.system("hdfs dfs -ls -C /user > tmp")
# str_dirs_already = open("tmp").read().strip().replace("\n"," ")
ls_dirs_already = open("tmp").read().strip().replace("\n"," ").split()
usr_json = json.load(open("users.txt"))[u'items']
usr_dirs = ["/user/"+str(item[u'MemberInfo'][u'user_name']) for item in usr_json]
str_usr_dirs = ' '.join(usr_dirs)
dirs_to_create = list(set(usr_dirs)-set(ls_dirs_already))
str_dirs_to_create = ' '.join(dirs_to_create)
print("creando directorios...")
os.system("hdfs dfs -mkdir {}".format(str_dirs_to_create))
print("####### directorios creados #######")
print("\n<N> in bytes, N can also be specified with a binary prefix for convenience, for e.g. 50g for 50 gigabytes and 2t for 2 terabytes etc.")
common_quota = raw_input("declare la quota en común para todos los usuarios del grupo escogido en la variable de entorno C_GROUP <N>: ")
print("asignando Space Quota para el grupo....")
os.system("hdfs dfsadmin -setSpaceQuota {} {}".format(common_quota,str_usr_dirs))
print("quota asignada, puede comprobar el resultado ejecutando:\n\
        hdfs dfs -count -h -q /user/*")
os.remove('tmp')
os.remove('users.txt')