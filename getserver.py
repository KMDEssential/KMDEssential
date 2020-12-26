import requests

class getServer():

    def __init__(self):
        self.urlmain = "https://raw.githubusercontent.com/KMDEssential/KMDEssential/main"
        self.version_usage = dict()
        self.msg = ""
        self.version_latest =""
        self.version =""

    def getversion(self):
        url = self.urlmain + "/VERSION/version"
        source = requests.get(url).text
        result = source.rstrip('\n')
        return result
    
    def getmsg(self):
        result =""
        url = self.urlmain + "/VERSION/msg"
        source = requests.get(url).text
        str = source.split('#')
        for key in str:
            if "version" in key : 
                str1 = key.split('\n')
                for key2 in str1:
                    str2 = key2.split(" ")
                    if len(str2) ==2:
                        self.version_usage[str2[0]]=str2[1]
                        if str2[1]=='latest':
                            self.version_latest = str2[0]
        for key in str:
            if "msg" in key :
                position = key.rfind('\n')
                str1 = key[0:position-1]
                str2 = str1.replace("$VERSION",self.version).replace("$LATEST", self.version_latest).replace("msg\n","")
                result = str2
        return result
