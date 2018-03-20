import os
import sys
import json

# this script ASSUMES that you are using the default version of python which hadoop works with (python 2.7.X) and
# you MUST be a superuser for hdfs on the node to execute the following commands
# NOTE: 
# superuser group to hdfs is configured in dfs.permissions.superusergroup in hdfs-site.xml
# to add an existent user to the default superuser group do: `usermod -a -G hdfs <username>`

AMBARI_USER = os.getenv('AMBARI_USER', "admin")
AMBARI_PASSWD = os.getenv('AMBARI_PASSWD', "admin")
AMBARI_HOST = os.getenv('AMBARI_HOST', "localhost")
C_GROUP = os.getenv('C_GROUP', False)

op = raw_input(
    "1. asignar cuota a todo un grupo\n\
     2. asignar cuota a usuario especifico dentro del grupo:\
     modo de operacion: ")
if not C_GROUP:
    C_GROUP = raw_input("grupo al que pertence(n) el/los usuario(s) a configurar cuota: ")

os.system("curl -u {AMBARI_USER}:{AMBARI_PASSWD} -H 'X-Requested-By: ambari'\
 -X GET \"http://{AMBARI_HOST}:8080/api/v1/groups/{C_GROUP}/members\"\
 -o users.txt".format(AMBARI_USER, AMBARI_PASSWD, AMBARI_HOST, C_GROUP))
os.system("hdfs dfs -ls -C /user > tmp")
# str_dirs_already = open("tmp").read().strip().replace("\n"," ")
ls_dirs_already = open("tmp").read().strip().replace("\n"," ").split()
usr_json = json.load(open("users.txt"))[u'items']
usr_dirs = []
usr_dict = {} #used to verify if an user exists in the directory group

#choose what operation to do

for item in usr_json:
    if (op==1):
        usr_dirs.append("/user/"+str(item[u'MemberInfo'][u'user_name']))
    usr_dict[str(item[u'MemberInfo'][u'user_name'])] = 1
#usr_dirs = ["/user/"+str(item[u'MemberInfo'][u'user_name']) for item in usr_json]

if(op==1):
    str_usr_dirs = ' '.join(usr_dirs)
    dirs_to_create = list(set(usr_dirs)-set(ls_dirs_already))
    str_dirs_to_create = ' '.join(dirs_to_create)
    message_quota ="declare la cuota en común para todos los usuarios del grupo escogido en la variable de entorno C_GROUP <N>: "
elif(op==2):
    esp_user=raw_input("a que usuario se le haran los cambios?: ")
    if usr_dict.get(esp_user,False):
        str_usr_dirs = "/user/"+esp_user
        str_dirs_to_create = "/user/"+esp_user
        message_quota = "cuota a asignar <N>: "
    else:
        sys.exit("el usuario {} no existe dentro del grupo {}".format(esp_user, C_GROUP))
else:
    sys.exit("operación no valida")

print("creando directorios...")
os.system("hdfs dfs -mkdir {}".format(str_dirs_to_create))
print("####### directorios creados #######")
print("\n<N> in bytes, N can also be specified with a binary prefix for convenience, for e.g. 50g for 50 gigabytes and 2t for 2 terabytes etc.")

common_quota = raw_input(message_quota)
print("asignando Space Quota....")
os.system("hdfs dfsadmin -setSpaceQuota {} {}".format(common_quota,str_usr_dirs))
print("quota asignada, puede comprobar el resultado ejecutando:\n\
        hdfs dfs -count -h -q /user/*")
os.remove('tmp')
os.remove('users.txt')