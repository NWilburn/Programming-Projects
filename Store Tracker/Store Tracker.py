from tkinter import Tk, StringVar, CENTER, VERTICAL, Canvas, Menu, Frame, font, ttk, messagebox
from selenium.webdriver.common import desired_capabilities
from ttkthemes import ThemedTk
from PIL import ImageTk, Image
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pathlib import Path
from time import sleep
from threading import Thread
import sys
import logging


class TrackedSite:

    def __init__(self, current_frame, site_data, file_location):
        self.splitter = "hx00A8F~"
        self.site_data = site_data.split(self.splitter)
        self.nickname = self.site_data[0]
        self.site_link = self.site_data[1]
        self.file_location = file_location
        self.current_frame = current_frame
        self.not_in_stock = ttk.Label(self.current_frame, text='Not in stock', foreground='red')
        self.in_stock = ttk.Label(self.current_frame, text="It's in stock!", foreground='green')
        self.not_in_stock.grid(column=1, row=self.file_location, padx=20, pady=20)
        self.kill_thread = False
        self.options_menu = Menu(tearoff=0)
        self.options_menu.add_command(label="Set Nickname", command=lambda : self.set_nickname())
        self.options_menu.add_command(label="Go to Site", command=lambda : self.go_to_site())
        self.options_menu.add_command(label="Delete", command=lambda : self.delete_site())
        self.options_button = ttk.Menubutton(self.current_frame, text='Options', menu=self.options_menu)
        self.options_button.grid(column=2, row=self.file_location, padx=20, pady=20)
        self.set_nickname_entry = ttk.Entry(current_frame, width=10)
        self.change_new_tracked(True)
        p = Thread(target=self.track_site)
        p.start()


    def change_new_tracked(self, first_run):
        if first_run == False:
            self.new_tracked.grid_remove()
        if self.nickname == "None":
            self.new_tracked = ttk.Label(self.current_frame, text=self.site_link, width=70, anchor=CENTER)
            self.new_tracked.grid(column=0, row=self.file_location, padx=20, pady=20)
        else:
            self.new_tracked = ttk.Label(self.current_frame, text=self.nickname, width=70, anchor=CENTER)
            self.new_tracked.grid(column=0, row=self.file_location, padx=20, pady=20)

    def set_nickname(self):
        self.options_button.grid_forget()
        self.set_nickname_entry.grid(column=2, row=self.file_location, padx=20, pady=20)
        self.set_nickname_entry.bind('<Return>', self.option_return)

    def option_return(self, event):
        self.nickname = self.set_nickname_entry.get()
        self.change_new_tracked(False)
        self.site_data[0] = self.nickname
        trackedSites[self.file_location] = self.splitter.join(self.site_data)
        with open(tracked_items_file, 'w') as f:
            f.writelines(trackedSites)
        self.set_nickname_entry.grid_forget()
        self.options_button.grid(column=2, row=self.file_location, padx=20, pady=20)

    def go_to_site(self):
        inStockDriver = webdriver.Firefox(executable_path=f'{Path(__file__).parent.absolute()}/geckodriver.exe')
        inStockDriver.get(self.site_link)

    def delete_site(self):
        for t in range(len(trackedSites)):
            if t > self.file_location:
                TrackedSiteClasses[t].file_location -= 1
        del trackedSites[self.file_location]
        del TrackedSiteClasses[self.file_location]
        self.new_tracked.grid_remove()
        self.not_in_stock.grid_remove()
        self.in_stock.grid_remove()
        self.options_button.grid_remove()
        with open(tracked_items_file, 'w') as f:
            f.writelines(trackedSites)
        if len(trackedSites) == 0:
            noSitesTracked.grid(column=0, columnspan=3, row=2, pady=200)
        self.kill_thread = True

    def track_site(self):
        opts = Options()
        opts.add_argument('--headless')
        opts.add_argument('--disable-gpu')
        capa = DesiredCapabilities.FIREFOX
        capa["pageLoadStrategy"] = "none"
        while True:
            if self.kill_thread == True:
                print("Killing thread")
                break
            else:
                driver = webdriver.Firefox(executable_path=f'{Path(__file__).parent.absolute()}/geckodriver.exe', options=opts, desired_capabilities=capa)
                wait = WebDriverWait(driver, 10)
                driver.get(self.site_link)
                try:
                    available_status = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '.btn-disabled')))
                    driver.execute_script("window.stop();")
                    if available_status.get_attribute("class") == 'btn btn-disabled btn-lg btn-block add-to-cart-button' and self.kill_thread == False:
                        self.in_stock.grid_remove()
                        self.not_in_stock.grid(column=1, row=self.file_location, padx=20, pady=20)
                        print("Not in stock")
                except:
                    try:
                        available_status = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'button.btn-primary:nth-child(1)')))
                        driver.execute_script("window.stop();")
                        if available_status.get_attribute("class") == 'btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button' and self.kill_thread == False:
                            self.not_in_stock.grid_remove()
                            self.in_stock.grid(column=1, row=self.file_location, padx=20, pady=20)
                            print("In stock!")
                            inStockAlert = messagebox.askquestion('Item in Stock!', 'One of your items is in stock!\nWould you like to go to the site?')
                            if inStockAlert == 'yes':
                                self.go_to_site()
                            self.kill_thread = True
                    except:
                        print("This shit done broke")
                finally:
                    driver.quit()
                    sleep(3)



