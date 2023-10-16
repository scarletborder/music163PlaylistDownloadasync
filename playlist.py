# 从获得的li 标签中获得所有想要的以原曲为单个样本集
from bs4 import BeautifulSoup
import re


class PlayListTool:
    def __init__(self, html: str, rule: str) -> None:
        self.file = html
        self.rule = rule
        pass

    def filterRule(self, inStr) -> bool:
        if re.match(self.rule, inStr) is not None:
            return True
        return False

    def execParser(self):
        with open(self.file, "r", encoding="utf-8") as fout:
            soup = BeautifulSoup(fout.read(), "html.parser")
        items = soup.find("ul", id="cBox").find_all("li")
        ret = []

        for item in items:
            element = item.find("a")
            if self.filterRule(element["title"]) is True:
                ret.append(
                    [
                        str(element["href"]).split("=")[-1],
                        str(element["title"]).split("｜")[-1].strip(),
                    ]
                )

        return ret[2:]
        pass


if __name__ == "__main__":
    tool = PlayListTool("./crawler/163musics.txt", r"东方同音录｜.{3}｜.*$")
    # a = tool.filterRule("东方同音录｜东方辉针城~反逆革命｜全收集")
    b = tool.execParser()
    print(b)
    print(len(b))
