#Note: Data from Ministry of Health and Family Welfare India.

import requests   #To send requests to website
import bs4   #For web scrapping
import tkinter as tk   #To generate UI
import plyer   #For windows notifications
import time
import threading

def get_html_data(url):
    data = requests.get(url) #gets data of this url in html format.
    return data

def get_corona_detail_of_india():
    url = 'https://www.mohfw.gov.in/'
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text,'html.parser')
    #The data is of type response and to get the actual data we use .txt format
    # data is printed/parserd  in a preety format using indentation.

    info_div = bs.find('div',class_='col-xs-8 site-stats-count').find('ul').find_all('li')
    # Here we used inspect element to check which div conatins the data we desire.
    # beautifulsoup.find is a method which will find all the divs containing class as given.

    #This gives us a list of all li's (3 li)
    data = []
    number = []
    all_details = ''
    for item in info_div:
        data_str = item.select('strong')[0].text
        data_str = data_str.replace(u'\xa0', u'')
        data_str = data_str[:-1]
        data.append(data_str)

        number_str = item.select('strong')[1].text
        number_str = number_str.replace(u'\xa0', u'')
        loc = number_str.find('(')
        number_str = number_str[0:loc]
        number.append(number_str)

        all_details = all_details+data_str+" : "+number_str+"\n"
    return all_details

#Funcuton used to reload the data from website
def refresh():
    new_data = get_corona_detail_of_india()
    print('refreshing')
    mainLabel['text'] = new_data

#Funciton for notifications
def notify_me():
    while True:
        #Creating notification using plyer
        plyer.notification.notify(
            title = 'Covid-19 stats India',
            message = get_corona_detail_of_india(),
            timeout = 15, #Time duration for viewing
        )
        time.sleep(3000)


#Creating GUI
root = tk.Tk()
root.geometry("500x500") #Setting width and height
root.title('CORONA TRACKER- INDIA')
root.configure(background='white')
f = ("poppins",22,'bold')
fbtn = ("poppins",15,'bold')

banner = tk.PhotoImage(file='Image/superhero and germ teaser.png')
banner = banner.zoom(22) #Resizing zoom
banner = banner.subsample(32)
bannerLabel = tk.Label(root,image=banner) #For image
bannerLabel.pack()


mainLabel = tk.Label(root,text=get_corona_detail_of_india(),font=f,bg='white') #For data
mainLabel.pack()

reBtn = tk.Button(root,text='Refresh',font=f,command=refresh) #For button
reBtn.pack()

#Create a new thread
th1 = threading.Thread(target=notify_me)
th1.setDaemon(True) #Closes the thread when application is closed.
th1.start() #Creatig a new thread for notifications

root.mainloop()

def main():
    print(get_corona_detail_of_india())


#If main is present within the code, it will automatically call main.
if __name__ == '__main__':
    main()