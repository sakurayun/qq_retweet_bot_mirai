# qq_retweet_bot
使用 Python 编写和 CoolQ 第三方 QQ 应用程序的 QQ 转推机器人脚本

## 使用方法
0. 安装Wine、Docker
1. 安装Tweepy
<pre><code>pip install tweepy</pre></code>
2. 安装<a href="https://cqp.cc/">酷Q</a>（只有酷Q Pro版本才有搬图功能，如不需要可自行删除相关代码）

3. 安装<a href="https://cqhttp.cc/">CQHTTP</a>，并将上报端口地址设置为5700，或在代码中自行更改
4. 设置系统Crontab服务每隔一段时间运行一次

## 其他
脚本会创建一个 Last_id 缓存文件，请勿删除
