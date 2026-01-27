from PIL import Image
import customtkinter as ctk
import os

os.chdir(os.getcwd().replace("testing","data"))
test=ctk.CTkImage(Image.open("assets/RUSH_logo.png"))