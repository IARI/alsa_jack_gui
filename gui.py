"""
Gui
"""
from PyQt5.QtWidgets import (QMainWindow, QListWidgetItem)

# QWidget, QFileDialog, QAction,
# QActionGroup, QMessageBox, QApplication

from PyQt5.QtCore import QObject, QSettings  # , Qt
# from PyQt5.QtGui import QIcon
from gui_ui import Ui_MainWindow
import json
from interface import DeviceList


class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


class DevWidgetItem(QListWidgetItem):
    FORMAT_ACTIVE = {
        True: "{detail} ({delay})",
        False: "{detail}"
    }

    def __init__(self, device):
        # QObject.__init__(self)
        super(DevWidgetItem, self).__init__()
        self.device = device
        self.updateText()
        device.audio_proc.delay_changed.connect(self.updateText)
        device.audio_proc.log_message.connect(print)

    def updateText(self, delay='Off'):
        formatString = self.FORMAT_ACTIVE[self.isSelected()]
        self.setText(formatString.format(detail=self.device.detail,
                                         delay=delay))

    def update_audio_proc(self):
        self.device.audio_proc.setActive(self.isSelected())


class GuiDeviceList:
    def __init__(self, devlist, listWidget):
        self.devlist = devlist
        self.listWidget = listWidget
        self.itemDict = {}
        # noinspection PyUnresolvedReferences
        self.listWidget.itemSelectionChanged.connect(self.update_audio_procs)

    def update(self):
        self.devlist.update()
        self.update_widget()

    def update_widget(self):
        self.listWidget.clear()
        self.itemDict.clear()
        for d in self.devlist:
            this_item = DevWidgetItem(d)
            self.listWidget.addItem(this_item)

            self.itemDict[d.hw] = this_item
            #    # this_item.setFlags(this_item.flags() | Qt.ItemIsEditable)

    @property
    def items(self):
        return map(self.listWidget.item, range(self.listWidget.count()))

    @property
    def selection_json(self):
        s_list = [i.device.detail for i in self.items if i.isSelected()]
        return json.dumps(s_list)

    @selection_json.setter
    def selection_json(self, list_str):
        s_list = json.loads(list_str)
        for i in self.items:
            s = i.device.detail in s_list
            if s:
                print("selecting " + i.device.detail)
            i.setSelected(s)

    def update_audio_procs(self):
        for i in self.items:
            i.update_audio_proc()


class Gui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QObject.__init__(self)
        super(Gui, self).__init__()
        self.setupUi(self)
        self.show()
        devs_play = DeviceList('aplay -l')
        devs_record = DeviceList('arecord -l', True)
        self.play = GuiDeviceList(devs_play, self.list_play)
        self.record = GuiDeviceList(devs_record, self.list_record)

        self.settings = QSettings('alsa_jack', 'playback')
        self.play.update()
        self.record.update()

        if self.settings.contains('playback'):
            self.play.selection_json = self.settings.value('playback')
        if self.settings.contains('record'):
            self.record.selection_json = self.settings.value('record')


        # noinspection PyUnresolvedReferences
        self.btn_update_playback.clicked.connect(self.play.update)
        # noinspection PyUnresolvedReferences
        self.btn_update_record.clicked.connect(self.record.update)

        self.btn_dc_all.clicked.connect(self.clearSelection)

    def clearSelection(self):
        self.list_play.clearSelection()
        self.list_record.clearSelection()

    def update_record(self):
        self.record.update()
        self.update_lists()

    def closeEvent(self, event):
        self.settings.setValue('playback', self.play.selection_json)
        self.settings.setValue('record', self.record.selection_json)
        self.play.devlist.stop()
        self.record.devlist.stop()
        print('closing')
