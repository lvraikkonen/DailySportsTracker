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