@echo off

::获取管理员权限
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"

echo config IPv4 and MTU of local machine to work flexiblely, the goal of changing the MTU is to access company git

::修改本机IP
netsh interface ip set address "WLAN" static 192.168.10.126 255.255.255.0 192.168.10.1

::修改DNS
netsh interface ip set dns "WLAN" static 8.8.8.8 primary

::修改本机MTU以访问公司git
netsh interface ipv4 set subinterface "WLAN" mtu=1420
