## steps to create directories in HDFS for every user of an specific group and assign a Space Quota 

1) login in the principal Ambari Server with superadmin user (HDFS superadmin) (superuser group of hdfs is configured in dfs.permissions.superusergroup in hdfs-site.xml, to add an existent user to the default superuser group do: `usermod -a -G hdfs <username>`)

1) set the environment variables
`export AMBARI_USER=llenar_usuario_de_ambari AMBARI_PASSWD=llenar_password AMBARI_HOST=llenar_con_host CLUSTER_NAME=llenar_con_nombre_cluster C_GROUP=llenar_con_nombre_de_grupo`

1) assign a space quota to a group/user(local or LDAP ambari user): `python create_dirs_and_quota.py`

1) you can chek the assigned quota with: `hdfs dfs -count -h -q /user/*`


## MANUAL SETTING: How to use space Quota in HDFS
### if you prefer to do it manually without the scripts provided

The hdfs admin can create Quota. There is two types of quota: 
- space quota ( how much storage can be used )
- file quota ( how many files can be created )

This alert only check the space quota, it doesn't look into file quota.

Set a quota of 2GB on folder /application/digital - value are in bytes = 2*1024*1024*1024 = 2147483648
```sh
hdfs dfsadmin -setSpaceQuota 2147483648  /application/digital
```
NB: Quota works on raw storage

Check the quota ( can be run by any user w/ read permission on folder ) 
```sh
hdfs dfs -count -q /application/digital
       none             inf      2147483648      1832910848            1            1          104857600 /application/digital
                                    |               |
                                  Quota           Usage
```

Delete quota
```sh
hdfs dfsadmin -clrSpaceQuota /application/digital
```



references:
* http://hadoop.apache.org/docs/r2.7.2/hadoop-project-dist/hadoop-hdfs/HdfsQuotaAdminGuide.html
* https://www.intropro.com/resources/blog/108-hadoop-hdfs-quota-space-usage-and-cli-tools
* https://community.hortonworks.com/articles/81353/popular-ambari-rest-api-commands.html
* https://community.hortonworks.com/content/supportkb/49416/managing-ambari-users-and-groups-with-the-rest-api.html
* https://www.cyberciti.biz/faq/howto-linux-add-user-to-group/
* https://hadoop.apache.org/docs/r2.4.1/hadoop-project-dist/hadoop-hdfs/HdfsPermissionsGuide.html
