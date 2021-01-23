from tkinter import *
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox

root = Tk()

root.title('Covid-19')
root.state('zoomed')

globalurl = "https://api.covid19api.com/world/total"
globalresponse = requests.get(globalurl)
global_bilgileri = globalresponse.json()

frame = Frame(root)
lframe = Frame(frame)
gframe = Frame(root)
tframe = Frame(root)

frame.pack(side=LEFT)
lframe.pack()
tframe.pack(side=TOP)
gframe.pack(fill=BOTH)

ulkelerlabel = Label(lframe, text="Ülkeler:", font=("Helvetica", 16))
grafiklabel = Label(frame, text="Grafikler:", font=("Helvetica", 16))

globalvakalar = global_bilgileri["TotalConfirmed"]
globalolumler = global_bilgileri["TotalDeaths"]
globaliyilesen = global_bilgileri["TotalRecovered"]

global_label = Label(tframe, text="Dünya Geneli-> Toplam Vaka: " + str(globalvakalar) + " Toplam Ölümler: " + str(
    globalolumler) + " Toplam İyileşen: " + str(globaliyilesen), font='Helvetica 13 bold')
global_label.pack(side=TOP)
ulkeler_list = []

ulkeler = Listbox(lframe, exportselection=0)

scroolbar = Scrollbar(lframe, orient="vertical")
scroolbar.config(command=ulkeler.yview)
ulkeler.config(width=0, height=50, yscrollcommand=scroolbar.set)

grafik = Listbox(frame, exportselection=0)
grafik.config(width=0, height=0)

grafik.insert("end", "Toplam Vaka Grafiği")
grafik.insert("end", "Toplam İyileşen grafiği")
grafik.insert("end", "Toplam Ölüm Grafiği")
grafik.insert("end", "Günlük Aktif Vakalar Grafiği")
grafik.insert("end", "Günlük Ölümler Grafiği")
grafik.insert("end", "Günlük İyileşenler Grafiği")
grafik.insert("end", "Günlük Onaylanmış Vakalar Grafiği")

ulkeurl = "https://api.covid19api.com/countries"

response = requests.get(ulkeurl)

ulke_bilgileri = response.json()

for x in ulke_bilgileri:
    ulkeler_list.append(x["Country"])

ulkeler_list.sort()

for eleman in ulkeler_list:
    ulkeler.insert("end", eleman)


