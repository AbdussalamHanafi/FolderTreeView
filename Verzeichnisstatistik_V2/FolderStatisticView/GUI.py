from FolderStatistic import *
import PyQt5.QtCore as core
import PyQt5.QtGui as gui
import PyQt5.QtWidgets as widgets
import PyQt5.uic as uic
import sys
import threading

class FileTreeGui:

    def __init__(self):
        self.__folder_stats = FolderStats(self.process_is_finished)
        threading.Event.__init__(self)
        self.connected = threading.Event
        self.__app = widgets.QApplication(sys.argv)
        self.__fileTreeGui = uic.loadUi("VerzeichnisGUI.ui")
        self.__define_actions()

        self.__buttons = [self.__fileTreeGui.startBut, self.__fileTreeGui.pauseBut, self.__fileTreeGui.resumeBut,
                          self.__fileTreeGui.stopBut, self.__fileTreeGui.showBut]



    def __define_actions(self):
        self.__fileTreeGui.actionSpeichern.triggered.connect(self.speichern)
        self.__fileTreeGui.actionConnect.triggered.connect(self.__connect)
        self.__fileTreeGui.startBut.clicked.connect(self.__start_process)
        self.__fileTreeGui.pauseBut.clicked.connect(self.__pause_process)
        self.__fileTreeGui.resumeBut.clicked.connect(self.__continue_process)
        self.__fileTreeGui.stopBut.clicked.connect(self.__stop_process)
        self.__fileTreeGui.showBut.clicked.connect(self.__show_folder_stats)


    def show(self):
        self.__fileTreeGui.show()
        self.__app.exec_()


    def speichern(self):
        if self.__folder_stats.status == Status.Finished:
            with open("FolderStats.txt", "w") as file:
                for fold in self.__folder_stats.get_folders():
                    file.write(str(fold) + "\n")

    def process_is_finished(self):
        if self.__folder_stats.status == Status.Finished:
            self.__fileTreeGui.status_label.setText("Status: " + str(self.__folder_stats.status))

            folder_tree = self.__folder_stats.folders_list
            root = widgets.QTreeWidgetItem(folder_tree.root.to_list())
            self.set_widget_children(root, folder_tree.root)
            self.__fileTreeGui.fileTree.addTopLevelItems([root])


    def set_widget_children(self, widget_item, children):
        for child in children.children:
            child_item = widgets.QTreeWidgetItem(child.to_list())
            widget_item.addChild(child_item)
            self.set_widget_children(child_item, child)

    def __start_process(self):
        if self.__folder_stats.status != Status.Running and self.__folder_stats.status != Status.Finished and\
                        self.__folder_stats.status != Status.Paused:
            self.__folder_stats.start()
            self.__fileTreeGui.status_label.setText("Status: " + str(self.__folder_stats.status))

    def __pause_process(self):
        if self.__folder_stats.status == Status.Running:
            self.__folder_stats.pause()
            self.__fileTreeGui.status_label.setText("Status: " + str(self.__folder_stats.status))

    def __continue_process(self):
        if self.__folder_stats.status == Status.Paused:
            self.__folder_stats.resume()
            self.__fileTreeGui.status_label.setText("Status: " + str(self.__folder_stats.status))

    def __stop_process(self):
        if self.__folder_stats.status == Status.Running or self.__folder_stats.status == Status.Paused:
            self.__folder_stats.stop()
            self.__fileTreeGui.status_label.setText("Status: " + str(self.__folder_stats.status))

            folder_tree = self.__folder_stats.folders_list
            root = widgets.QTreeWidgetItem(folder_tree.root.to_list())
            self.set_widget_children(root, folder_tree.root)
            self.__fileTreeGui.fileTree.addTopLevelItems([root])


    def __show_folder_stats(self):
        folder_tree = self.__folder_stats.folders_list
        root = widgets.QTreeWidgetItem(folder_tree.root.to_list())
        self.set_widget_children(root, folder_tree.root)
        self.__fileTreeGui.fileTree.addTopLevelItems([root])

    def __connect(self):
            directory = widgets.QFileDialog.getExistingDirectory()
            self.__folder_stats.connect(directory)
            self.__show_buttons()
            self.dir = directory

    def __show_buttons(self):
        if self.__folder_stats.status == Status.Connected:
            self.__fileTreeGui.status_label.setText("Status: " + str(self.__folder_stats.status))
            for but in self.__buttons:
                but.setEnabled(True)


fileTree = FileTreeGui()
fileTree.show()