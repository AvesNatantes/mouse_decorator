import tkinter as tk
from PIL import Image, ImageTk
from pynput import mouse
import pystray
from pystray import MenuItem as item
import threading
import time
import os
import sys

class MouseFollowerApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-topmost', True, '-transparentcolor', 'white')
        self.root.overrideredirect(True)
        self.root.geometry('+0+0')
        # self.root.withdraw()  # Hide the window initially

        # Load the images with transparency
        self.no_image = Image.open(self.resource_path("mouse.png")).convert('RGBA')
        self.cl_image = Image.open(self.resource_path("mouse_left.png")).convert('RGBA')
        self.cr_image = Image.open(self.resource_path("mouse_right.png")).convert('RGBA')
        self.cm_image = Image.open(self.resource_path("mouse_middle.png")).convert('RGBA')
        self.sl_image = Image.open(self.resource_path("mouse_scroll_left.png")).convert('RGBA')
        self.sr_image = Image.open(self.resource_path("mouse_scroll_right.png")).convert('RGBA')
        self.su_image = Image.open(self.resource_path("mouse_scroll_up.png")).convert('RGBA')
        self.sd_image = Image.open(self.resource_path("mouse_scroll_down.png")).convert('RGBA')

        # Create Tkinter PhotoImage objects
        self.no_photo = ImageTk.PhotoImage(self.no_image)
        self.cl_photo = ImageTk.PhotoImage(self.cl_image)
        self.cr_photo = ImageTk.PhotoImage(self.cr_image)
        self.cm_photo = ImageTk.PhotoImage(self.cm_image)
        self.sl_photo = ImageTk.PhotoImage(self.sl_image)
        self.sr_photo = ImageTk.PhotoImage(self.sr_image)
        self.su_photo = ImageTk.PhotoImage(self.su_image)
        self.sd_photo = ImageTk.PhotoImage(self.sd_image)

        # Create a label and set a default image
        self.label = tk.Label(root, image=self.no_photo, bg='white')
        self.label.pack()

        # Start the mouse listener
        self.listener = mouse.Listener(on_move=self.on_move,on_click=self.on_click,on_scroll=self.on_scroll)
        self.listener.start()

        self.track_mouse()

        # create another thread with the tray icon
        self.tray_thread = threading.Thread(target=self.create_tray_icon)
        self.tray_thread.daemon = True
        self.tray_thread.start()

    def resource_path(self,relative_path):
        try:
            # for code inside PyInstaller
            base_path = sys._MEIPASS
        except Exception:
            # Get absolute path in plain code
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def create_tray_icon(self):
        # Create and run the system tray icon
        menu = (item('Exit', self.on_close),)
        image = Image.open("mouse.ico")
        self.tray_icon = pystray.Icon('mouse_follower', image, 'Mouse Follower', menu)
        self.tray_icon.run()

    def on_move(self, x, y):
        self.root.deiconify()

    def move(self):
        self.root.deiconify()

    def on_click(self, x, y, button, pressed):
        if pressed:
            # Show the custom cursor with the appropriate image
            if button == mouse.Button.left:
                self.label.config(image=self.cl_photo)
            elif button == mouse.Button.right:
                self.label.config(image=self.cr_photo)
            elif button == mouse.Button.middle:
                self.label.config(image=self.cm_photo)
        else:
            #show the default image
            self.label.config(image=self.no_photo)
            self.root.after(100, self.move)

        self.root.deiconify()

    def on_scroll(self, x, y, dx, dy):
        print(dx,dy)
        if dx > 0:
            self.label.config(image=self.sr_photo)
        elif dx < 0:
            self.label.config(image=self.sl_photo)
        if dy < 0:
            self.label.config(image=self.sd_photo)
        elif dy > 0:
            self.label.config(image=self.su_photo)

        self.root.deiconify()
        self.root.after(100, self.return_to_default)

    def return_to_default(self):
        # Return to the default cursor image
        self.label.config(image=self.no_photo)

    def track_mouse(self):
        # Update the position of the window
        # self.root.deiconify()
        x, y = self.root.winfo_pointerxy()
        self.root.geometry(f'+{x+14}+{y+5}')
        self.root.after(10, self.track_mouse)  # Update position every 10 milliseconds

    def on_close(self):
        self.tray_icon.visible = False
        self.tray_icon.stop()
        self.listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseFollowerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