def click():
    for widget in gframe.winfo_children():
        widget.destroy()
    y_ekseni = []
    tarih = []
    secim = ulkeler.get(ulkeler.curselection())
    grafik_secim = grafik.get(grafik.curselection())
    for i in ulke_bilgileri:
        if secim == i["Country"]:
            secilen_ulke = i["Slug"]
    if secilen_ulke != "australia":
        grafik_url = "https://api.covid19api.com/total/dayone/country/" + secilen_ulke
    else:
        grafik_url = "https://api.covid19api.com/dayone/country/" + secilen_ulke

    toplam_vaka = requests.get(grafik_url)

    vaka_bilgileri = toplam_vaka.json()

    fig = Figure(figsize=(25, 10))
    graf = fig.add_axes([0.05, 0.1, 0.9, 0.85])
    graf.set_xlabel("Tarihler")
    graf.set_ylabel("Veriler")
    graf.set_title(grafik_secim +": " + secim)

    if grafik_secim == "Toplam Vaka Grafiği":

        for a in vaka_bilgileri:
            y_ekseni.append(a["Confirmed"])
            duzenle = a["Date"]
            duzenle = datetime.strptime(duzenle, '%Y-%m-%dT%H:%M:%SZ')
            tarih1 = duzenle.strftime("%d-%m-%Y")
            tarih.append(tarih1)

        graf.plot(tarih, y_ekseni)


    if grafik_secim == "Günlük Aktif Vakalar Grafiği":
        for c in vaka_bilgileri:
            y_ekseni.append(c["Active"])
            duzenle = c["Date"]
            duzenle = datetime.strptime(duzenle, '%Y-%m-%dT%H:%M:%SZ')
            tarih1 = duzenle.strftime("%d-%m-%Y")
            tarih.append(tarih1)

        graf.bar(tarih, y_ekseni)



    if grafik_secim == "Toplam İyileşen grafiği":
        for c in vaka_bilgileri:
            y_ekseni.append(c["Recovered"])
            duzenle = c["Date"]
            duzenle = datetime.strptime(duzenle, '%Y-%m-%dT%H:%M:%SZ')
            tarih1 = duzenle.strftime("%d-%m-%Y")
            tarih.append(tarih1)

        graf.plot(tarih, y_ekseni)



    if grafik_secim == "Toplam Ölüm Grafiği":
        for b in vaka_bilgileri:
            y_ekseni.append(b["Deaths"])
            duzenle = b["Date"]
            duzenle = datetime.strptime(duzenle, '%Y-%m-%dT%H:%M:%SZ')
            tarih1 = duzenle.strftime("%d-%m-%Y")
            tarih.append(tarih1)

        graf.plot(tarih, y_ekseni)



    if grafik_secim == "Günlük Ölümler Grafiği":

        gun = []
        for a in vaka_bilgileri:
            y_ekseni.append(a["Deaths"])

            duzenle = a["Date"]
            duzenle = datetime.strptime(duzenle, '%Y-%m-%dT%H:%M:%SZ')
            tarih1 = duzenle.strftime("%d-%m-%Y")
            tarih.append(tarih1)
        list1 = y_ekseni.copy()
        list1.insert(0, 0)
        i = 0

        while i < len(y_ekseni):
            a = y_ekseni[i] - list1[i]
            gun.append(a)
            i += 1

        graf.bar(tarih, gun)



    if grafik_secim == "Günlük İyileşenler Grafiği":
        gun = []
        for a in vaka_bilgileri:
            y_ekseni.append(a["Recovered"])

            duzenle = a["Date"]
            duzenle = datetime.strptime(duzenle, '%Y-%m-%dT%H:%M:%SZ')
            tarih1 = duzenle.strftime("%d-%m-%Y")
            tarih.append(tarih1)
        list1 = y_ekseni.copy()
        list1.insert(0, 0)
        i = 0

        while i < len(y_ekseni):
            a = y_ekseni[i] - list1[i]
            gun.append(a)
            i += 1

        graf.bar(tarih, gun)



    if grafik_secim == "Günlük Onaylanmış Vakalar Grafiği":
        gun = []
        for a in vaka_bilgileri:
            y_ekseni.append(a["Confirmed"])

            duzenle = a["Date"]
            duzenle = datetime.strptime(duzenle, '%Y-%m-%dT%H:%M:%SZ')
            tarih1 = duzenle.strftime("%d-%m-%Y")
            tarih.append(tarih1)
        list1 = y_ekseni.copy()
        list1.insert(0, 0)
        i = 0

        while i < len(y_ekseni):
            a = y_ekseni[i] - list1[i]
            gun.append(a)
            i += 1

        graf.bar(tarih, gun)


    plt.setp(graf.xaxis.get_majorticklabels(), rotation=90)
    plt.gca().set_position([0, 0, 1, 1])

    graf.grid()

    canv = FigureCanvasTkAgg(fig, master=gframe)
    canv.draw()
    toolbar = NavigationToolbar2Tk(canv, gframe)
    toolbar.update()
    get_widz = canv.get_tk_widget()

    get_widz.pack()
    
def on_closing():
    if messagebox.askokcancel("Çıkış", "Çıkmak istediğinize emin misiniz?"):
        root.quit()

buton = Button(frame, text='Çiz', command=click)
buton.config(width=20, height=1)
scroolbar.pack(side=RIGHT, fill=Y)
ulkelerlabel.pack()
grafiklabel.pack()
ulkeler.pack()

grafik.pack()
buton.pack()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
