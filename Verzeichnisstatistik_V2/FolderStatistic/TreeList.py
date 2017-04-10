

class TreeList:

    def __init__(self, root=None):
        self.__root = root
        self.__cache = self.Cache()

    @property
    def root(self):
        return self.__root

    def set_root(self, root):
        self.__cache.add_folder(root)
        self.__root = root

    def add_node(self, ob):
        self.__cache.add_folder(ob)
        parent_name = ob.path[0: ob.path.rfind("\\")]
        parent_ob = self.__cache.get_folder(parent_name)
        parent_ob.add_child(ob)

        parent_ob.set_number_of_files(ob.number_of_files)
        parent_ob.set_current_bytes(ob.current_bytes)
        parent_ob.set_depth(ob.depth)

        while 1:
            parent_ob =  self.__cache.get_folder(parent_ob.path[0: parent_ob.path.rfind("\\")])
            if parent_ob is None:
                break
            parent_ob.set_number_of_files(ob.number_of_files)
            parent_ob.set_current_bytes(ob.current_bytes)
            parent_ob.set_depth(ob.depth)



    class Cache:
        def __init__(self):
            self.cache = {}

        def add_folder(self, folder_obj):
            self.cache[folder_obj.path] = folder_obj

        def get_folder(self, folder_name):
            return self.cache.get(folder_name, None)