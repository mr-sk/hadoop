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

###### Prepare Hadoop Input
For this example, I'm performing the "Hello World" of Map Reduce, which is "Word Count". I've downloaded three
Project Gutenberg UTF-8 books and placed them in the "/tmp/gutenberg" which I will copy to HDFS "/gutenberg_input".

```
hadoop dfs -copyFromLocal /tmp/gutenberg /gutenberg_input
```

###### Execute Hadoop Job
```
hadoop jar wordcount.jar org.myorg.WordCount /gutenberg_input /gutenberg_output
```

After the job completes, view the output and copy from HDFS: 
```
hls /gutenberg_output

Found 2 items
-rw-r--r--   1 hduser supergroup          0 2013-11-25 23:44 /gutenberg_output/_SUCCESS
-rw-r--r--   1 hduser supergroup     880838 2013-11-25 23:44 /gutenberg_output/part-r-00000

hadoop dfs -getmerge /gutenberg_output /tmp/gutenberg_output
tail -n 400 /tmp/gutenberg_output
wristbangles	1
wristlet,	1
wrists	1
wrists,	1
writ	4
writ.	1
write	62
...
```


