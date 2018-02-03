import urllib.request
import re
import json
import datetime

code_dict = {
	200: 'Слабый дождь',
	201: 'Гроза с дождём',
	202: 'Гроза с сильным дождём',
	210: 'Слабая гроза',
	211: 'Гроза',
	212: 'Сильная гроза',
	221: 'Периодическая гроза',
	230: 'Гроза со слабым дождём',
	231: 'Гроза с дождём',
	232: 'Гроза с сильным дождём',
	
	300: 'Слабый дождь',
	301: 'Слабый дождь',
	302: 'Дождь',
	310: 'Дождь',
	311: 'Дождь',
	312: 'Дождь',
	313: 'Дождь',
	314: 'Сильный дождь',
	321: 'Сильный дождь',
	
	500: 'Слабый дождь',
	501: 'Дождь',
	502: 'Сильный дождь',
	503: 'Очень сильный дождь',
	504: 'Экстремальный дождь',
	511: 'Ледяной дождь',
	520: 'Проливной дождь',
	521: 'Проливной дождь',
	522: 'Проливной дождь',
	531: 'Сильный проливной дождь',
	
	600: 'Слабый снег',
	601: 'Снег',
	602: 'Сильный снег',
	611: 'Снег с дождем',
	612: 'Проливной дождь со снегом',
	615: 'Легкий снег с дождём',
	616: 'Снег с дождем',
	620: 'Снегопад',
	621: 'Снегопад',
	622: 'Сильный снегопад',
	
	701: 'Туман',
	711: 'Дымка',
	721: 'Туман',
	731: 'Пылевые завихрения',
	741: 'Туман',
	751: 'Пысочные завихрения',
	761: 'Пылевые завихрения',
	762: 'Вулканический пепел',
	771: 'Шквал',
	781: 'Ураган',

	800: 'Чистое небо',
	801: 'Малооблачно',
	802: 'Рассеянная облачность',
	803: 'Облачно',
	804: 'Облачно',
	
	900: 'Ураган',
	901: 'Тропический шторм',
	902: 'Ураган',
	903: 'Холодно',
	904: 'Жарко',
	905: 'Ветренно',
	906: 'Град',
	951: 'Безветренно',
	952: 'Слабый ветер',
	953: 'Слабый ветер',
	954: 'Умеренный ветер',
	955: 'Сильный ветер',
	956: 'Сильный ветер',
	957: 'Шторм',
	958: 'Шторм',
	959: 'Сильный шторм',
	960: 'Сильный шторм',
	961: 'Сильный шторм',
	962: 'Сильный шторм',

}

def wind_deg(deg):
	''' функция для определения названия направлению ветра по его градусу'''
	if deg > 337.5:
		return 'Сев.'
	elif deg > 292.5:
		return 'С-З'
	elif deg > 247.5:
		return 'Зап.'
	elif deg > 202.5:
		return 'Ю-З'
	elif deg > 157.5:
		return 'Южн.'
	elif deg > 122.5:
		return 'Ю-В'
	elif deg > 67.5:
		return 'Вост.'
	elif deg > 22.5:
		return 'С-В'
	else:
		return 'Сев.'

def weather_icon(code):
	''' функция для определения иконки погоды в соответствии с кодом-идетификатором'''
	group_code = int(code/100)
	if group_code == 2:
		return 'img/weather/thunderstorm.png'
	elif group_code == 3:
		return 'img/weather/shower_rain.png'
	elif group_code == 5:
		bit_code = code - 500
		if bit_code < 10:
			return 'img/weather/rain.png'
		else:
			return 'img/weather/shower_rain.png'
	elif group_code == 6:
		return 'img/weather/snow.png'
	elif group_code == 7:
		return 'img/weather/mist.png'
	elif group_code == 8:
		if code == 800:
			return 'img/weather/clear_sky.png'
		elif code == 801:
			return 'img/weather/few_clouds.png'
		elif code == 802:
			return 'img/weather/clouds.png'
		else:
			return 'img/weather/many_clouds.png'
	elif group_code == 9:
		if code < 903 or code > 954:
			return 'img/weather/thunderstorm.png'
		else:
			return 'img/weather/clear_sky.png'

def weather_by_coord():
	''' фуекция для получения данных прогноза погоды на 5 дней в зависимости от географического положения'''
	
	#определяем свой внешний ip
	ip_url = 'http://ipecho.net'
	data = urllib.request.urlopen(ip_url).read()
	data = data.decode("utf-8")

	ip = re.search(r'\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}', data).group(0)
	
	#определяем свои координаты по ip-адресу
	coord = urllib.request.urlopen('https://freegeoip.net/json/{0}'.format(ip)).read()
	coord = coord.decode("utf-8")
	coord = json.loads(coord)

	latitude = coord['latitude']
	longitude = coord['longitude']

	#отправляем запрос для получения прогноза
	weather_data = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?lat={0}&lon={1}&appid=2aa921cfd8d3d14f40c541452725e8be'.format(latitude, longitude)).read()

	weather_data = weather_data.decode('utf-8')
	weather_data = json.loads(weather_data)
	
	city = weather_data['city']["name"]
	five_days = weather_data['list']

	return city, five_days



