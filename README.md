# CDS Builder



## Docker dev tips


Remove all containers:
```
docker stop `docker ps -q`
docker rm `docker ps -a -q`
```

Remove all relevant images:
```
docker image rm `docker image ls --filter=reference='cdsuser/test-dash:*' -q`
```
