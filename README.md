# satori-core
The core functionalities of the Satori-NG Suite.
  
File System (and more) *Greppable/Diffable* Serialization

## Contents
The *Satori-NG Core* consists of the *Satori Image File* basic format implementations, along with the `SatoriImage` class, and common functions.
  

### The `satori-file` entrypoint
The package contains a *Satori Image File* checker and reader that can be run with:

#### Check if a file is a *Satori Image File*
```bash
$ satori-file -q test_image.json.gz 
[!] invalid load key, '{'.
[+] File is a compressed JSON SatoriImage 
```

#### Print a Satori Image File as JSON 
```bash
$ satori-file test_image.json.gz
[!] invalid load key, '{'.
[+] File is a compressed JSON SatoriImage
{
 "metadata":{
  "uuid":"fa7b6117-5336-404e-a7f7-c16f4c57acc9",
  "system":{
   "type":"Linux",
   "platform":"Linux-4.15.3-300.fc27.x86_64-x86_64-with-fedora-27-Twenty_Seven",
   "hostname":"FkUkO43a",
   "machine":"x86_64",
   "release":"4.15.3-300.fc27.x86_64",
   "processor":"x86_64",
   "user":"user1"
  },
  "satori":{
   "version":"0.1.0",
   "extensions":[]
  },
  "timestamp":{
   "tstamp":1525443206.9632154,
   "unix":"Fri May  4 17:13:26 2018",
   "tz-secs":-7200
  }
 },
 "data":{
  "filesystem":{
   "/":{
    "type":"D",
    "contents":{
     "tmp":{
      "type":"D",
      "contents":{
       "dir":{
        "type":"D",
        "contents":{
         "dir3":{
[...]
```
The JSON output can be used with commands like `jq` and [`gron`](https://github.com/tomnomnom/gron)

#### `SatoriImage` / `os` module [Interchangeability]:
```python
>>> satori_image.listdir('/tmp/dir')
dict_keys(['dir3', 'dir2', 'test4', 'test3', 'test2', 'test1'])
>>> st = satori_image.stat('/tmp/dir')
>>> st
{'st_blksize': 4096, 'st_blocks': 0, 'st_dev': 43, 'st_gid': 1000, 'st_ino': 12256767, 'st_mode': 16893, 'st_nlink': 4, 'st_rdev': 0, 'st_size': 160, 'st_uid': 1000, 'st_atime': 1525443206.9662495, 'st_mtime': 1525442545.44051, 'st_ctime': 1525442545.44051}
>>> st.st_uid
1000
```


### Crawlers
The *Satori-NG Core* also contains a `Crawler` class that is internally used as a generic `os.walk` implementation, yielding `(path, type)` tuples for objects (modules, class instances, etc) that implement `listdir(path)` and `lstat(path)` methods.

```python
import os
>>> from satoricore.crawler import BaseCrawler
>>>
>>> crawler = BaseCrawler(
...         entrypoints='/usr/lib/python3.6/site-packages/',
...         excluded_dirs=['/proc'],
...         image=os
...     )
>>> 
>>> for path, type in crawler():
...     print(path, type)
... 
/ D   # D for Directory
[...]
/usr/lib/python3.6/site-packages/easy_install.py U    # U for any type of file
[...]
```

Crawlers are also compatible with `SatoriImage` objects, as they are designed to be interchangeable with the `os` module:

```python
>>> satori_image = load_image("test_image.json.gz")
>>> crawler = BaseCrawler(
...         entrypoints='/tmp',
...         excluded_dirs=[],
...         image=satori_image
...     )
>>> crawler = BaseCrawler('/tmp', [], image=satori_image)
>>>
>>> for path, type in crawler():
...     print (path, type)
... 
/ D
/tmp D
/tmp/dir D
/tmp/dir/dir3 D
/tmp/dir/dir2 D
/tmp/dir/test4 U
/tmp/dir/test3 U
/tmp/dir/test2 U
/tmp/dir/test1 U
```

