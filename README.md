# crawl-JD-app
使用京东app，输入要查找的商品名，捕获相关商品信息和买家评价，并保存到本地MongoDB数据库

## 环境要求：<br>
python3，mitmproxy,appium,Android模拟器or真机，MongoDB

## 使用步骤：<br>
1、启动监听
  mitmdump -s MitmJD.py<br>
2、执行UI操作
  python appiumJD.py<br>
