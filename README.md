# setup
Server setup and client setup tips

## windows client
[Configure correct java version after installing](https://www.happycoders.eu/java/how-to-switch-multiple-java-versions-windows/): setup JAVA_HOME and delete javapath directories from PATH

## map migration
Prune all unnecessary chunks using [mcaselector](https://github.com/Querz/mcaselector) replace default server world folder

## server
run **SETUP.sh** with game version and optionally a backup

use **screen** to manage running servers:
```shell
screen -S server  # create a named session
Ctrl-a + d  # leave a session
screen -r server  # reconnect to the named session
```
