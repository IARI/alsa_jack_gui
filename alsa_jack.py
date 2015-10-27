import sys
from gui import Gui
from qtsingleapplication import QtSingleApplication


appGuid = '58B37CBA-BE8F-4483-965C-5E2ED0C90D54'
app = QtSingleApplication(appGuid, sys.argv)
if app.isRunning():
    print("Running already")
    sys.exit(0)

gui = Gui()
app.setActivationWindow(gui)
sys.exit(app.exec_())