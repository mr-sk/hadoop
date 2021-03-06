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
* /usr/local/hadoop/etc/hadoop (log4j.properties)

###### Prepare Hadoop Input
For this example, I'm performing the "Hello World" of Map Reduce, which is "Word Count". I've downloaded three
Project Gutenberg UTF-8 books and placed them in the "/tmp/gutenberg" which I will copy to HDFS "/gutenberg_input".

```
hadoop dfs -copyFromLocal /tmp/gutenberg /gutenberg_input
```

###### Execute Hadoop Job
```
javac -classpath /home/ubuntu/.m2/repository/org/apache/hadoop/hadoop-core/0.20.2-cdh3u2/hadoop-core-0.20.2-cdh3u2.jar -d wordcount_classes WordCount.java
jar -cvf wordcount.jar -C wordcount_classes/ .
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


### MapReduce I: Word Count in Python

Using the mapper and reducer written in python included in the repository:
* mapper.py
* reducer.py

We can test they are running properly: 
```
echo "foo foo quuz labs foo bar quuz" | ./mapper.py  | sort -k1,1 | ./reducer.py 
bar	1
foo	3
labs	1
quuz	2
```

Now we'll execute them with Hadoop.
(I've included the streaming 2.2 .jar in the repo as well)

```
hadoop jar hadoop-streaming-2.2.0.jar -file mapper.py -mapper mapper.py -file reducer.py  -reducer reducer.py -input /gutenberg_input -output /gutenburg_output_python
...
...
hadoop dfs -cat /gutenburg_output_python/part-00000 | more
"(Lo)cra"	1
"1490	1
"1498,"	1
"35"	1
"40,"	1
"A	2
"AS-IS".	1
...
```

### MapReduce II: Inverted Index in Python

Based on the Java Iverted Index (but ghetto simplified) see the python files included in the repo:
* inverted_index/mapper.py
* inverted_index/reducer.ph
* inverted_index/a.txt, b.txt

Test they are running:
```
cat a.txt b.txt | ./mapper.py | ./reducer.py 
bat b.txt
sat a.txt
mat a.txt
fat b.txt
cat a.txt,b.txt
```

Copy the files into HDFS
```
hdfs dfs -mkdir /inverted_index_input
hdfs dfs -put a.txt /inverted_index_input/a.txt
hdfs dfs -put b.txt /inverted_index_input/b.txt
hdfs dfs -ls /inverted_index_input/
-rw-r--r--   1 hduser supergroup         18 2013-11-27 20:01 /inverted_index_input/a.txt
-rw-r--r--   1 hduser supergroup         18 2013-11-27 20:02 /inverted_index_input/b.txt
```

Now execute the hadoop job:
```
hadoop jar ../hadoop-streaming-2.2.0.jar -file mapper.py -mapper mapper.py -file reducer.py -reducer reducer.py -input /inverted_index_input/ -output /inverted_index_output_python
```

Check the output:
```
hdfs dfs -ls /inverted_index_input/
-rw-r--r--   1 hduser supergroup          0 2013-11-27 20:03 /inverted_index_output_python/_SUCCESS
-rw-r--r--   1 hduser supergroup         61 2013-11-27 20:03 /inverted_index_output_python/part-00000

hdfs dfs -cat /inverted_index_output_python/part-00000
bat b.txt	
sat a.txt	
mat a.txt	
fat b.txt	
cat a.txt,b.txt	
```





