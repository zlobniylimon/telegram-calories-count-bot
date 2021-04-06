from aiogram import Bot, Dispatcher, executor, types 
from decouple import config
import logging
import control
import exceptions
import os 

API_TOKEN = config("API_TOKEN")

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start','help'])
async def send_welcome(message: types.Message):
	""" Вывод списка комманд при старте бота и вызова хелпа"""
	await message.answer(
				'Список комманд:\n'
            	' - *\\d* - Список продуктов и их калорий за этот день\n'
                ' - *<название_продукта> <ккал>* - Добавить продукт и его калории к съеденым продуктам',
                parse_mode = 'markdown'
            )

@dp.message_handler(commands=['day'])
async def daily_cal(message:types.Message):
	""" Вывод списка продуктов, которые внесены в базу сегодня"""
	answer =control.daily_cal()
	await message.answer(answer, parse_mode='markdown')
	

@dp.message_handler(commands=['week'])
async def weekly_cal(message: types.Message):
	# data = control.weekly_cal()
	await message.answer('Среднее количество калорий за неделю')

@dp.message_handler()
async def add_cal(message: types.Message):
	"""Добавить продукт и его калораж в базу"""
	try:
		answer = control.add_cal(message.text)
	except exceptions.NotCorrectMessage as e:
		await message.answer(str(e))
		return
	await message.answer(f'Добавлена следующая еда:\n'
						 f'{answer.food_name}\n'
						 f'{answer.calories} ккал')

if __name__=="__main__":
	executor.start_polling(dp, skip_updates=True)
