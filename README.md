# qq_retweet_bot
使用 Python 编写和 CoolQ 第三方 QQ 应用程序的 QQ 转推机器人脚本

## 安装
0. 安装Wine、Docker
1. 安装Tweepy
<pre><code>pip install tweepy</pre></code>
2. 安装<a href="https://cqp.cc/">酷Q</a>（只有酷Q Pro版本才有搬图功能，如不需要可自行删除相关代码）

3. 安装<a href="https://cqhttp.cc/">CQHTTP</a>，并将上报端口地址设置为5700，或在代码中自行更改
4. 设置系统Crontab服务每隔一段时间运行一次
<pre><code>vi /etc/crontab
*/time  *  *  * <user> /<path-to-file></pre></code>

## 使用

### 推文类型
推文分为一般推文、带媒体推文、转推、评论和转发并评论。他们在转推机中的格式是：
一般推文：正文内容
1. 带媒体推文：正文内容+媒体链接（Pro 版可搬图）
2. 转推：默认不搬，RT+正文内容
3. 评论：@[用户名]+正文内容
4. 转发并评论：正文内容+原推链接

### 工作方式
机器人在收到运行命令后首先通过 Twitter API 获取某用户最新推文内容，然后判断并提取图片链接，并通过运行中的酷 Q 插件 CQHttp 的 API 发送消息到指定 QQ 群，并发送图片。最后会在服务器留下一个与推文用户名相同的缓存文件，记录推文的 id 以用于判断是否已转发最新推文。

### 妥协
1. 由于腾讯未提供 API，故无法自动发送到 QQ 空间。
2. 转发并评论的原推文无法自动转发。因为每条推文只有推文正文、id、媒体内容等信息（https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json），原推文只提供链接。而我暂时无法通过链接获得推文内容，而且转发并评论可能是嵌套的，无法遍历所有转发并评论内容。故只能以链接的形式挂在推文最后。
3. 图片的推文链接无法去除。
