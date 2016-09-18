## Deploy spider using Scrapyd


0. install scrapyd

```shell
pip install scrapyd
```

1. Starting Scrapyd

```shell
scrapyd
``` 
Sracpyd is a service daemon to run Scrapy spiders


edit ```scrapy.cfg```
```shell
[deploy:MySpider]
url = http://localhost:6800/
project = AirQuality
```

check scrapyd status
```shell
scrapy deploy -l
```

2. Deploy spider project
```shell
scrapy deploy <target> -p <project>
```
```shell
scrapy deploy MySpider -p AirQuality
```

3. Scheduling a spider run

```shell
$ curl http://localhost:6800/schedule.json -d project=AirQuality -d spider=AqiSpider
```

## Scrapyd 与 scrapyd-client

scrapyd是一个守护进程，监听爬虫的运行和请求，然后启动进程来执行它们， 
启动服务
```shell
scrapyd
```
scrapyd-client提供scrapyd-deploy工具
安装scrapyd-client
```shell
pip install scrapyd-client
```

### 配置服务器信息

编辑```scrapy.cfg```文件

检查配置
```shell
scrapyd-deploy -l
```

### 部署项目
```shell
scrapyd-deploy <target> -p <project>
```
```shell
scrapyd-deploy MySpider -p AirQuality
```

