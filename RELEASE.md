## Release to PyPI

Update setup.py to the new version

Update docs: z2jh and dockerspawner to the latest tags

delete dist folder

delete cdsdashboards.egg-info

`python setup.py sdist bdist_wheel`

`twine upload dist/*`

git add and git commit

`git tag -a X.X.X -m 'comment'`

`git push`

`git push --tags`


## Remove tags

# delete local tag '123'
git tag -d 123
# delete remote tag '123'
git push origin :refs/tags/123


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
