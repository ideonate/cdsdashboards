## Release to PyPI

Update setup.py to the new version

delete dist folder

`python setup.py sdist`

`twine upload dist/*`

git add and git commit

`git tag -a X.X.X -m 'comment'`

`git push`

`git push --tags`


## Docker dev tips

Remove all containers:
```
docker stop `docker ps -q`
docker rm `docker ps -a -q`
```


Remove all relevant images:
```
docker image rm `docker image ls --filter=reference='cdsuser/*:*' -q`
```
