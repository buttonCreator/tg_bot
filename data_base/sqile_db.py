import sqlite3 as sq
from create_bot import bot, storage

def sql_start():
    global base, cur
    base = sq.connect('banks1.sqlite')
    cur = base.cursor()


async def sql_check_user(state):
    print('aaaa')
    print(state)
    print(state.proxy())
    async with state.proxy() as data:
        banks = ['Sber', 'Tinkoff', 'Rencredit']

        def checking_banks(banks, data):
            banks_rus = ['СберБанк', 'Тинькофф Банк', 'Ренесанс Кредит']
            my_banks = []
            for i in range(len(banks)):
                sql = "SELECT * FROM {} WHERE surname={} AND name={} AND fathername={}"
                surname = str('\'') + data['secondName'] + str('\'')
                name = str('\'') + data['firstName'] + str('\'')
                fathername = str('\'') + data['middleName'] + str('\'')
                cur.execute(sql.format(banks[i], surname, name, fathername))
                result = cur.fetchall()
                if len(result) == 1:
                    my_banks.append(banks_rus[i])
                    pasport = result[0][0]
            return my_banks, pasport

        my_banks1, pasport = checking_banks(banks, data)

        def text_banks(data):
            str1 = ''
            for i in data:
                str1 = str1 + i + ', '
            stroka = f'Я нашел Вас в банках: {str1}'
            return stroka

        await bot.answer(text_banks(my_banks1))
