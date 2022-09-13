# delay-test

> PyQt project.

## 介绍

基于PySide6、easyocr开发的延时测试工具

### Developer

[FanHao](http://alanfanh.github)

### 项目结构

````text
delay-test
|
|--common
|  |---common.py    # 通用函数
|  |---gui.ui       # gui文件
|  |---gui.py       # 界面源码
|
|--image            # 图片目录
|--model            # 数据模型目录
|
|--main.py          # 界面主线程,工作子线程,核心处理逻辑,项目入口
|--readme.md        # 说明文件
|
````

## 环境

> python3.9.2 64bit

### 依赖

> 可使用"pip install -r requirements.txt"一键安装所有依赖项

````text
pyside6==6.2.1
easyocr==1.6.0
````