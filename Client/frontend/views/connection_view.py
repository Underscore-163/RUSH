import time
import datetime
import customtkinter as ctk
import json
from Client.frontend.widgets.styles import Fonts, Colours, Icons
import Client.backend.server as server
import requests

class ConnectionView(ctk.CTkFrame):
    def __init__(self,master):
        self.master=master
        ctk.CTkFrame.__init__(self,self.master)

        self.fonts=Fonts()
        self.colours=Colours()
        self.icons=Icons()

        """
        {
          "remember": false,
          "username": "",
          "password": ""
        }
        """
        with open("data/user_data/credentials.json") as file:
            credentials_dict=json.load(file)
            self.remember_var = ctk.BooleanVar(value=credentials_dict["remember"])
            self.username_var = ctk.StringVar(value=credentials_dict["username"])
            self.password_var = ctk.StringVar(value=credentials_dict["password"])

        self.rowconfigure(index=list(range(2)), uniform="_", weight=1)
        self.columnconfigure(index=list(range(3)), uniform="-", weight=1)

        self.credentials_frame=ctk.CTkFrame(master=self)
        self.info_frame=ctk.CTkFrame(master=self)
        self.actions_frame=ctk.CTkFrame(master=self)


        self.credentials_frame.grid(row=0,column=0,sticky="nsew",columnspan=2,padx=5,pady=5)
        self.info_frame.grid(row=1,column=0,sticky="nsew",columnspan=2,padx=5,pady=5)
        self.actions_frame.grid(row=0,column=2,sticky="nsew",rowspan=2,padx=5,pady=5)

        self.username_input=ctk.CTkEntry(master=self.credentials_frame,textvariable=self.username_var)
        self.password_input=ctk.CTkEntry(master=self.credentials_frame,textvariable=self.password_var)
        self.remember_switch = ctk.CTkSwitch(self.credentials_frame, text="Remember Credentials",
                                             font=self.fonts.get_font("Medium"),
                                             variable=self.remember_var, )
        self.authenticate_button=ctk.CTkButton(master=self.credentials_frame,
                                               image=ctk.CTkImage(self.icons.icon(
                                                   "data/app_data/static/assets/authenticate.png",
                                                   self.colours.white),size=(30,30)),
                                               text="Authenticate",
                                               font=self.fonts.get_font("Medium",20),
                                               command=self.authenticate)

        ctk.CTkLabel(self.credentials_frame,text="Username:",
                     font=self.fonts.get_font("Medium",bold=True)).pack(padx=5,pady=5,anchor="w")
        self.username_input.pack(padx=5,pady=5,anchor="w",fill="x")
        ctk.CTkLabel(self.credentials_frame,text="Password:",
                     font=self.fonts.get_font("Medium",bold=True)).pack(padx=5,pady=5,anchor="w")
        self.password_input.pack(padx=5,pady=5,anchor="w",fill="x")
        self.remember_switch.pack(fill="both",expand=True,padx=10,pady=5)
        self.authenticate_button.pack(fill="both",expand=True,padx=5,pady=5)


        self.download_assignments_button=ctk.CTkButton(master=self.actions_frame,
                                                       text="Download Assignments",
                                                       image=ctk.CTkImage(
                                                           self.icons.icon(
                                                               "data/app_data/static/assets/download.png",
                                                                           self.colours.white),size=(30,30)
                                                       ),
                                                       font=self.fonts.get_font("Medium", ),
                                                       anchor="w",
                                                       command=server.test_connection
                                                       )
        self.download_review_button=ctk.CTkButton(master=self.actions_frame,
                                                  text="Download Review Packages",
                                                  image=ctk.CTkImage(
                                                      self.icons.icon(
                                                          "data/app_data/static/assets/download.png",
                                                                      self.colours.white),size=(30,30)
                                                  ),
                                                  font=self.fonts.get_font("Medium", ),
                                                  anchor="w",
                                                  )
        self.upload_assignments_button=ctk.CTkButton(master=self.actions_frame,
                                                     text="Upload Assignments",
                                                     image=ctk.CTkImage(
                                                         self.icons.icon(
                                                             "data/app_data/static/assets/upload.png",
                                                                         self.colours.white),size=(30,30)
                                                     ),
                                                     font=self.fonts.get_font("Medium", ),
                                                     anchor="w",
                                                     )
        self.upload_work_button=ctk.CTkButton(master=self.actions_frame,
                                              text="Upload Student Work",
                                              image=ctk.CTkImage(
                                                  self.icons.icon("data/app_data/static/assets/upload.png",
                                                                  self.colours.white),size=(30,30)
                                              ),
                                              font=self.fonts.get_font("Medium",),
                                              anchor="w",
                                              )

        ctk.CTkLabel(self.actions_frame, text="Download", font=self.fonts.get_font("Medium", bold=True)
                     ).pack(padx=10, pady=5, anchor="w")
        self.download_assignments_button.pack(fill="both",expand=True,padx=10,pady=5,ipadx=15)
        self.download_review_button.pack(fill="both",expand=True,padx=10,pady=5,ipadx=15)
        ctk.CTkLabel(self.actions_frame, text="Upload", font=self.fonts.get_font("Medium", bold=True)
                     ).pack(padx=10, pady=5, anchor="w")
        self.upload_assignments_button.pack(fill="both",expand=True,padx=10,pady=5,ipadx=15)
        self.upload_work_button.pack(fill="both",expand=True,padx=10,pady=5,ipadx=15)

        self.token_lifetime_label=ctk.CTkLabel(master=self.info_frame,
                                               text=str((datetime.datetime.fromtimestamp(
                                                   server.get_connection_info()["token"]["TimeOfDeath"]
                                               )-datetime.datetime.fromtimestamp(time.time())).days)+" Days Remaining",
                                               font=self.fonts.get_font("Medium", bold=True),
                                               text_color=self.colours.secondary
                                               )
        self.user_id_label=ctk.CTkLabel(master=self.info_frame,
                                        text=server.get_connection_info()["token"]["UserID"],
                                        font=self.fonts.get_font("Medium"),)
        self.client_id_label=ctk.CTkLabel(master=self.info_frame,
                                          text=server.get_connection_info()["token"]["ClientID"],
                                          font=self.fonts.get_font("Medium"),)
        self.status_label=ctk.CTkLabel(master=self.info_frame,
                                       text="Ready",
                                       font=self.fonts.get_font("Medium",bold=True),
                                       text_color=self.colours.yellow
                                       )

        ctk.CTkLabel(self.info_frame,text="Last Connection Info",font=self.fonts.get_font("Medium",20,bold=True)).grid(row=0,column=0,padx=5,pady=10)
        ctk.CTkLabel(self.info_frame,text="Authentication Token Time Out",font=self.fonts.get_font("Medium"),text_color=self.colours.dark_grey).grid(row=1,column=0,padx=15,pady=5,sticky="w")
        ctk.CTkLabel(self.info_frame, text="User ID", font=self.fonts.get_font("Medium"),text_color=self.colours.dark_grey).grid(row=2,column=0,padx=15,pady=5,sticky="w")
        ctk.CTkLabel(self.info_frame, text="Client ID", font=self.fonts.get_font("Medium"),text_color=self.colours.dark_grey).grid(row=3,column=0,padx=15,pady=5,sticky="w")
        ctk.CTkLabel(self.info_frame, text="Status", font=self.fonts.get_font("Medium"),text_color=self.colours.dark_grey).grid(row=4,column=0,padx=15,pady=5,sticky="w")

        self.token_lifetime_label.grid(row=1,column=1,padx=5,pady=5,sticky="e")
        self.user_id_label.grid(row=2,column=1,padx=5,pady=5,sticky="e")
        self.client_id_label.grid(row=3,column=1,padx=5,pady=5,sticky="e")
        self.status_label.grid(row=4,column=1,padx=5,pady=5,sticky="e")

    def authenticate(self):
        self.status_label.configure(text="Connecting...", text_color=self.colours.primary)
        if self.remember_var.get():
            with open("data/user_data/credentials.json","w") as file:
                json.dump({
                    "remember":True,
                    "username":self.username_var.get(),
                    "password":self.password_var.get()
                           }
                ,file)
        else:
            with open("data/user_data/credentials.json","w") as file:
                json.dump({
                    "remember":False,
                    "username":"",
                    "password":""
                           }
                ,file)
        try:
            status_code= server.authenticate(username=self.username_var.get(),password=self.password_var.get())

            self.token_lifetime_label.configure(text=str((datetime.datetime.fromtimestamp(
                server.get_connection_info()["token"]["TimeOfDeath"]) - datetime.datetime.fromtimestamp(time.time())).days) + " Days Remaining",)
            self.user_id_label.configure(text=server.get_connection_info()["token"]["UserID"])
            self.client_id_label.configure(text=server.get_connection_info()["token"]["ClientID"],)
            if status_code == 200:
                self.status_label.configure(text="OK",text_color=self.colours.green)
            elif status_code == 401:
                self.status_label.configure(text="Failed Authentication",text_color=self.colours.yellow)
            elif status_code == 403:
                self.status_label.configure(text="Unauthorised Client",text_color=self.colours.red)
            else:
                self.status_label.configure(text=f"Error {status_code}", text_color=self.colours.red)

        except requests.exceptions.ConnectionError as e:
            self.status_label.configure(text="Failed to connect", text_color=self.colours.red)