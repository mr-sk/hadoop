hadoop
======

Hadoop 2.2.0 for Ubuntu 12.04 LTS x86_64 - This setup was executed on an EC2 m1.small.


##### Start Hadoop

```
/usr/local/hadoop/sbin/start-all.sh
```

### Installation

##### Install Java
```
sudo add-apt-repository ppa:webupd8team/java  
sudo apt-get update && sudo apt-get upgrade  
sudo apt-get install oracle-java7-installer 
```

##### Hadoop Installation
###### Hadoop User
```
sudo addgroup hadoop
su - hduser
ssh-keygen -t rsa -P ""
sudo adduser --ingroup hadoop hduser
cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys
```

###### Hadoop Download
```
cd /usr/local
wget http://apache.petsads.us/hadoop/core/stable/hadoop-2.2.0.tar.gz
tar -xvf hadoop-2.2.0.tar.gz
mv hadoop-2.2.0 hadoop
sudo chown -R hduser:hadoop hadoop
```

###### Setup .bashrc
```
export HADOOP_HOME=/usr/local/hadoop
export JAVA_HOME=/usr/lib/jvm/java-7-oracle
export PATH=$PATH:$HADOOP_HOME/bin

unalias fs &> /dev/null
alias fs="hadoop fs"
unalias hls &> /dev/null
alias hls="fs -ls"
```

###### Hadoop Configuration
```
sudo mkdir -p /app/hadoop/tmp
sudo chown hduser:hadoop /app/hadoop/tmp
sudo chmod 750 /app/hadoop/tmp
```

###### Update XML Files
In Hadoop 2.2.0 the XML files are located in: /usr/local/hadoop/etc/hadoop
See the contents of the following files in this repository:
* core-site.xml
* mapred-site.xml
* hdfs-site.xml