def add_site(event):
    noSitesTracked.grid_remove()
    link=linkInput.get()
    with open(tracked_items_file, "a") as f:
        f.write("Nonehx00A8F~" + link +"hx00A8F~\n")
        trackedSites.append("Nonehx00A8F~" + link +"hx00A8F~\n")
    with open(tracked_items_file, "r") as f:
        TrackedSiteClasses.append(TrackedSite(trackedSitesPane, "Nonehx00A8F~" + link +"hx00A8F~\n", len(f.readlines()) - 1))

def scroll_event(event):
    trackedSitesCanvas.configure(scrollregion=trackedSitesCanvas.bbox("all"))

def exit_window():
    for t in TrackedSiteClasses:
        t.kill_thread = True
    wn.destroy()


if __name__ == '__main__':
    tracked_items_file = str(Path(__file__).parent.absolute()) + "\\Tracked Items.txt"
    wn = ThemedTk()
    wn.set_theme(theme_name='scidgrey', themebg=True)
    wn.title("Store Tracker")
    wn.geometry("750x500")
    wn.resizable(False, False)
    rows = 0
    while rows < 5:
        wn.rowconfigure(rows, weight=1)
        wn.columnconfigure(rows, weight=1)
        rows += 1
    linkInputText = StringVar(wn, value="Enter Link")
    linkInput = ttk.Entry(wn, textvariable=linkInputText, width=27)
    linkInput.grid(row=0, column=0, columnspan=2, sticky="NW", padx=5, pady=10)
    linkInput.bind('<Return>', add_site)
    plusIcon = ImageTk.PhotoImage(Image.open(str(Path(__file__).parent.absolute()) + "\\plusButton.png"))
    submitLinkButton = ttk.Button(wn, text="Submit")
    submitLinkButton.bind('<Button-1>', add_site)
    submitLinkButton.grid(column=1, row=0, sticky="NW", pady=10, padx=170)
    TrackedSitesTopFrame = ttk.Frame(wn, width="700", height="400", relief='sunken')
    TrackedSitesTopFrame.grid(column=1, row=1)
    trackedSitesCanvas = Canvas(TrackedSitesTopFrame, width="700", height="400", bg='gainsboro')
    trackedSitesCanvas.grid()
    trackedSitesPane = Frame(trackedSitesCanvas, bg='gainsboro')
    trackedSitesCanvas.create_window((0,0), window=trackedSitesPane, anchor="nw")
    paneScrollBar = ttk.Scrollbar(TrackedSitesTopFrame, orient=VERTICAL, command=trackedSitesCanvas.yview)
    paneScrollBar.grid(column=0, row=0, sticky='NSE')
    trackedSitesCanvas.configure(yscrollcommand=paneScrollBar.set)
    wn.bind("<Configure>", scroll_event)
    noSitesTracked = ttk.Label(trackedSitesPane, text="You don't have any sites tracked", foreground="grey", width=115, anchor=CENTER)
    TrackedSiteClasses = []
    with open(tracked_items_file, "r") as f:
        trackedSites = f.readlines()
    if len(trackedSites) == 0:
        noSitesTracked.grid(column=0, columnspan=3, row=2, pady=200)
    else:
        for t in range(len(trackedSites)):
            TrackedSiteClasses.append(TrackedSite(trackedSitesPane, trackedSites[t], t))
    

    wn.protocol("WM_DELETE_WINDOW", exit_window)
    wn.mainloop()