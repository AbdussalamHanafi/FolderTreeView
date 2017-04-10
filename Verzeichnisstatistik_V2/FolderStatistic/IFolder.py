

class Folder:

    def __init__(self, path, parent=None):
        self.__path = path
        self.__number_of_files = 0
        self.__total_bytes = 0
        self.__depth = 0
        self.parent = parent
        self.children = []

    @property
    def current_bytes(self):
        return self.__total_bytes

    def set_current_bytes(self, bytes):
        self.__total_bytes += bytes


    def add_child(self, new_children):
        self.children.append(new_children)

    @property
    def number_of_files(self):
        return self.__number_of_files

    def set_number_of_files(self, file_number):
        self.__number_of_files += file_number

    @property
    def depth(self):
        return self.__depth

    def set_depth(self, depth):
        self.__depth += depth
    @property
    def path(self):
        return self.__path

    def set_path(self, path):
        self.__path = path

    def to_list(self):
        return [str(self.__path), str(self.__number_of_files), str(self.__number_of_files), str(self.__depth)]

    def __str__(self):
        return "Path: " + str(self.__path) + " Number of Files: " + str(self.__number_of_files) + " Total Bytes: " \
               + str(self.__number_of_files) + " Depth: " + str(self.__depth)

