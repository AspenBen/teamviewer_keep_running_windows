this program supports windows currently.

The program can keep teamviewer running always.

logic:
A thread in the program will watch teamviewer whether is ruuning, send a signal and cut screenshot to the path we pointed when teamviewer doesn't run.
The signal will triger another thread which will copy the screenshot to remote server and send the screenshot to mail we set.
The screenshot have info including teamviewer ID and password.
