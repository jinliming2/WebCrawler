# Web Crawler [![TravisCI Build Status](https://travis-ci.org/772807886/WebCrawler.svg?branch=master)](https://travis-ci.org/772807886/WebCrawler) [![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/3ncbuauq10i1ugsf?svg=true&retina=true)](https://ci.appveyor.com/project/LimingJin/webcrawler) [![Coverage Status](https://coveralls.io/repos/github/772807886/WebCrawler/badge.svg?branch=master)](https://coveralls.io/github/772807886/WebCrawler?branch=master)
[![Developing](https://img.shields.io/badge/Web%20Crawler-developing-yellow.svg)](https://github.com/772807886/WebCrawler)
[![GitHub license](https://img.shields.io/badge/license-AGPL-blue.svg)](https://raw.githubusercontent.com/772807886/WebCrawler/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/772807886/WebCrawler.svg)](https://github.com/772807886/WebCrawler/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/772807886/WebCrawler.svg)](https://github.com/772807886/WebCrawler/network)
[![GitHub issues](https://img.shields.io/github/issues/772807886/WebCrawler.svg)](https://github.com/772807886/WebCrawler/issues)

A Web Crawler Written in Python 3, Get images from website.

# Usage
* Firstly, Clone this repository using git.
```
git clone https://github.com/772807886/WebCrawler.git
cd WebCrawler
```
* Secondly, Restore dependency modules.
```
pip install -r .\requirements.txt
```
* Run use python(Recommend Python 3).
```
py main.py http://www.example.com
```

# Arguments
|Argument|Requirement|Need Value|Default Value|Introduce|
|:---:|:---:|:---:|:---:|:---:|
|url|[x]|[x]| |Start from here.|
|unsafe|[ ]|[ ]|False|Ignore the https certificate check.|
|deep|[ ]|[x]|5|Crawl depth.|
|thread|[ ]|[x]|10|The number of threads.|
|parent|[ ]|[ ]|False|Crawl parent pages.(depth less than start.)|
|timeout|[ ]|[x]|30|Load timeout.|
|download|[ ]|[ ]|False|Download image files.|
|database|[ ]|[x]|./crawler_{$Y}{$M}{$D}{$H}{$m}{$s}.db|Log database.|

### Example
* Unsafe mode
```
py main.py http://www.example.com -unsafe
```
* Download image files
```
py main.py http://www.example.com -download
```
* Set Crawl depth
```
py main.py http://www.example.com -deep 1
```

# Constants
|Constant|Introduce|
|:---:|:---:|
|Y|Year|
|M|Month|
|D|Date|
|H|Hour|
|m|Minute|
|s|Second|

### Example
* Save log to `./log_2016-10-14 18-05-30.db`
```
py main.py http://www.example.com -database "log_{$Y}-{$M}-{$D} {$H}-{$m}-{$s}.db"
```
