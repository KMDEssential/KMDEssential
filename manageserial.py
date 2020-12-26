import hashlib 
from datetime import datetime
from binascii import unhexlify, b2a_base64
import re
import os
import string
import random

class manageSerial():
    def __init__(self):
        self.serial_in = ""
        self.serial_out = ""

    def makeSerial(self, regdate = datetime.today().strftime("%Y%m%d")):
        serial = ""
        for i in range(8) : 
            serial += random.choice(string.ascii_lowercase)

        result =""
        str1 = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', serial)
        if len(str1) >= 8 :
            str_head = str1[0:8].lower()
            str2 = self.joinBase64(str_head,regdate)
            str4 = str2[0:12]
            str5 = str_head + str4
            result = str5[0:4]+"-"+str5[4:8]+"-"+str5[8:12]+"-"+str5[12:16]+"-"+str5[16:20]
        return result

    def checkSerial(self,serial,regdate):
        result = False
        str1 = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', serial)
        if len(str1) >= 20 :
            str_head = str1[0:8].lower()
            str2 = self.joinBase64(str_head,regdate)
            str_tail = str1[8:20].lower()
            str4 = str2[0:12]
            if str_tail == str4 : result = True
        return result

    def joinBase64(self, str1, str2):
        str3 = str1 + str2
        str4 = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', str3)
        str5 = b2a_base64(unhexlify(hashlib.sha256(str4.encode("UTF-8")).hexdigest() )).decode()
        str6 = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', str5).lower()
        return str6

    def makePathserial(self,serial):
        path = os.getcwd()
        result = self.joinBase64(path,serial)
        return result

    def checkPathserial(self,serial,pathserial):
        path = os.getcwd()
        result = self.joinBase64(path,serial)
        if result == pathserial : 
            return True
        else :
            return False