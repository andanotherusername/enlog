import os, sys
from shutil import move, copyfile

LOGFILE=os.environ["HOME"]+"/enlog.log"

def curl_ix(error, content=[]):
    # Provide a filename to generate a ix.io link
    # import necesssary classes and functions
    from pycurl import Curl
    from io import BytesIO
    from urllib.parse import urlencode
    curl=Curl()
    buf=BytesIO()
    curl.setopt(curl.URL, "ix.io")
    curl.setopt(curl.WRITEDATA, buf)
    if content==[]:
        try:
            content=open(LOGFILE, 'r').readlines()
        except FileNotFoundError:
            error(f"{LOGFILE} not found.")
    curl.setopt(curl.POSTFIELDS, urlencode({"f:1": '\n'.join(content)}))
    try:
        curl.perform()
    except Exception as e:
        error(str(e))
    curl.close()
    return buf.getvalue().decode().strip()

def run(error, cmd, shell=True):
    import subprocess
    _return=subprocess.run(cmd.split(), shell=shell, capture_output=True)
    try:
        _return.check_returncode()
    except subprocess.CalledProcessError:
        error(f"{cmd} run failed\n{_return.stderr.decode()}")
        sys.exit(1)
    return _return.stdout.decode()

def userNames(low, high):
    import pwd
    users=[]
    for struct in pwd.getpwall():
        if low <= struct.pw_uid <= high:
            users.append(struct.pw_name)
    return users

def removePersonalData(error, content=[]):
    FILE=False
    if content==[]:
        if not os.path.isfile(LOGFILE):
            error(f"{LOGFILE} not found.\nPlease file a bug report if necessary.")
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
    from PyQt5 import QtWidgets
    import main_
    app=QtWidgets.QApplication(sys.argv)
    e=QtWidgets.QErrorMessage()
    error=lambda msg: e.showMessage(msg)
    main_window=QtWidgets.QMainWindow()
    ui=main_.MainUI()
    ui.initUI(main_window)

    # Handle checkboxes
    def handle(error, do):
        outputs=[]
        if ui.checkBox.isChecked():
            # journalctl -b -0
            outputs.append(run(error, "journalctl -b -o"))
        if ui.checkBox_2.isChecked():
            # journalctl -b -1
            outputs.append(run(error, "journalctl -b -1"))
        if ui.checkBox_3.isChecked():
            # journalctl -b -2
            outputs.append(run(error, "journalctl -b -2"))
        if ui.checkBox_4.isChecked():
            # .xsession-errors
            try:
                with open(os.environ["HOME"]+"/.xsession-errors", 'r') as f:
                    outputs.append(f.read())
            except FileNotFoundError:
                error(".xsession.error file not  found")
        if ui.checkBox_5.isChecked():
            # /var/lov/Xorg.0.log
            try:
                with open("/var/log/Xorg.0.log", 'r') as f:
                    outputs.append(f.read())
            except FileNotFoundError:
                error("/var/log/Xorg.0.log file not  found")
        if ui.checkBox_6.isChecked():
            # /var/log/lightdm/lightdm.log
            outputs.append(run(error, "pkexec cat /var/log/lightdm/lightdm.log", shell=False))
        if ui.checkBox_7.isChecked():
            # /var/log/lightdm/x-0.log
            outputs.append(run(error, "pkexec cat /var/log/lightdm/x-0.log", shell=False))
        if ui.checkBox_8.isChecked():
            # /var/log/Calamares.log
            try:
                with open("/var/log/Calamares.log", 'r') as f:
                    outputs.append(f.read())
            except FileNotFoundError:
                error("/var/log/Calamares.log file not  found")
        if ui.checkBox_10.isChecked():
            # systemd-analyze blame
            outputs.append(run(error, "systemd-analyze blame", shell=False))
        if ui.checkBox_9.isChecked():
            # lspci -vnn
            outputs.append(run(error, "lspci -vnn"))
        if ui.checkBox_11.isChecked():
            # lsusb
            outputs.append(run(error, "lsusb"))
        if ui.checkBox_12.isChecked():
            # hwinfo --short
            outputs.append(run(error, "hwinfo --short"))

        if do=="link":
            outputs=removePersonalData(error, outputs)
            url=curl_ix(error, outputs)
            error(url)
        elif do=="local":
            if ui.radioButton.isChecked():
                outputs=removePersonalData(error, outputs)
            if os.path.isfile(LOGFILE):
                move(LOGFILE, f"{LOGFILE}.bak")
            with open(LOGFILE, 'w') as f:
                for x in outputs:
                    f.write(x)

    ui.pushButton.clicked.connect(lambda: handle(error, "link"))
    ui.pushButton_2.clicked.connect(lambda: handle(error, "local"))
    main_window.show()

    sys.exit(app.exec_())

if __name__=="__main__":
    main()