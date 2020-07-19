import os, sys
import pyperclip
from shutil import move, copyfile

LOGFILE=os.environ["HOME"]+"/enlog.log"
ERROR=None

def curl_ix(content=[]):
    # Provide a filename to generate a ix.io link
    # import necesssary classes and functions
    global ERROR
    from pycurl import Curl
    from io import BytesIO
    from urllib.parse import urlencode
    curl=Curl()
    buf=BytesIO()
    curl.setopt(curl.URL, "ix.io")
    curl.setopt(curl.WRITEDATA, buf)
    if content==[]:
        try:
            with open(LOGFILE, 'r') as f:
                content=f.readlines()
        except FileNotFoundError:
            ERROR(f"{LOGFILE} not found.")
        except Exception as e:
            ERROR(f"Error occured:\n{str(e)}")
    curl.setopt(curl.POSTFIELDS, urlencode({"f:1": '\n'.join(content)}))
    try:
        curl.perform()
    except Exception as e:
        ERROR(f"Error occured:\n{str(e)}")
    curl.close()
    return buf.getvalue().decode().strip()

def run(cmd, shell=True):
    global ERROR
    import subprocess
    _return=subprocess.run(cmd.split(), shell=shell, capture_output=True)
    try:
        _return.check_returncode()
    except subprocess.CalledProcessError:
        ERROR(f"{cmd} run failed\n{_return.stderr.decode()}")
    except Exception as e:
        ERROR(f"Error occured:\n{str(e)}")
    return _return.stdout.decode()

def userNames(low, high):
    import pwd
    users=[]
    for struct in pwd.getpwall():
        if low <= struct.pw_uid <= high:
            users.append(struct.pw_name)
    return users

def removePersonalData(content=[]):
    global ERROR
    FILE=False
    if content==[]:
        if not os.path.isfile(LOGFILE):
            ERROR(f"{LOGFILE} not found.\nPlease file a bug report if necessary.")
        FILE=True
        from tempfile import NamedTemporaryFile
        with open(LOGFILE, 'r') as f:
            content=f.readlines()
        _file=NamedTemporaryFile(delete=False)
        copyfile(LOGFILE, f"{LOGFILE}.bak")
    from re import sub
    from socket import gethostname
    result=[]
    for line in content:
        for user in userNames(1000, 50000):
            x=sub(user, "_user_", line)
            x=sub(gethostname(), "_hostname_", x)
            result.append(x)
    
    if FILE:
        for x in result:
            _file.write(x.encode())
        _file.close()
        move(_file.name, LOGFILE)
    else:
        return result

def main():
    # Get the gui up and do everything
    global ERROR
    from PyQt5 import QtWidgets, QtGui, QtCore
    from enui.EnUI import MainUI
    
    app=QtWidgets.QApplication(sys.argv)
    main_window=QtWidgets.QMainWindow()
    ui=MainUI()
    ui.initUI(main_window)
    url=""
    # Icon
    icon=QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("/usr/share/endeavouros/EndeavourOS-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    # Error handler
    error=QtWidgets.QMessageBox()
    error.setWindowTitle("enlog error")
    error.setWindowIcon(icon)
    error.setIcon(QtWidgets.QMessageBox.Critical)
    error.buttonClicked.connect(lambda: sys.exit(1))
    ERROR=lambda msg: error.setText(msg) or error.show()
    # URL handler
    msg_=QtWidgets.QMessageBox()
    msg_.setWindowTitle("Log URL")
    msg_.setWindowIcon(icon)
    msg_.buttonClicked.connect(lambda: pyperclip.copy(url))
    showUrl=lambda msg: msg_.setText(msg+"\nClick on to copy it to clipboard") or msg_.show()
    # Message handler
    end=QtWidgets.QMessageBox()
    end.setWindowTitle("Success")
    end.setWindowIcon(icon)
    notify=lambda: end.setText("Log file created.\nPersonal data was"+(" " if ui.radioButton.isChecked() else " not ")+"removed.") or end.show()

    # Handle checkboxes
    def handle(do):
        outputs=[]
        global ERROR
        HEADER=lambda cmd: "#"*25+"  "+cmd+"  "+"#"*25+"\n"
        FOOTER="\n\n"
        add=lambda cmd, shell=True: outputs.append(HEADER(cmd)) or outputs.append(run(cmd, shell)) or outputs.append(FOOTER)
        if ui.checkBox.isChecked():
            cmd="journalctl -b -0"
            add(cmd)
        if ui.checkBox_2.isChecked():
            cmd="journalctl -b -1"
            add(cmd)
        if ui.checkBox_3.isChecked():
            cmd="journalctl -b -2"
            add(cmd)
        if ui.checkBox_4.isChecked():
            cmd=".xsession-errors"
            outputs.append(HEADER)
            try:
                with open(os.environ["HOME"]+"/.xsession-errors", 'r') as f:
                    outputs.append(f.read())
            except FileNotFoundError:
                ERROR(".xsession.error file not  found")
            outputs.append(FOOTER)
        if ui.checkBox_5.isChecked():
            cmd="/var/lov/Xorg.0.log"
            outputs.append(HEADER)
            try:
                with open("/var/log/Xorg.0.log", 'r') as f:
                    outputs.append(f.read())
            except FileNotFoundError:
                ERROR("/var/log/Xorg.0.log file not  found")
            outputs.append(FOOTER)
        if ui.checkBox_6.isChecked():
            cmd="pkexec cat /var/log/lightdm/lightdm.log"
            add(cmd, False)
        if ui.checkBox_7.isChecked():
            cmd="pkexec cat /var/log/lightdm/x-0.log"
            add(cmd, False)
        if ui.checkBox_8.isChecked():
            cmd="/var/log/Calamares.log"
            outputs.append(HEADER)
            try:
                with open("/var/log/Calamares.log", 'r') as f:
                    outputs.append(f.read())
            except FileNotFoundError:
                ERROR("/var/log/Calamares.log file not  found")
            outputs.append(FOOTER)
        if ui.checkBox_10.isChecked():
            cmd="systemd-analyze blame"
            add(cmd, False)
        if ui.checkBox_9.isChecked():
            cmd="lspci -vnn"
            add(cmd)
        if ui.checkBox_11.isChecked():
            cmd="lsusb"
            add(cmd)
        if ui.checkBox_12.isChecked():
            cmd="hwinfo --short"
            add(cmd)

        if do=="link":
            nonlocal url
            url=curl_ix(removePersonalData(outputs))
            if url!="":
                showUrl(url)
        elif do=="local":
            if os.path.isfile(LOGFILE):
                move(LOGFILE, f"{LOGFILE}.bak")
            if ui.radioButton.isChecked():
                outputs=removePersonalData(outputs)
            with open(LOGFILE, 'w') as f:
                for x in outputs:
                    f.write(x)
            notify()

    ui.pushButton.clicked.connect(lambda: handle("link"))
    ui.pushButton_2.clicked.connect(lambda: handle("local"))

    main_window.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()