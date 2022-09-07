# author:Fanhao
# 通过adb命令控制手机拍照，并将手机拍的照片存放到/image目录下
import sys
import os
import time

def get_device_id() -> str:
    # 获取设备ID
    try:
        cmd = 'adb devices'
        res = os.popen(cmd).read()
        id = res.split('\n')[1].split('\t')[0]
        print(id)
        return id
    except Exception as e:
        print("获取设备ID失败",e)
        return False

def is_screen_on(id) -> bool:
    # 判断手机屏幕是否点亮
    try:
        cmd = 'adb -s ' + id + ' shell dumpsys window policy ^| grep screenState'
        res = os.popen(cmd).read()
        if "screenState=SCREEN_STATE_ON" in res:
            return True
        else:
            return False
    except Exception as e:
        print("获取手机屏幕点亮状态异常",e)
        return False

def unlock_phone(id) -> bool:
    # 点亮并滑动解锁
    try:
        cmd = 'adb -s ' + id + ' shell input keyevent 26'
        unlock = 'adb -s ' + id + ' shell input swipe 200 900 200 120'
        if not is_screen_on(id):
            res = os.popen(cmd).read()
            if res.strip() == '' and is_screen_on(id):
                os.popen(unlock)
                return True
        else:
            os.popen(unlock)
            return True
    except Exception as e:
        print("滑动解锁失败",e)
        return False

def take_photo(id) -> bool:
    # 打开相机拍照
    try:
        cmd = 'adb -s ' + id + ' shell am start -a android.media.action.STILL_IMAGE_CAMERA'
        take = 'adb -s ' + id + ' shell input keyevent 27'
        res = os.popen(cmd).read()
        if "act=android.media.action.STILL_IMAGE_CAMERA" in res:
            time.sleep(0.8)
            result=os.popen(take).read()
            return len(result)==0
        else:
            print("Error!未打开相机")
            return False
    except Exception as e:
        print('命令执行报错',e)

def get_photo(id, file):
    """
    # 控制手机拍照完成后，最好等待2s使手机生成照片
    id: 设备adb标识
    file: PC上文件保存路径和文件名。eg:file='E:\image\test.jpg'
    """
    # 获取最新的一张照片
    cmd = "adb -s " +id+" shell ls -t /storage/emulated/0/DCIM/Camera/  ^| grep '.jpg' ^| head -n 1 ^| awk '{print $1}'"
    try:
        res = os.popen(cmd).read()
        if '.jpg' in res:
            down = "adb pull /storage/emulated/0/DCIM/Camera/"+res.strip() +" "+ file
            result = os.popen(down).read()
            if "pulled" in result:return True
    except Exception as e:
        print("获取照片命令执行失败",e)

def get_screencap(id):
    # 截图
    cmd = 'adb -s ' +id+' shell /system/bin/screencap -p /sdcard/screenshot.png'
    down = 'adb pull /sdcard/screenshot.png E:\screenshot.png'
    try:
        res = os.open(cmd).read()
        if res.strip() == '':os.popen(down)
    except Exception as e:
        print("截图动作失败",e)


def cur_file_dir():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录
    # 如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)