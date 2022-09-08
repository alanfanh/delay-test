# author:Fanhao
# 2022-8-31
# 
import sys
import re
import easyocr
from PySide6.QtCore import SIGNAL
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow
from common.gui import Ui_MainWindow
from common.common import *

class Thread(QtCore.QThread):
    def __init__(self, parent) -> None:
        super(Thread,self).__init__(parent)
        # 主GUI线程
        self.parent = parent

    def get_easy_text(self, img):
        reader = easyocr.Reader(['ch_sim','en'],gpu=False,model_storage_directory='./model')
        result = reader.readtext(img, detail=0)
        return result

    def run(self):
        text = self.get_easy_text(self.parent.img)
        list_num = []
        if text:
            print(text)
            for i in text:
                if re.match('^\d{2}时\d{2}分\d{2}秒\d{3}.秒$',i):
                    list_num.append(i)
            if len(list_num)==2:
                self.parent.ui.textBrowser.append("第一次计时:"+list_num[0])
                self.parent.ui.textBrowser.append("第二次计时:"+list_num[1])
                a_time = list(map(int, re.findall(r'\d+',list_num[0])))
                b_time = list(map(int, re.findall(r'\d+',list_num[1])))
                res_time=[]
                for j in range(len(a_time)):
                    res_time.append(b_time[j]-a_time[j])
                s = str(res_time[0])+"时"+str(res_time[1])+"分"+str(res_time[2])+"秒"+str(res_time[3])+"毫秒"
                self.parent.ui.textBrowser.append("延时如下：")
                self.parent.ui.textBrowser.append(s)
                self.parent.statusBar().showMessage("图片识别成功，结果如上所示")
            else:
                self.parent.ui.textBrowser.append("未识别出2次计时")
            print(list_num)

    def start_test(self):
        self.start()

    def stop_test(self):
        self.terminate()
        self.wait()

class RunThread(QtCore.QThread):
    # 
    def __init__(self, parent) -> None:
        super(RunThread,self).__init__(parent)
        self.parent = parent

    def get_easy_text(self, img):
        reader = easyocr.Reader(['ch_sim','en'],gpu=False,model_storage_directory='./model')
        result = reader.readtext(img, detail=0)
        return result

    def run(self):
        """
        调用手机拍照，存入指定文件夹；然后读取此图片识别，并输出文字
        """
        path = cur_file_dir()
        file = path+'./image/test.jpg'
        try:
            id = get_device_id()
            time.sleep(0.2)
            if unlock_phone(id):
                time.sleep(1)
                res = take_photo(id)
                time.sleep(2)
            if res:
                get_photo(id,file)
        except Exception as e:
            return False
        # 判断image目录下是否存在从手机中获取的照片
        if os.path.isfile('./image/test.jpg'):
            text = self.get_easy_text('./image/test.jpg')
            list_num = []
            if text:
                print(text)
                for i in text:
                    if re.match('^\d{2}时\d{2}分\d{2}秒\d{3}.秒$',i):
                        list_num.append(i)
                if len(list_num)==2:
                    self.parent.ui.textBrowser.append("第一次计时:"+list_num[0])
                    self.parent.ui.textBrowser.append("第二次计时:"+list_num[1])
                    a_time = list(map(int, re.findall(r'\d+',list_num[0])))
                    b_time = list(map(int, re.findall(r'\d+',list_num[1])))
                    res_time=[]
                    for j in range(len(a_time)):
                        res_time.append(b_time[j]-a_time[j])
                    s = str(res_time[0])+"时"+str(res_time[1])+"分"+str(res_time[2])+"秒"+str(res_time[3])+"毫秒"
                    self.parent.ui.textBrowser.append("延时如下：")
                    self.parent.ui.textBrowser.append(s)
                    self.parent.statusBar().showMessage("图片识别成功，结果如上所示")
                else:
                    self.parent.ui.textBrowser.append("未识别出2次计时")
                print(list_num)
        else:
            self.parent.statusBar().showMessage("没有找到图片，请检查image目录下是否存在test.jpg")

    def start_run(self):
        self.start()

    def stop_run(self):
        self.terminate()
        self.wait()

class Form(QMainWindow):
    def __init__(self, parent=None) -> None:
        super(Form, self).__init__(parent)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("60Ghz毫米波延时测试程序")
        self.img=''
        # 连接信号与槽函数
        self.connect(self.ui.img, SIGNAL("clicked()"), self.select_img)
        self.connect(self.ui.run, SIGNAL("clicked()"), self.start_run)
        self.connect(self.ui.actionhelp, QtCore.SIGNAL("triggered()"), self.help)
        self.connect(self.ui.running, SIGNAL("clicked()"), self.start_running)
        # 子线程
        self.run_thread = Thread(self)
        self.running_thread = RunThread(self)

    def select_img(self):
        print('clicked')
        file_name,_ = QtWidgets.QFileDialog.getOpenFileName(None,"选取文件夹","C:/")  # 起始路径
        self.img = file_name
        print(self.img,type(self.img))
        self.ui.file.setText(file_name)
        self.statusBar().showMessage("已选择文件")

    def help(self):
        QtWidgets.QMessageBox.about(self,u"帮助信息",u"Auther: FanHao\n1.仅支持jpg,jpeg,bmp,png等格式图片\n2.图片不宜过大,2MB以下最好\n3.图片最好保证数字清晰可见,不模糊以达到最好识别效果")

    def start_run(self):
        a = re.findall('^.*\.(jpg|jpeg|bmp|png)$',self.img)
        if not a:
            self.statusBar().showMessage("请选择图片")
        else:
            self.statusBar().showMessage("程序正在运行，识别图片中")
            self.run_thread.start_test()

    def start_running(self):
        self.running_thread.start_run()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
