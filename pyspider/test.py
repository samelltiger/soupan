import http.cookiejar  
import urllib.request  
import urllib.parse
def getOpener(head):  
    # deal with the Cookies  
    cj = http.cookiejar.CookieJar()  
    print(cj)
    pro = urllib.request.HTTPCookieProcessor(cj)  
    print(pro)
    opener = urllib.request.build_opener(pro)  
    header = []  
    for key, value in head.items():  
        elem = (key, value)  
        header.append(elem)  
    opener.addheaders = header  
    return opener  

# res = getOpener({"Cookie":"UM_distinctid=15d2303b5061b9-013d0e5a6b0e3b-5d6a3f77-fa000-15d2303b50711e; uid=4da641e28022a7bb498f3b82e8e165d7; ASPSESSIONIDCSATBCTC=ELDMJOCCMINEGPIKNMDJFCGC; ASPSESSIONIDASATAASC=NFHMJOCCKLJKIPEEHHNNMFLD; CNZZDATA2248624=cnzz_eid%3D2005743748-1499526615-null%26ntime%3D1504502955; Hm_lvt_d0a6a9f299b739eae1eeb1ef415604ca=1503058995,1504231480,1504496694; Hm_lpvt_d0a6a9f299b739eae1eeb1ef415604ca=1504505967"})
# print(res)
resp = urllib.request.urlopen("http://localhost/console/setcookie.php")
