import sqlite3

# from database import Database
import os
import schema
import json
import inspect


class Sort:
    def __init__(self) -> None:
        pass

    def listpath(self, path="./modules"):
        lists = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if os.path.isfile(os.path.join(root, name)):
                    lists.append(os.path.join(root, name))
        return lists

    def drdata(self):
        paths = self.listpath()
        dicts = {}
        for p in paths:
            imported_vars = {}
            try:
                exec(open(p).read(), imported_vars)
                # print(imported_vars["metadata"])
            except:
                continue
            if "metadata" in imported_vars:
                metadata_var = imported_vars["metadata"]
                # قم بمعالجة المتغير هنا
                dicts.update({p: metadata_var})
        return dicts

    def woriteJsonFile(self):
        with open("db/modules_drdata_base.json", "w") as f:
            json.dump(self.drdata(), f)

    def readJsonFile(self):
        with open("db/modules_drdata_base.json") as f:
            return json.load(f)

    def readDirs(self):
        modsum = {}
        names = 0
        self.woriteJsonFile()
        pTest = self.readJsonFile()

        for path in os.listdir("./modules"):
            x = 0
            for root, dirs, files in os.walk(os.path.join("./modules", path)):
                for file in files:
                    if os.path.join(root, file) in pTest:
                        x += 1
                    modsum.update({path: int(x)})
        return modsum

    def listmodules(self):
        lists = []
        x = self.readJsonFile()

        for i in x:
            lists.append(str("".join(i).replace(".py", "").replace("./modules/", "")))
        # print(lists)
        return lists
