import json
import aiohttp
import os


class netmusic_apis:  # 网易云相关函数
    def __init__(self, apiurl: str, apicookies: dict, listname: str) -> None:
        self.api_url = apiurl
        self.api_cookies = apicookies
        self.listname = listname
        if os.path.exists(f"./music/{self.listname}") is False:
            os.mkdir(f"./music/{self.listname}")
        pass

    async def get_music_list(self, songlist_id: str, maxnum: int):  # 获取音乐列表
        all_song_info = []

        async with aiohttp.ClientSession(cookies=self.api_cookies) as se:
            async with se.get(
                url=self.api_url
                + "/playlist/track/all?id="
                + songlist_id
                + "&limit=all",
            ) as resp:
                json_text = await resp.text()

        try:
            json_text = json.loads(json_text)
            if json_text["code"] != "200":
                raise Exception
            flag = 0
        except:
            try:
                async with aiohttp.ClientSession() as se:
                    async with se.get(
                        url=f"https://api.no0a.cn/api/cloudmusic/playlist/{songlist_id}"
                    ) as resp:
                        json_text = await resp.text()
                        json_text = json.loads(json_text)
                        flag = 1
            except:
                return

        # code = json_text["code"]

        # if code != 200:
        #     print("获取音乐列表:失败")
        #     print(json_text)
        # else:
        #     print("获取音乐列表:成功")
        if flag == 0:
            song_num = min(len(json_text["songs"]), maxnum)
        else:
            song_num = min(maxnum, len(json_text["results"]))

        print("歌曲数量:" + str(song_num))

        i = 0

        while i < song_num:
            if flag == 0:
                id = json_text["songs"][i]["id"]
            else:
                id = json_text["results"][i]["id"]

            all_song_info.append(id)

            i = i + 1

        return all_song_info

    async def downMusic(self, allList: list):
        for song in allList:
            name = str(song)
            mid = str(song)
            async with aiohttp.ClientSession(
                headers={  # 下载音乐用的headers
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"
                }
            ) as se:
                url = (
                    "https://music.163.com/song/media/outer/url?id=" + str(mid) + ".mp3"
                )
                async with se.post(url) as resp:
                    with open(f"./music/{self.listname}/{name}.mp3", "wb") as fd:
                        # iter_chunked() 设置每次保存文件内容大小，单位bytes
                        async for chunk in resp.content.iter_chunked(1024 * 1024):
                            fd.write(chunk)
                pass

        pass

    async def execDown(self, songlist_id: str, maxnum: int):
        mList = await self.get_music_list(songlist_id, maxnum)
        if mList is None:
            return
        await self.downMusic(mList)


if __name__ == "__main__":
    import asyncio

    async def main(tool: netmusic_apis):
        l = await tool.get_music_list("2893510982", 5)
        await tool.downMusic(l)

        # down

    tool = netmusic_apis(
        apiurl="http://cloud-music.pl-fe.cn",
        apicookies={
            "MUSIC_U": "0030158EF926D2C87DD2FF1FB4993EAAA306175F6F5151253508C57EB663B7C0D8875794E3DFB3E05B3C140AAA74DD22AC5D9A9BDDD6DF97EC7C03CEB8D05B95DE8275537C6CD72DE7C9F544D2F49954A845B59F43B76ACBCBCDF3E0CB4CDAE8FEACC9296AD0138FF6DFA8636AB42FBEBB83759703FBB4FD92B7BA95C7883985B99A8467F1E7B41D28E3DFB6103190D3FE16EEDCC841C567094A2FA4ACB06AA53B7905F69D58A930A6E7C73015432AECC4649FAEA97735A40AD19FB197241935BB4248F7D1FC4A46404DE95D0F5D4893433FF578F3912F81CC689E97556B85B51958530215A5638AEEFDDC4AABDE92054A3A8FE84E45C9870BF7924CCCA7E1EE3F6427DAF1BF5EF736661A47B11C918F6181A909BC3650622AA199A356F12590C5E9EE183F2C02BE3065E0AE4401A0B8AEBD95A19F933222DE4D0E60F8AF511E42437F1CCA68C760378B9CBE72CE1A8F2D4E6CD10F301EB217BCF430627117C5D8C24BF6F95FB7A0114FBE77D937117A67",
            "NMTID": "00O2vZsuoR3-zUxxUqLiD4kD9bGYvEAAAGK1nXrIw; _iuqxldmzr_=32",
        },
        listname="123",
    )

    asyncio.run(main(tool))

    # music_list = netmusic_apis.get_music_list(15)
    # music_num = len(music_list)
