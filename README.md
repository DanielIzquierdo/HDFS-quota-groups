## pasos para crear directorios en HDFS para cada usuario y asignarles una cuota en común

1) loguearse en el Server Principal Ambari con un usuario con permisos superuser para manipular hdfs (superuser group of hdfs is configured in dfs.permissions.superusergroup in hdfs-site.xml, to add an existent user to the default superuser group do: `usermod -a -G hdfs <username>`)

1) llenar las variables que necesites
`export AMBARI_USER=llenar_usuario_de_ambari AMBARI_PASSWD=llenar_password AMBARI_HOST=llenar_con_host CLUSTER_NAME=llenar_con_nombre_cluster C_GROUP=llenar_con_nombre_de_grupo`
**C_GROUP es el grupo de usuarios a los cuales se les asignará una quota de almacenamiento en común**

1) para obtener la lista de usuarios de un grupo determinado:
`curl -u $AMBARI_USER:$AMBARI_PASSWD -H 'X-Requested-By: ambari'\
 -X GET "http://$AMBARI_HOST:8080/api/v1/groups/$C_GROUP/members"\
 -o users.txt`

1) para asignarle una cuota de almacenamiento en común a un grupo(existente en Ambari, ya sea local o del LDAP) de usuarios: `python create_dirs_and_quota.py`

1) puedes chequear que la cuota fue asignada a los usuarios del grupo con el comando: `hdfs dfs -count -h -q /user/*`




me basé en los siguientes links para crear el repositorio:
* http://hadoop.apache.org/docs/r2.7.2/hadoop-project-dist/hadoop-hdfs/HdfsQuotaAdminGuide.html
* https://www.intropro.com/resources/blog/108-hadoop-hdfs-quota-space-usage-and-cli-tools
* https://community.hortonworks.com/articles/81353/popular-ambari-rest-api-commands.html
* https://community.hortonworks.com/content/supportkb/49416/managing-ambari-users-and-groups-with-the-rest-api.html
* https://www.cyberciti.biz/faq/howto-linux-add-user-to-group/
* https://hadoop.apache.org/docs/r2.4.1/hadoop-project-dist/hadoop-hdfs/HdfsPermissionsGuide.html
