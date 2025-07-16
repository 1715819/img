# img
```bash
cp images/* diannaobizi/
```
```
- https://ecdn.317927.xyz/gh/1715819/img@main/img/1704300707384170430070714.png
```
```
find . -type f -exec basename {} \; | awk '{print "- https://ecdn.317927.xyz/gh/1715819/img@main/images/" $1}' > file_urls.txt
```