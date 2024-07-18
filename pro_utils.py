# import re, string
from collections import UserDict

class MapLUT(UserDict):
    def __init__(self, pro_proj):
        super().__init__()
        
        self.update(
            {"Basemaps": {}, "Anno": {}, "Special": {},}
        )
        
        self.data["Anno"].update(
            {"Bridge": {}, "County": {},}
        )
        
        maps_list = pro_proj.listMaps()

        for one_map in maps_list:
            if not self.read_map(one_map):
                print(f"Unable to read {one_map.name}")
    def read_map(self, this_map):
        try:
            my_name_is = this_map.name.lower()
        except AttributeError as ae:
            print(ae)
            raise Exception

        if my_name_is.count("basemap"):
            if my_name_is.count("complete"):
                self.data["Basemaps"].update({"A": this_map.name})
                return True
            else:
                self.data["Basemaps"].update({"B": this_map.name})
                return True

        elif my_name_is.count("bridge") and my_name_is.count("anno"):
            if my_name_is.count("complete"):
                self.data["Anno"]["Bridge"].update({"A": this_map.name})
                return True
            elif my_name_is.count("nomileage"):
                self.data["Anno"]["Bridge"].update({"B": this_map.name})
                return True

            else:
                return False
        
        elif my_name_is.count("county") and my_name_is.count("anno"):
            if my_name_is.count("complete"):
                self.data["Anno"]["County"].update({"A": this_map.name})
                return True
            elif my_name_is.count("nomileage"):
                self.data["Anno"]["County"].update({"B": this_map.name})
                return True

            else:
                return False

        elif my_name_is.count("nbis"):
            self.data["Special"].update({"NonNBIS": this_map.name})
            return True

        elif my_name_is.count("mileage anno"):
            self.data["Special"].update({"Mileage": this_map.name})
            return True

        elif my_name_is.count("structure"):
            self.data["Special"].update({"Structures": this_map.name})
            return True

        else:
            return False
