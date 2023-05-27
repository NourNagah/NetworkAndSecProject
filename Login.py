from email_sender import *
import smtplib

class Login:
    senderEmail = ''
    senderPassword = ''
    def __init__(self, root):
        self.root = root
        # setting title
        self.to_var = tk.StringVar()
        root.title("Login to Mail")
        # setting window size
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,
                                    (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times', size=12)
        label_Email = tk.Label(root)
        label_Email["font"] = ft
        label_Email["fg"] = "#333333"
        label_Email["justify"] = "right"
        label_Email["text"] = "Email:"
        label_Email.place(x=40, y=40, width=70, height=25)
        label_Password = tk.Label(root)
        label_Password["font"] = ft
        label_Password["fg"] = "#333333"
        label_Password["justify"] = "right"
        label_Password["text"] = "Password:"
        label_Password.place(x=40, y=90, width=70, height=25)
        self.email = tk.Entry(root, textvariable=self.to_var)
        self.email["borderwidth"] = "1px"
        self.email["font"] = ft
        self.email["fg"] = "#333333"
        self.email["justify"] = "left"
        self.email["text"] = "To"
        self.email.place(x=120, y=40, width=420, height=30)
        bullet = "\u2022"
        self.email_Password = tk.Entry(root, show=bullet)
        self.email_Password["borderwidth"] = "1px"
        self.email_Password["font"] = ft
        self.email_Password["fg"] = "#333333"
        self.email_Password["justify"] = "left"
        self.email_Password["text"] = "Subject"
        self.email_Password.place(x=120, y=90, width=417, height=30)
        button_Login = tk.Button(root)
        button_Login["bg"] = "#f0f0f0"
        button_Login["font"] = ft
        button_Login["fg"] = "#000000"
        button_Login["justify"] = "center"
        button_Login["text"] = "Login"
        button_Login.place(x=270, y=260, width=70, height=25)
        button_Login["command"] = self.button_Login_command

    def button_Login_command(self):
        smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        smtp_server.starttls()
        print(self.email.get())
        try:
            if(smtp_server.login(self.email.get(), self.email_Password.get())):
                smtp_server.quit()
                root = tk.Tk()
                app = App(root, self.email.get(), self.email_Password.get())
                self.root.destroy()
                root.mainloop()
        except:
            print('Could not login either password or email is incorrect')

