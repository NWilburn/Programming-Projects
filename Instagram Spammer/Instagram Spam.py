from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import tkinter as tk
import pathlib

class InstagramPrank:

    def __init__(self):
        self.wn = tk.Tk()
        self.wn.geometry("425x225")
        self.wn.title("Instagram Spam")
        self.wn.resizable(False, False)
        tk.Label(self.wn, text = "Your email or username:").grid(row=1, pady=5, sticky = "E")
        email_in = tk.Entry(self.wn, width = '25')
        email_in.grid(row=1, column=2, pady=5)
        self.var = tk.IntVar()
        tk.Label(self.wn, text = "Your Password:").grid(row=2, pady=5, sticky = "E")
        self.passw_in = tk.Entry(self.wn, show = '*', width = '25')
        self.passw_in.grid(row=2, column=2, pady=5)
        show_pass = tk.Checkbutton(self.wn, text = 'Show password', variable=self.var, onvalue=1, offvalue=0, command=self.changeShow)
        show_pass.grid(row=3, column=2, pady=5)
        tk.Label(self.wn, text = "Your Target's Username:").grid(row=4,pady=5, sticky = "E")
        target_in = tk.Entry(self.wn, width = '25')
        target_in.grid(row=4, column=2, pady=5)
        tk.Label(self.wn, text = "Your Message:").grid(row=5, pady=5, sticky = "E")
        message_in = tk.Entry(self.wn, width = '25')
        message_in.grid(row=5, column=2, pady=5)
        tk.Label(self.wn, text = "Amount of times you'd like to send message:").grid(row=6, pady=5, sticky = "E")
        n_in = tk.Entry(self.wn, width = '25')
        n_in.grid(row=6, column=2, pady=5)
        submit = tk.Button(self.wn, text='Submit', command=lambda: self.prank(email_in.get(), self.passw_in.get(), target_in.get(), message_in.get(), int(n_in.get())))
        submit.grid(row=7, column=2, pady=5)
        
        self.wn.mainloop()

    def changeShow(self):
        if self.var.get() == 0:
            self.passw_in.configure(show='*')
        if self.var.get() == 1:
            self.passw_in.configure(show='')

    def prank(self, email, passw, target, message, n):
        if email == '' or passw == '' or target == '' or message == '' or n == '' or type(n) != int:
            self.error_pt1 = tk.Label(self.wn, fg = 'red', text = 'Input information is missing.')
            self.error_pt1.grid(row=7, pady=5, sticky='E')
            self.error_pt2 = tk.Label(self.wn, fg = 'red', text = 'Please fill in missing entries.')
            self.error_pt2.grid(row=8, sticky='E')
            self.wn.geometry("425x250")
            return
        if target == 'nickwilburn7' or target == 'Nick' or target == 'nick' or target == 'Nick Wilburn' or target == 'nick wilburn' or target == 'nickwilburn' or target == 'Nicholas' or target == 'nicholas' or target == 'Nicholas Wilburn' or target == 'nicholas wilburn':
            self.fuck_off = tk.Label(self.wn, fg = 'red', text = "Did you really think I wouldn't think of this?")
            self.fuck_off.grid(row=7, sticky='E')
            self.fuck_off_pt2 = tk.Label(self.wn, fg = 'red', text = 'Try again.')
            self.fuck_off_pt2.grid(row=8)
            self.wn.geometry("425x250")
            return
        try:
            self.error_pt1.grid_forget()
            self.error_pt2.grid_forget()
            self.wn.geometry("425x225")
        except:
            pass
        try:
            self.fuck_off.grid_forget()
            self.fuck_off_pt2.grid_forget()
            self.wn.geometry("425x225")
        except:
            pass
        try:
            opts = Options()
            opts.add_argument('--headless')
            opts.add_argument('--disable-gpu')
            driver = webdriver.Firefox(executable_path=f'{pathlib.Path(__file__).parent.absolute()}/geckodriver.exe', options=opts)
            wait = WebDriverWait(driver, 10)
            driver.get('https://www.instagram.com')
            femail = wait.until(ec.visibility_of_element_located((By.NAME, 'username')))
            password = driver.find_element_by_name("password")
            femail.clear()
            password.clear()
            femail.send_keys(email)
            password.send_keys(passw)
            password.send_keys(Keys.RETURN)
            try:
                not_now = wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/div/div/div/button')))
            except:
                invalid_info = tk.Label(self.wn, fg = 'red', text = "Username or password was invalid.")
                invalid_info.grid(row=7, pady=5, sticky= "E")
                return
            not_now.click()
            no_sir_notif = wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[2]')))
            no_sir_notif.click()
            dms = wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a')))
            dms.click()
            new_message = wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button')))
            new_message.click()
            search = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '.j_2Hd')))
            search.send_keys(target)
            target_pt_2 = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div.-qQT3:nth-child(1)')))
            target_pt_2.click()
            next_button = wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div/button')))
            next_button.click()
            message_box = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '.ItkAi > textarea:nth-child(1)')))
            for t in range(n):
                message_box.send_keys(message)
                message_box.send_keys(Keys.RETURN)
                msgSent = tk.Label(self.wn, fg = 'green', text = f'Message {t + 1} sent')
                msgSent.grid(row=7, pady=5, sticky='E')
        except:
            self.error_pt1 = tk.Label(self.wn, fg = 'red', text = 'Timed out sending messages.')
            self.error_pt1.grid(row=7, pady=5, sticky='E')
            self.error_pt2 = tk.Label(self.wn, fg = 'red', text = 'Please try again.')
            self.error_pt2.grid(row=8, sticky='E')
            self.wn.geometry("425x250")
    
if __name__ == '__main__':
    prank = InstagramPrank()