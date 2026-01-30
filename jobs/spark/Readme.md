
## REQUIREMENTS

- java version 17 for Spark 4.0.1
- sbt version 1.19

- To view all java versions installed
```bash
sudo update-alternatives --config java
```

- To install java 17 (if applicable)

```bash
sudo apt install openjdk-17-jdk
```

- Install sbt
```bash
echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | sudo tee /etc/apt/sources.list.d/sbt.list

curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo tee /etc/apt/trusted.gpg.d/sbt.asc

sudo apt-get update
sudo apt-get install sbt

sbt --version

```

## BUILD JAR

- Go to the root of the project
```bash
cd spark-iceberg-project
```
- Execute command below to 
```bash
sbt clean assembly
```


