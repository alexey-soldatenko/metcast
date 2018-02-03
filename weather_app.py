from meteo.metcast import weather_by_coord
from widget.weather_widget import MyWeatherWidget
import tkinter
from tkinter import messagebox

try:
	city, five_days = weather_by_coord()
except Exception as err:
	#скрытое главное окно
	root = tkinter.Tk()
	root.withdraw()
	 
	#сообщение об ошибке
	messagebox.showerror("Ошибка", "Проверьте подключение к интернету")
else:
	my_widget = MyWeatherWidget(city, five_days)
	my_widget.root.mainloop()
