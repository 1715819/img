#!/bin/bash

cd diannaobizi

for file in *; do
  if [[ -f "$file" ]]; then
    extension="${file##*.}"
    newname="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1).${extension}"
    
    # 如果新文件名已存在，生成直到不冲突为止
    while [[ -e "$newname" ]]; do
      newname="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1).${extension}"
    done

    mv "$file" "$newname"
  fi
done
