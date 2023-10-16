from playlist import PlayListTool
from downsongs import netmusic_apis
import asyncio

apiurl = "http://cloud-music.pl-fe.cn"
apicookies = {
    "MUSIC_U": "不甜没关系",
    "NMTID": "不甜没关系",
}


class CrawlerApi:
    def __init__(self, maxMusicPerModel: int) -> None:
        self.maxSong = maxMusicPerModel
        pass

    def exec(self) -> str:
        """
        返回原曲中文名
        """
        listtool = PlayListTool("./crawler/163musics.txt", r"东方同音录｜.{3}｜.*$")
        idnameList = listtool.execParser()
        for idname in idnameList:
            pid = idname[0]
            name = idname[1]
            downtool = netmusic_apis(
                apiurl=apiurl, apicookies=apicookies, listname=name
            )
            asyncio.run(downtool.execDown(pid, self.maxSong))
            yield name, pid


import os

if __name__ == "__main__":
    api = CrawlerApi(2)
    generator = api.exec()
    testid = 0
    for v in generator:
        print(v)
        if len(os.listdir(f"./music/{v[0]}")) == 0:
            print("获取失败,pid已放到fail.txt，跳过这个")
            with open("./music/fail.txt", "a") as fout:
                fout.write(f"{v[1]}\n")
            continue
        print("开始训练")
        testid += 1
        if testid == 4:
            break
