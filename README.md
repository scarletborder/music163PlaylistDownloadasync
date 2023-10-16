# music163PlaylistDownloadasync
python 异步 获取已知用户所有歌单  
后直接下载到 ./music/{listName}里，这里设置了listName从原始名字到文件夹名字的转换规则  
见`playlist.py` line 29


## tips
`playlist.py` line 33 限制了返回的歌单range

163music.txt 自己拓展爬虫，这里省事直接从网页源码copy了
