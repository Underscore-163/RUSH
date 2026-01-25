from ctksidebar import CTkSidebarNavigation
from PIL import Image
import customtkinter as ctk
from logger import get_main_logger

log=get_main_logger()


class Sidebar(CTkSidebarNavigation):
    """RUSH sidebar"""
    def __init__(self,master,width):
        log.info("creating sidebar")
        self.master=master
        self.width=width
        CTkSidebarNavigation.__init__(self,master=self.master,width=self.width)
        self.pack(fill="both", expand=True)

        self.sidebar.add_spacing(10)
        self.header=self.get_header()
        self.sidebar.add_frame(self.header)
        self.sidebar.add_spacing(10)
        self.sidebar.add_separator(width=self.width)
        self.sidebar.add_spacing(10)

        self.sidebar.add_item(id="home",text="Home")


    def get_header(self):
        """create the sidebar header"""
        """
        creates the sidebar header and returns it as a CTkFrame object.

        1. first, we make the frame (header)
        2. then we find how mush we need to scale the image (header_width_sf)
            a. sf is scale factor
            b. the magic number is the image width.
            it probably shouldn't be hard coded, but I cant be bothered.
        3. next we create a CTkFrame object to hold the logo image
            a. it has no identifier, as we don't need to refer to it ever again
            b. we set the 'header' frame as the master
            c. we set its text to an empty string to remove the default text
            d. we set the image to the correct logo with CTkImage
                i. we set the size of the image based on the scale factor we worked out in step 2
            e. we pack the label onto the header frame
        4. finally, we return the header
        """
        log.info("creating header")
        header=ctk.CTkFrame(self.sidebar,bg_color="transparent")
        header_width_sf=int(3645/self.width)
        log.debug(f"header width scale factor={header_width_sf}")
        ctk.CTkLabel(master=header,
                     text="",
                     image=ctk.CTkImage(Image.open("data/assets/RUSH_logo.png"),
                                        size=(int(3645/header_width_sf),int(738/header_width_sf))),
                     ).pack()
        return header

    def collapse(self):
        print("collapse")

    def expand(self):
        print("expand")
