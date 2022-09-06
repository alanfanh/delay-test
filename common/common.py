# author:Fanhao
# 通过adb命令控制手机拍照，并将手机拍的照片存放到/image目录下
import os


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
        take = 'adb -s ' + id + 'input keyevent 27'
        res = os.popen(cmd).read()
        if "act=android.media.action.STILL_IMAGE_CAMERA" in res:
            result=os.popen(cmd).read()
            return len(result)==0
        else:
            print("Error!未打开相机")
            return False
    except Exception as e:
        print('命令执行报错',e)

