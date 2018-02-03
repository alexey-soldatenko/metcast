import tkinter
from meteo.metcast import code_dict, wind_deg, weather_icon
import datetime
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class MyWeatherWidget:
	def __init__(self, city, metcast_for_five_days):
		self.root = tkinter.Tk()
		self.root.configure(background='#F5F5F5')
		self.root.title('Прогноз погоды на 5 дней')
		self.root.geometry('300x250')
		self.root.resizable(False, False)
		
		#виджет даты и времени прогноза
		self.choose_date = tkinter.Label(self.root, background='#F5F5F5')
		self.choose_date.pack()
		
		#основные иконки прогнозируемых данных
		self.temp_icon = tkinter.PhotoImage(file = 'img/service/temperature.png')
		self.humidity_icon = tkinter.PhotoImage(file = 'img/service/humidity.png')
		self.cloudiness_icon = tkinter.PhotoImage(file = 'img/service/cloudiness.png')
		self.wind_icon = tkinter.PhotoImage(file = 'img/service/wind.png')
		
		#город
		self.city = tkinter.Label(self.root, text = city, font = ('helvetica', 15), background='#F5F5F5')
		self.city.pack()
		
		#контейнер для линейки с днями недели
		self.days_frame = tkinter.Frame(self.root, pady = 5, background = '#F5F5F5')
		self.days_frame.pack()
		
		#данные прогноза на 5 дней
		self.metcast = metcast_for_five_days
		
		#контейнер для общего описания погоды
		self.weather_frame = tkinter.Frame(self.root, background='#F5F5F5')
		self.weather_frame.pack()
		
		#контейнер для метео-данных
		self.meteo_data_frame = tkinter.Frame(self.root, background='#F5F5F5', width = 200)
		self.meteo_data_frame.pack()
		
		#определяем расположение основных виджетов
		self.widgets_location()
		
		#контейнер для кнопок переключения во времени
		self.bottom_frame = tkinter.Frame(self.root, background = '#F5F5F5')
		self.bottom_frame.pack()
		
		#кнопка назад на 3ч
		self.left_arrow = tkinter.PhotoImage(file = 'img/service/left_arrow.png')
		self.button_back = tkinter.Button(self.bottom_frame, image = self.left_arrow, command = self.but_back)
		self.button_back.grid(row = 0, column = 0, sticky = 's', pady = 2)
		
		#ползунок для наглядности показа времени
		self.days_options = tkinter.Scale(self.bottom_frame, from_ = 2, to = 23, command = self.scale_calculation, orient = 'horizontal', background='#F5F5F5', highlightbackground='#F5F5F5', width = 13, length = 200)
		self.days_options.grid(row = 0, column = 1, sticky = 's')
		self.current_time = 2
		
		#кнопка вперед на 3ч
		self.right_arrow = tkinter.PhotoImage(file = 'img/service/right_arrow.png')
		self.button_to_future = tkinter.Button(self.bottom_frame, image = self.right_arrow, command = self.but_click)
		self.button_to_future.grid(row = 0, column = 2, sticky = 's', pady = 2)
		
		#получаем дни и соответствующие им индексы списка данных
		self.handle_days()	
		#создаём кнопки переключения между днями недели	
		self.buttons_for_days()
		
		#текущая страница (индекс в списке данных 0-39)
		#прогноз на 5 дней разбит на 40 частей, с разницей в 3ч
		self.current_page = 0
		
		#заносим необходимые значения в виджеты на текущий момент времени
		self.current_weather(self.current_page)		
 
		
	
	def widgets_location(self):
		#общее описание погоды
		self.weather = tkinter.Label(self.weather_frame, background='#F5F5F5', font = ('helvetica', 11))
		self.weather.grid(row = 0, column = 2, columnspan = 2, sticky="nsew")
		
		#иконка прогноза
		self.icon = tkinter.Label(self.weather_frame, background='#F5F5F5')
		self.icon.grid(row = 0, column = 0, columnspan = 2, padx = 10)
		
		#температура
		self.temp_desc = tkinter.Label(self.meteo_data_frame, image = self.temp_icon, background='#F5F5F5')
		self.temp_desc.grid(row = 1, column = 0, sticky="nsew", padx = 5)
		self.temp = tkinter.Label(self.meteo_data_frame, background='#F5F5F5', anchor = 'w')
		self.temp.grid(row = 1, column = 1, sticky="nsew")
		
		#влажность
		self.humidity_desc = tkinter.Label(self.meteo_data_frame, image = self.humidity_icon, background='#F5F5F5', anchor = 'e')
		self.humidity_desc.grid(row = 1, column = 2, sticky="nsew", padx = 5)
		self.hum = tkinter.Label(self.meteo_data_frame, background='#F5F5F5', anchor = 'w')
		self.hum.grid(row = 1, column = 3, sticky="nsew")
		
		#облачность
		self.clouds_desc = tkinter.Label(self.meteo_data_frame, image = self.cloudiness_icon, background='#F5F5F5', anchor = 'e')
		self.clouds_desc.grid(row = 2, column = 0, sticky="nsew", padx = 5)
		self.cloudiness = tkinter.Label(self.meteo_data_frame, background='#F5F5F5', anchor = 'w')
		self.cloudiness.grid(row = 2, column = 1, sticky="nsew")
		
		#ветер
		self.wind_desc = tkinter.Label(self.meteo_data_frame, image = self.wind_icon, background='#F5F5F5', anchor = 'e')
		self.wind_desc.grid(row = 2, column = 2, sticky="nsew", padx = 5)
		self.wind = tkinter.Label(self.meteo_data_frame, background='#F5F5F5', anchor = 'w')
		self.wind.grid(row = 2, column = 3, sticky="nsew")	
		
	def current_weather(self, choose_time):
		'''функция для определения прогноза и его отображения в зависимость от выбранного времени (индекса 0-39)'''
		
		self.current_page = choose_time
		#выбранная дата прогноза
		date = datetime.datetime.fromtimestamp(self.metcast[choose_time]['dt'])
		self.current_time = int(datetime.datetime.strftime(date, '%H'))
		
		#отображение выбранного времени на ползунке
		self.days_options.set(self.current_time)
		
		num_current_but = 0
		#выделяем цветом текущий день
		for day in self.days:
			if choose_time in day[1]:
				current_day_button = self.days_frame.winfo_children()[num_current_but]
				current_day_button.configure(bg = '#FF8C00')
			else:
				current_day_button = self.days_frame.winfo_children()[num_current_but]
				current_day_button.configure(bg = '#F5F5F5')
			num_current_but += 1
		
		#отображаем дату и время
		date_text = datetime.datetime.strftime(date, '%A %d/%m/%Y (%H:%M)')		
		self.choose_date.configure(text = date_text)
		
		#общее описание погоды
		weather_code = self.metcast[choose_time]['weather'][0]['id'] 
		weather_desc = code_dict[weather_code]
		self.weather.configure(text = weather_desc)
		
		#иконка прогноза
		icon_name = weather_icon(weather_code)
		self.weather_photo = tkinter.PhotoImage(file = icon_name)
		self.icon.configure(image = self.weather_photo)
		
		#температура (из K->C)
		temperature = int(self.metcast[choose_time]['main']['temp'])-273
		out_temperature = str(temperature) + '\u00B0' + 'C'
		self.temp.configure(text = out_temperature)
		
		#влажность
		humidity = str(self.metcast[choose_time]['main']['humidity']) + '%'
		self.hum.configure(text = humidity)
		
		#облачность
		clouds = str(self.metcast[choose_time]['clouds']['all']) + '%'
		self.cloudiness.configure(text = humidity)
		
		#ветер
		wind_deg_code = self.metcast[choose_time]['wind']['deg']
		wind = wind_deg(wind_deg_code)
		wind_speed = str(self.metcast[choose_time]['wind']['speed'])
		wind_text = wind + ' ' + wind_speed + 'м/с'
		self.wind.configure(text = wind_text)
		
	def handle_days(self):
		'''функция для получения списка дней недели и соответствующих им индексов списка данных, т.е
		[0,1,2....39] -> [[['Вторник'], [0,1,2]], [['Среда'], [3,4,5,6,7,8,9,10], [['Четверг'], [11,12,13,14,15,16,17,18]], ...]'''
		
		#определяем число первого дня
		first_day = datetime.datetime.fromtimestamp(self.metcast[0]['dt']).day
		current_day = first_day
		self.days = []
		one_day = []
		i = 0
		for item in self.metcast:
			date = datetime.datetime.fromtimestamp(item['dt'])
			#определяем число текущего дня
			num_day = date.day
			if num_day == current_day:
				if i == 39:
					one_day.append(i)
					current_day = num_day
					#определяем аббревиатуру дня
					day_name = self.weekday_abbr(day_name)
					self.days.append([[day_name],one_day])
				else:	
					#заполняем список one_day индексами соотв. этому дню	
					one_day.append(i)
					day_name = datetime.datetime.strftime(date, '%A')
			else:
				current_day = num_day
				#определяем аббревиатуру дня
				day_name = self.weekday_abbr(day_name)
				self.days.append([[day_name],one_day])
				del one_day
				one_day = [i]
			i += 1

		
	def but_click(self):
		'''функция для просмотра прогноза на 3ч вперёд'''
		if self.current_page < 39:
			self.current_page = self.current_page + 1
			self.current_weather(self.current_page)
		
	def but_back(self):
		'''функция для просмотра проноза на 3ч назад'''
		if self.current_page > 0:
			self.current_page = self.current_page - 1
			self.current_weather(self.current_page)
			
	def scale_calculation(self, event):
		'''функция для обработки событий ползунка'''
		#игнорируем все события, выставляем ползунок в то положение, в котором он находится сейчас
		self.days_options.set(self.current_time)
		
	def buttons_for_days(self):
		'''функция для создания кнопок для каждого отдельного дня недели'''
		i = 0
		for item in self.days:
			but = tkinter.Button(self.days_frame, text = self.days[i][0])
			but.configure(command = lambda i=i: self.current_weather(self.days[i][1][0]))
			but.grid(row = 0, column = i)
			i += 1
		
	def weekday_abbr(self, day_name):
		'''функция для получения аббревиатуры дня недели'''
		if day_name == 'Понедельник':
			return 'Пн'
		elif day_name == 'Вторник':
			return 'Вт'
		elif day_name == 'Среда':
			return 'Ср'
		elif day_name == 'Четверг':
			return 'Чт'
		elif day_name == 'Пятница':
			return 'Пт'
		elif day_name == 'Суббота':
			return 'Сб'
		else:
			return 'Вс'
			
