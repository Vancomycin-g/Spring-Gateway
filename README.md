在王政代码基础上添加了，两种反弹shell，出网探测，
运行行时缺少什么模块。使用pip下载哪个模块就行了。

输入可疑的url地址，注意端口后面不要跟'/'
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2897198/1648563449938-a6af2e26-e49a-4c77-ae60-63a8a9b8ec99.png#clientId=ueef59e7b-262a-4&from=paste&height=230&id=u7f36b1f4&margin=%5Bobject%20Object%5D&name=image.png&originHeight=459&originWidth=1091&originalType=binary&ratio=1&size=1044455&status=done&style=none&taskId=u11cd66ae-e609-4287-b399-04788c3067b&width=545.5)
# 1.先检测是否存在漏洞
默认命令执行的是whoami，因为好多命令执行并不会回显，whoami若回显成功则存在漏洞
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2897198/1648553065986-9b71117c-4225-45cf-af0e-d16973cfcca1.png#clientId=u5cd8a292-b94f-4&from=paste&height=81&id=u0891a954&margin=%5Bobject%20Object%5D&name=image.png&originHeight=161&originWidth=2050&originalType=binary&ratio=1&size=677883&status=done&style=none&taskId=u063cf6c6-1ed8-4991-a96e-6e870142c56&width=1025)
返回内容有root,确定存在漏洞
# 2.反弹shell
输入公网ip与端口
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2897198/1648553159932-6d64c318-ebdd-45b5-861f-c8add5bbce7f.png#clientId=u5cd8a292-b94f-4&from=paste&height=267&id=u871b6f6e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=533&originWidth=1022&originalType=binary&ratio=1&size=1096147&status=done&style=none&taskId=uc8bef806-558a-4348-a948-110e8f20774&width=511)
若反弹成功，此页面会卡住。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2897198/1648564981885-eadb257e-e758-4d4f-a12a-6ad0d14bef75.png#clientId=ueef59e7b-262a-4&from=paste&height=187&id=u9d6a4e91&margin=%5Bobject%20Object%5D&name=image.png&originHeight=373&originWidth=1252&originalType=binary&ratio=1&size=73455&status=done&style=none&taskId=u8c84af80-072a-41e8-97cc-71ac6694de4&width=626)
若反弹失败，会直接结束
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2897198/1648555782045-0d0a5d4f-f810-448f-bc01-3f8647a508f1.png#clientId=u5cd8a292-b94f-4&from=paste&height=205&id=uf1cb6134&margin=%5Bobject%20Object%5D&name=image.png&originHeight=410&originWidth=518&originalType=binary&ratio=1&size=371044&status=done&style=none&taskId=u2c59631f-cc9c-402b-aaff-23d1e2aafb1&width=259)
# 3.测试出网，
是为了功能4准备的
默认访问百度页面
# 4.使用java代码反弹shell
若不能反弹shell，可能不支持/dev/tcp ，在出网的前提下，可以尝试让靶机下载java代码然后命令执行进行反弹shell
1.打开shell.java文件，修改下面的ip与端口既可，这个文件，windows与Linux通用。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2897198/1648557922164-5fc7e341-33f3-482f-8dba-bc0db8662a48.png#clientId=u5cd8a292-b94f-4&from=paste&height=92&id=m5Z3d&margin=%5Bobject%20Object%5D&name=image.png&originHeight=184&originWidth=834&originalType=binary&ratio=1&size=14407&status=done&style=none&taskId=u01416e4b-7acd-40c1-8939-a867071824c&width=417)
2.然后使用**1.8的环境编译**成shell.class,
因为大多数服务器使用的是1.8,若高的环境也可以适用。**总之编译环境的jdk要小于等于靶机的jdk**
`javac shell.java`
3.托管shell.java文件

![image.png](https://cdn.nlark.com/yuque/0/2022/png/2897198/1648574642529-514bc81f-d615-4044-a339-e953e0254e6d.png#clientId=u6b9afde0-ccb9-4&from=paste&id=u2d853f60&margin=%5Bobject%20Object%5D&name=image.png&originalType=binary&ratio=1&size=2025119&status=done&style=none&taskId=udb93b496-267a-443f-8d17-4094d3eb56d)
[![Travis](https://img.shields.io/badge/语雀-虚无-brightgreen.svg)](https://www.yuque.com/u2395445)
