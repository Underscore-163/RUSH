import customtkinter as ctk

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

        self.light_grey="#e5e5e5"
        self.mid_grey="#d9d9d9"
        self.dark_grey="#a6a6a6"
