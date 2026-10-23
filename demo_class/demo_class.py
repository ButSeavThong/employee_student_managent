class Democlass:
    def __init__(self, class_name, class_id):
        self.class_name = class_name
        self.class_id = class_id

    def class_infor(self):
        print("Class demo infor")
        print(f"class name : {self.class_name}, class id {self.class_id}")


class_demo = Democlass("Java class", "J001")
class_demo.class_infor()
