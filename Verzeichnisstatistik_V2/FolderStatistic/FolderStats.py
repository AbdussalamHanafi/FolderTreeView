import os.path
from sys import platform
import threading
from FolderStatistic.IFolder import Folder
from FolderStatistic import TreeList
from enum import Enum

class Status(Enum):
    Waiting = 0
    Connected = 1
    Running = 2
    Paused = 3
    Finished = 4

    def __str__(self):
        if self.value == 0:
            return "Waiting"
        elif self.value == 1:
            return "Connected"
        elif self.value == 2:
            return "Running"
        elif self.value == 3:
            return "Paused"
        elif self.value == 4:
            return "Finished"
        else:
            return "Not Implemented"



class FolderStats(threading.Thread):

    file_seperator = "/"

    def __init__(self, callback=None):
        threading.Thread.__init__(self)
        threading.Event.__init__(self)
        self.status = Status.Waiting
        self.__folder_list = TreeList.TreeList()
        self.pause_process = threading.Event
        self.stop_process = threading.Event
        self.__finished = False
        self.callback = callback
        if "win" in platform.lower():
            FolderStats.file_seperator = "\\"


    def connect(self, path):
        if not os.path.isdir(path):
            print("Path existiert nicht")
        else:
            self.__path = path
            self.status = Status.Connected

    def root_path(self):
        return self.__path

    @property
    def folders_list(self):
        return self.__folder_list


    def pause(self):
        print("Paused")
        self.status = Status.Paused
        self.pause_process.set(self)

    def resume(self):
        print("Resumed")
        self.pause_process.clear(self)
        self.status = Status.Running

    def stop(self):
        print("Stop")
        self.stop_process.set(self)
        self.status = Status.Finished

    def finished(self):
        self.status = Status.Finished
        return self.__finished

    def run(self):
        print("Start")

        self.status = Status.Running
        parent = None
        for dirpath, dirnames, filenames in os.walk(self.__path):

            if self.stop_process.is_set(self):
                return

            if self.pause_process.is_set(self):
                self.pause_process.wait(self)
                self.status = Status.Running


            folder = Folder(dirpath, parent)
            folder.set_number_of_files(len(filenames))
            folder.set_depth(len(dirnames))
            bytes = 0
            for file in filenames:
                bytes += os.path.getsize(dirpath + FolderStats.file_seperator + file)

            folder.set_current_bytes(bytes)

            if self.__folder_list.root is None:
                self.__folder_list.set_root(folder)

            else:
                self.__folder_list.add_node(folder)


        self.__finished = True
        self.status = Status.Finished
        if self.callback is not None:
          self.callback()

def choose_task():
    global  folder_stats
    try:
        fkt = int(input("Welche Aufgabe wollen Sie ausführen? (1: Connect; 2: Start; 3: Pause; 4: Resume; 5: Stop;"
          " 6: Statisik abrufen)"))

        if fkt == 1:
            file = input("Geben Sie den Pfadnamen an: ")
            folder_stats.connect(file)

        elif fkt == 2:
            folder_stats.start()

        elif fkt == 3:
            folder_stats.pause()

        elif fkt == 4:
            folder_stats.resume()

        elif fkt == 5:
            folder_stats.stop()
            return False

        elif fkt == 6:
            for fold in folder_stats.get_folders():
                print(fold)

    except:
        print("Ein Problem ist bei der Durchführung der Aufgabe eingetreten.")

    return True


if __name__ == "__main__":
    folder_stats = FolderStats()

    while(not folder_stats.finished()):
        if not choose_task():
            break

    print("Ende")

    with open("FolderStats.txt", "w") as file:
        for fold in folder_stats.get_folders():
            file.write(str(fold) + "\n")




