import customtkinter as ctk
import PIL.Image
from performance_timer import PerformanceTimer
performance_timer=PerformanceTimer()

class Fonts:
    def __init__(self):
        self.fonts={
            "regular":ctk.FontManager.load_font("data/app_data/static/assets/fonts/JetBrainsMono-Regular.ttf"),
            "medium":ctk.FontManager.load_font("data/app_data/static/assets/fonts/JetBrainsMono-Medium.ttf"),
            "medium_italic":ctk.FontManager.load_font("data/app_data/static/assets/fonts/JetBrainsMono-Medium-Italic.ttf"),
            "italic":ctk.FontManager.load_font("data/app_data/static/assets/fonts/JetBrainsMono-Italic.ttf"),
            "extra_bold":ctk.FontManager.load_font("data/app_data/static/assets/fonts/JetBrainsMono-ExtraBold.ttf"),
            "extra_bold_italic":ctk.FontManager.load_font("data/app_data/static/assets/fonts/JetBrainsMono-ExtraBold-Italic.ttf"),
            "bold":ctk.FontManager.load_font("data/app_data/static/assets/fonts/JetBrainsMono-Bold.ttf"),
            "bold_italic":ctk.FontManager.load_font("data/app_data/static/assets/fonts/JetBrainsMono-Bold-Italic.ttf"),
        }

        self.regular=ctk.CTkFont("JetBrains Mono Medium")
        self.medium=ctk.CTkFont("JetBrains Mono Medium")
        self.bold=ctk.CTkFont("JetBrains Mono Bold")
        self.extrabold=ctk.CTkFont("JetBrains Mono ExtraBold")


    def get_font(self,font,size=15,italic=False,bold=False,underline=False,strike=False):

        if font=="medium":font_name = "JetBrains Mono Medium"
        elif font=="bold":font_name = "JetBrains Mono Bold"
        elif font=="extrabold":font_name = "JetBrains Mono ExtraBold"
        else:font_name = "JetBrains Mono"

        if italic: slant="italic"
        else: slant="roman"

        if bold:weight="bold"
        else:weight="normal"

        return ctk.CTkFont(family=font_name,size=size,slant=slant,weight=weight,underline=underline,overstrike=strike)


class Colours:
    def __init__(self):

        self.primary="#f07433"
        self.secondary="#c04f15"
        self.tertiary="#80350e"

        self.white="#ffffff"
        self.light_grey="#e5e5e5"
        self.mid_grey="#d9d9d9"
        self.dark_grey="#a6a6a6"
        self.blue_grey="#757D89"
        self.black="#000000"


    def hex_to_rgba(self,hex_color):
        if hex_color[0]=="#":
            return (int(hex_color[1:3],16),int(hex_color[3:5],16),int(hex_color[5:7],16),255)
        else:
            raise ValueError("hex code must start with #")


class Icons:
    def __init__(self):
        self.colours=Colours()

    def icon(self,icon_path,new_colour):
        performance_timer.lap(f"icon creation start {id(self)}")
        new_colour = self.colours.hex_to_rgba(new_colour)
        performance_timer.lap(f"convert icon colour {id(self)}")
        image=PIL.Image.open(icon_path)
        performance_timer.lap(f"open image {id(self)}")
        image=image.convert("RGBA")
        img_data=image.getdata()
        performance_timer.lap(f"convert and get image data {id(self)}")
        new_img_data=[]
        for pixel in img_data:
            if pixel ==(255,255,255,255):
                new_img_data.append(new_colour)
            else:
                new_img_data.append((0,0,0,0))
        performance_timer.lap(f"modify image data {id(self)}")
        image.putdata(new_img_data)
        performance_timer.lap(f"make new image {id(self)}")
        return image

