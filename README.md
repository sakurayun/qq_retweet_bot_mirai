# qq_retweet_bot_mirai
## 关于此fork
由于CoolQ停止服务，此fork将项目修改以适配Mirai-api-Http，并添加翻译功能(需要ApiKey)，简化终端输出。如需访问CoolQ版本，请[返回原Repo](https://github.com/xiofan2/qq_retweet_bot "xiofan2/qq_retweet_bot")

## 配置
1. 安装python3
2. 安装tweepy
3. 下载MiraiOK
4. 下载、安装并按官方教程配置Mirai-Api-HTTP
5. clone本项目，填写自己的apikey、服务器地址、token等信息。在末尾填写转推列表
6. 测试，在Windows环境下可以使用计划任务来定时运行

## 感谢
[xiofan2/qq_retweet_bot](https://github.com/xiofan2/qq_retweet_bot)

[project-mirai/mirai-api-http](https://github.com/project-mirai/mirai-api-http)

[mamoe/mirai](https://github.com/mamoe/mirai/tree/master)

特别感谢andropig(立方爹)debug
---
# qq_retweet_bot
使用 Python 编写和 CoolQ 的 QQ 转推机器人脚本

## 安装
请准备好VPS和Twitter开发者账号的keys and Tokens以用于设置

0. 安装<a href="https://www.winehq.org/">Wine</a>、<a href="https://www.docker.com/">Docker</a>
1. 安装Tweepy
<pre><code>pip install tweepy</pre></code>
2. 安装<a href="https://cqp.cc/">酷Q</a>（只有酷Q Pro版本才有搬图功能）

3. 安装<a href="https://cqhttp.cc/">CQHTTP</a>，并将上报端口地址设置为5700，或在代码中自行更改
4. 设置系统Crontab服务每隔一段时间运行一次
<pre><code>vi /etc/crontab</pre></code>
并在文件最后一行添加以下内容
<pre><code>*/time  *  *  * [user] /[path-to-file]</pre></code>

## 使用

填入Twitter Keys and Tokens、更改retweet函数的参数以设置转推的用户、是否带图、是否识别标签
<pre><code>retweet('推特screen_name','用户在现实中的名字',QQ群号,['仅搬运该标签内容']或0（不识别）,0（重复推文内容）/1（不重复推文内容）,0（不带图）/1（带图，酷Q Air版用户填1会报错）)</pre></code>

### 推文类型
推文分为一般推文、带媒体推文、转推、评论和转发并评论。他们在转推机中的格式是：
一般推文：正文内容
1. 带媒体推文：正文内容+媒体链接（酷Q Pro 版可搬图）
2. 转推：默认不搬，RT+正文内容
3. 评论：@[用户名]+正文内容
4. 转发并评论：正文内容+原推链接

### 工作方式
机器人在收到运行命令后首先通过 Twitter API 获取某用户最新推文内容，然后判断并提取图片链接，并通过运行中的酷 Q 插件 CQHttp 的 API 发送消息到指定 QQ 群，并发送图片。最后会在服务器留下一个与推文用户名相同的缓存文件，记录推文的 id 以用于判断是否已转发最新推文。
