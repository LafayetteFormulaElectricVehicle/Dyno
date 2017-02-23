Read Me

The two python files in this directories are example logging files that can write messages in syslogd. logging.conf is the configuration file for those two files. 

In the folder, system, there is a vsd.service file. This is the file that systemd will run as the daemon. One of its key command, ExecStart, takes two args (or more). The first is the absolute path to an executable, the second is the command to run following the syntax of the executable. 
Remember to change the path for working directory. 
