import tkinter as tk
from Who_is_it import find_face_def
from new_face import add_face


class GuiClass:
    def __init__(self, main):
        # build GUI frame
        self.main = main
        self.frame = tk.Frame(self.main)
        self.main.title("Control panel")
        self.main.geometry("500x100")

        # add buttons - find face and add new face
        self.Find_face_btn = tk.Button(self.main, text="Who is it?", command=self.find_face_gui)
        self.Find_face_btn.pack(side=tk.TOP)
        self.add_new_face_btn = tk.Button(self.main, text=" Add new face ", command=self.add_new_face_def)
        self.add_new_face_btn.pack(side=tk.TOP)

        # add comment for the user
        self.name_face = tk.Entry(self.main)
        self.name_face.pack()
        self.label_info = tk.Label(self.main, text="")
        self.label_info.pack()
    
    # call find face function from button
    def find_face_gui(self):
        find_face_def()

    # call add face function from button   
    def add_new_face_def(self):
        # make sure input is valid
        if self.name_face.get() != "" and self.name_face.get().replace(" ", "").isalpha():
            self.label_info['text'] = add_face(self.name_face.get().lower())
        else:
            self.label_info['text'] = "Name is invalid - name should be only letters"
        

root = tk.Tk()
GUI = GuiClass(root)
root.mainloop()
