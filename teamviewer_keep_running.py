import os
from PIL import ImageGrab
import time
import threading
import paramiko
import settings_file
import send_screenshot_mail
import subprocess

event = threading.Event()

#run bat script to set gateway to .1
print ("run bat script to set gateway to .1")
p = subprocess.Popen("cmd.exe /c" + "C:\\Users\\26989\\software\\teamviwer_auto_running\\worknet-gw1.bat", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

class WriteScreenShotToServer(object):
    def __init__(self):
        self.remote_host = settings_file.REMOTE_HOST
        self.remote_port = settings_file.REMOTE_PORT
        self.remote_user = settings_file.REMOTE_USER
        self.remote_pwd = settings_file.REMOTE_PWD

    def call_back(self,size,file_size):
        print ("screenshot has upload to sever xx.xx.xx.xx")
    
    def upload_screenshot_to_server(self, local_path, dest_file_name):
        transport = paramiko.Transport((self.remote_host, self.remote_port))
        transport.connect(username = self.remote_user, password = self.remote_pwd)

        sftp = paramiko.SFTPClient.from_transport(transport)

        remote_save_path = settings_file.SAVE_PATH
        try:
            sftp.stat(remote_save_path)
            print ("the path to save screenshot in server exist")
        except Exception as e:
            print ("the path not exist, now to create it")
            folder = remote_save_path
            sftp.mkdir("/home/zhangben/teamviewer_screenshot/")
            print ("finish creating")

        remote_save_file_name = remote_save_path + '/' + dest_file_name
        sftp.put(local_path, remote_save_file_name, self.call_back)

        transport.close()

def copy_screenshot_to_server():
    local_path = 'C:\\Users\\26989\\software\\teamviwer_auto_running\\account_pswd.jpg'
    dest_file_name = 'teamviewer_screenshot.jpg'
    screenshot = WriteScreenShotToServer()
    screenshot.upload_screenshot_to_server(local_path, dest_file_name)

def send_screenshot_to_mail():
    send_screenshot_mail.send_mail()

def screenshot_to_server_and_mail():
    while True:
        event.wait()
        if event.is_set():
            time.sleep(20)
            print ("save the sreenshot to aviod accident")
            teamviewer_screenshot = ImageGrab.grab()
            teamviewer_screenshot.save('C:\\Users\\26989\\software\\teamviwer_auto_running\\account_pswd.jpg','jpeg')
            print ("copy the screenshot to server xx.xx.xx.xx to avoid accident")
            copy_screenshot_to_server()
            print ("send the email with screenshot to avoid accident")
            send_screenshot_to_mail()
            event.clear()

def run_teamviewer():
    while True:
        cmd = 'tasklist |find /i "teamviewer.exe"'
        p = os.popen(cmd)
        res = p.read()
        if "TeamViewer" not in res:
            print ("teamviewer is NOT running, now run teamviewer")
            event.set()
            os.chdir(r'C:\Program Files (x86)\TeamViewer')
            os.system('Teamviewer.exe')

teamviewer_run = threading.Thread(target=run_teamviewer,)
teamviewer_run.start()

screenshot = threading.Thread(target=screenshot_to_server_and_mail,)
screenshot.start()
