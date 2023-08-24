"""
This app window allows user to start/stop the app with a button click,
while also providing the current local URL and QRcode
"""
import tkinter as tk
import pyqrcode
from PIL import ImageTk, Image
import webbrowser
from mainAPIstarter import startMainApi, stopMainApi
from sourceAPIsStarter import startAPIs, stopAPIs

rem = 18
font = ('Helvetica Neue', rem)
primaryColor = '#441f89'
secondaryColor = '#9872df'
textColor = '#fff'
root = tk.Tk()
root.configure(bg=primaryColor)
root.title('Main APP')
mainFrame = tk.Frame(root, bg=primaryColor)
mainFrame.pack(padx=1*rem,pady=1*rem)
def generateQR(url):
    if len(url)!=0 :
        global qr,img
        qr = pyqrcode.create(url)
        img = tk.BitmapImage(data = qr.xbm(scale=8)) # 300 x 300
        qrcodeElement.config(image = img)
        qrcodeElement.grid(row=0,column=0)
qrcodeElement = tk.Label(mainFrame, bg='white')

appFrame = tk.Frame(mainFrame,bg=primaryColor)
appFrame.grid(row=0,column=1,padx=1*rem,pady=1*rem)

logoFrame = tk.Frame(appFrame,bg=primaryColor)
logoFrame.pack(side='top',pady=1*rem)
logoimg = ImageTk.PhotoImage(Image.open('logo.png').resize((5*rem,5*rem)))
tk.Label(logoFrame,image=logoimg,font=font, fg=textColor, bg=primaryColor).pack(side='top',expand='no')
tk.Label(logoFrame,text='Aplicacion multiplataforma y multinube\npara la descarga de contenido multimedia',font=font, fg=textColor, bg=primaryColor).pack(side='top')

controlPanel = tk.Frame(appFrame,bg=primaryColor)
controlPanel.pack(side='bottom')

def startApp(url):
    global startBtn,urlText,urlLabel,urlLink,started
    startBtn.configure(text='Stop app')
    generateQR(url)
    urlText.set(url)
    urlLabel.pack(side='top')
    urlLink.pack(pady=1*rem)
    started=True
def stopApp():
    global startBtn,urlText,urlLabel,urlLink,started
    startBtn.configure(text='Start app')
    qrcodeElement.grid_remove()
    urlLabel.pack_forget()
    urlLink.pack_forget()
    started=False

def modifyApp():
    global started, url
    if(not started):
        # Start app action here
        apis = startAPIs()
        url = startMainApi(apis)
        startApp(url)
    else:
        # Stop app action here
        stopAPIs()
        stopMainApi()
        stopApp()
    pass

started = False
url = 'http://google.com'
startBtn = tk.Button(controlPanel,text='Start app',command=modifyApp, bg=secondaryColor, fg=textColor, font=font)
startBtn.pack(side='bottom')

urlText = tk.StringVar()
urlLabel = tk.Label(controlPanel,textvariable=urlText,font=font, fg=textColor, bg=primaryColor)
urlLink = tk.Label(controlPanel, text="Click here to open app in browser!", fg=textColor, bg=primaryColor, font=font+('underline',), cursor="hand2")
urlLink.bind("<Button-1>", lambda e: webbrowser.open(url,new=0, autoraise=True))

def on_closing():
    global root, started
    if(started):
        stopAPIs()
        stopMainApi()
        stopApp()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()