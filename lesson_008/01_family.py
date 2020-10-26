# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint

######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.



class House:

    def __init__(self):
        self.money = 100
        self.ref_food = 50
        self.dirt = 0
        self.family = []

    def __str__(self):
        self.dirt += 5
        return '{} денег в доме, еды в доме {}, грязь {}'.format(self.money, self.ref_food, self.dirt)


class Human:

    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.house = None

    def act(self):
        if self.happiness < 0:
            del self.house.family[self.house.family.index(member)]
            cprint('{} УМЕР{}ОТ ДЕПРЕССИИ'.format(self.name, ' ' if self.__class__.__name__ == 'Husband' else 'ЛА '),
                   'red', attrs=['reverse'])
            return False
        if self.fullness < 0:
            del self.house.family[self.house.family.index(member)]
            cprint('{} УМЕР{}ОТ ГОЛОДА'.format(self.name, ' ' if self.__class__.__name__ == 'Husband' else 'ЛА '),
                   'red', attrs=['reverse'])
            return False
        self.fullness -= 10

    def eat(self):
        if self.house.ref_food >= 10:
            self.fullness += 30
            self.house.ref_food -= 10
            print('{} поел{}'.format(self.name, '' if self.__class__.__name__ == 'Husband' else 'а'))
        else:
            cprint('{} собрался поесть'.format(self.name))
            cprint('Недостаточно еды!', color='red')

    def move_in(self, house):
        self.house = house
        self.house.family.append(self)

    def __str__(self):
        if self.house.dirt >= 90:
            self.happiness -= 10
        return 'Я {}, сытость {}, уровень счастья {}'.format(self.name, self.fullness, self.happiness)


class Husband(Human):

    def act(self):
        if super().act() is False:
            return
        if self.fullness <= 10:
            self.eat()
            return
        dice = randint(1, 6)
        if dice in range(1, 3):
            self.work()
        elif dice == 4:
            self.eat()
        else:
            self.gaming()

    def work(self):
        house = self.house
        cprint('{} весь день работал'.format(self.name), color='yellow')
        house.money += 150

    def gaming(self):
        super().act()
        dice = randint(1, 6)
        if dice == 1:
            self.happiness += 20
            cprint('{} весь день бездельничал'.format(self.name), color='yellow')
        elif dice == 2:
            self.happiness += 20
            cprint('{} весь день смотрел телевизор'.format(self.name), color='yellow')
        else:
            self.happiness += 20
            cprint('{} весь день играл в доту'.format(self.name), color='yellow')


class Wife(Human):

    def act(self):
        if super().act() is False:
            return
        if self.fullness <= 10:
            self.eat()
            return
        if self.house.ref_food < 20:
            self.shopping()
        dice = randint(1, 6)
        if dice == 1:
            self.buy_fur_coat()
        elif dice == 2:
            self.nagging()
        elif dice == 4:
            self.eat()
        elif dice == 6:
            self.shopping()
        elif dice == 5:
            if self.house.dirt >= 100:
                self.clean_house()
            else:
                return
        else:
            print('{} бездельничала'.format(self.name))

    def nagging(self):
        if self.happiness < 50:
            for i in self.house.family:
                if i.__class__.__name__ == 'Husband':
                    self.happiness += 50
                    i.happiness -= 50
                    cprint('{} капает на мозги {}'.format(self.name, i.name), 'blue', attrs=['reverse'])
                else:
                    return False

    def shopping(self):
        if self.house.money < 180:
            cprint('Недостаточно денег!', 'green', attrs=['reverse'])
            return
        self.house.ref_food += 180
        self.house.money -= 180
        print('{} сходила в магазин за едой'.format(self.name))

    def buy_fur_coat(self):

        if self.house.money < 350:
            cprint('{} пытается купить шубу'.format(self.name))
            cprint('Недостаточно денег!', 'green', attrs=['reverse'])
            self.happiness -= 10
            return
        self.house.money -= 350
        self.happiness += 60
        print('{} купила шубу'.format(self.name))

    def clean_house(self):
        self.house.dirt -= 100
        print('{} убиралась в доме'.format(self.name))


home = House()
hus = Husband('Сережа')
wife = Wife('Маша')
hus.move_in(home)
wife.move_in(home)

# for member in home.family:
#     member.move_in(home)
# masha = Wife(name='Маша')

for day in range(300):
    if not home.family:
        break
    cprint('================== День {} =================='.format(day), color='red')
    for member in home.family:
        member.act()
        cprint(member, color='cyan')
    # cprint(masha, color='cyan')
    cprint(home, color='cyan')



# TODO после реализации первой части - отдать на проверку учителю

######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


class Cat:

    def __init__(self):
        pass

    def act(self):
        pass

    def eat(self):
        pass

    def sleep(self):
        pass

    def soil(self):
        pass


######################################################## Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)

# class Child:
#
#     def __init__(self):
#         pass
#
#     def __str__(self):
#         return super().__str__()
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass


# TODO после реализации второй части - отдать на проверку учителем две ветки


######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.

#
# home = House()
# serge = Husband(name='Сережа')
# masha = Wife(name='Маша')
# kolya = Child(name='Коля')
# murzik = Cat(name='Мурзик')
#
# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#     serge.act()
#     masha.act()
#     kolya.act()
#     murzik.act()
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')

