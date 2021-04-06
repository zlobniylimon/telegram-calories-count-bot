import re
import db
import exceptions
from typing import NamedTuple
import time

class Food(NamedTuple):
	food_name: str
	calories: int

def _parse_message(message: str):
	"""Парсит сообщение и достает название продукта и его калораж"""
	parsed = re.findall(r'(.+) (\d+)', message)

	if parsed == []:
		raise exceptions.NotCorrectMessage("Не смог прочитать сообщение. Повторите запрос")

	food = Food(food_name=parsed[0][0], calories=int(parsed[0][1]))

	return food

def add_cal(text):
	"""Добавляет Food в базу"""
	food = _parse_message(text)
	db.insert(calories = food.calories, food_name = food.food_name)

	return food

def daily_cal():	
	data = db.fetch_all()
	answer = ''
	summary = 0

	# return data

	for row in data:
		if int(time.strftime('%d')) == time.strptime(row[3],"%Y-%m-%d").tm_mday:
			answer+=str(row[1])+' - '+str(row[2])+' ккал\n'
			summary += row[2]

	if answer == '':
		answer = "Вы еще ничего не ели? :("
	else:
		answer += '*Всего за день: *' +str(summary)+' ккал'

	return answer
