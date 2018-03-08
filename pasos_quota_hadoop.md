## pasos para crear directorios en HDFS apra cada usuario y asignarles una cuota en común

1) loguearse en el Server Principal Ambari con un usuario con permisos Administrativos para manipular hdfs

1) llenar las variables que necesites
export AMBARI_USER=<FILL IN> AMBARI_PASSWD=<FILL IN> AMBARI_HOST=<FILL IN> CLUSTER_NAME=<FILL IN> C_GROUP=<FILL IN>

**C_GROUP es el grupo al cuál se le asignará una quota en común**

1) para obtener la lista de usuarios de un grupo determinado:
`curl -u $AMBARI_USER:$AMBARI_PASSWD -H 'X-Requested-By: ambari'\
 -X GET "http://$AMBARI_HOST:8080/api/v1/groups/$C_GROUP/members"\
 -o users.txt`

1) para asignarle una cuota de almacenamiento en común a un grupo(existente en Ambari, ya sea local o del LDAP) de usuarios:

`python create_dirs_and_quota.py`

1) puedes chequear que la cuota fue asignada a los usuarios del grupo con el comando:
`hdfs dfs -count -h -q /user/*`
