# MTR寻路bot

## 介绍

模仿LPS的寻路Bot，写了一个官方API的QQ机器人。

### 官方仓库

https://github.com/tencent-connect/botpy

https://github.com/CokeStudios/mtr-pathfinder

### 存在的问题

·图片从图床删除时使用selenium库访问url的功能，访问速度较慢且容易发生问题（这是源库的问题，暂时无法修复）。

### 声明

·bot脚本使用的部分代码借鉴自网络。

## 下载
首先下载QQ机器人的前置库，将根目录中的`requirements.txt`中的库下载，然后使用命令
``` powershell
pip3 install -U fontTools opencc pillow networkx requests
```

## 如何使用

#### (1) 更改机器人的账号密码

在 ./botpy/examples/config.yaml 中，找到

```yaml
#机器人配置
appid: "Your_Bot_Id"
secret: "Enter_Your_Bot_Secret_Here"
```

将其中的*Your_Bot_Id*和*Enter_Your_Secret_Here*分别更改为你的机器人Apple Id和Apple Secret。需从QQ开放平台获取。

#### （2）更改图床API令牌

\*因为本项目使用的sm.ms图床，所以脚本是基于该图床返回内容格式编写，如果你想用其它图床需根据自己图床返回数据的格式更改代码内容。

首先从https://sm.ms/ 中的*User*下找到*Dashboard*，在*API Token*中复制*Secret Token*。

在 ./botpy/examples/config.yaml 中，找到

```yaml
picturesToken: "Your_Token"
```

将其替换上述的*Your_Token*。

### 启动机器人

非常棒！你已经完成了全部配置过程！

现在，进入 ./botpy/examples/ 路径，找到*client.py*，在终端输入

```powershell
python client.py
```

启动机器人。

## 注意
`mtrpath`和`mtrpath_beta`都是修改过的版本，其中第一个是旧版本，第二个是新版本。

代码默认使用的是新版本，注释掉的代码是旧版本。

## 开源协议
与寻路程序原作者达成协议，决定用`GPLv3`开源协议。

## 错误
如果出现任何错误，请提交在Issue，谢谢！
