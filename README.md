# img
```bash
cp images/* diannaobizi/
```
```
- ht
```
```
find . -type f -exec basename {} \; | awk '{print "- https://ecdn.317927.xyz/gh/1715819/img@main/2/" $1}' > file_urls.txt
```
