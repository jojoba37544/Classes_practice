# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint, choice


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


def printer(str, color, length, direction='right', attrs=None, end=None):
    empty_space = '{}'.format(' ' * int(length - len(str)))
    if direction == 'right':
        return cprint(empty_space, color, attrs=attrs, end=''), cprint(str, color, end=end)
    elif direction == 'left':
        return cprint(str, color, end=''), cprint(empty_space, color, attrs=attrs, end=end)


class LifeResults:
    pass


class House:

    ref_capacity = 360
    pet_food_capacity = 180
    happiness_maximum = 100

    def __init__(self):
        self.money = 100
        self.ref_food = 50
        self.dirt = 0
        self.family = []
        self.pet = None
        self.results = '{} денег в доме, еды в доме {}, грязь {}'.format(self.money, self.ref_food, self.dirt)

    def __str__(self):
        self.dirt += 5
        return self.results

    def __len__(self):
        return len(self.__str__())


class Human:

    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.house = None

    def act(self):
        if self.happiness < 0:
            del self.house.family[self.house.family.index(self)]
            if self.__class__.__name__ == 'Husband' or self.__class__.__name__ == 'Child':
                cprint('{} УМЕР ОТ ДЕПРЕССИИ'.format(self.name), 'red', attrs=['reverse'])
            else:
                cprint('{} УМЕРЛА ОТ ДЕПРЕССИИ'.format(self.name), 'red', attrs=['reverse'])
            return False
        if self.fullness < 0:
            del self.house.family[self.house.family.index(self)]
            if self.__class__.__name__ == 'Husband' or self.__class__.__name__ == 'Child':
                cprint('{} УМЕР ОТ ГОЛОДА'.format(self.name), 'red', attrs=['reverse'])
            else:
                cprint('{} УМЕРЛА ОТ ГОЛОДА'.format(self.name), 'red', attrs=['reverse'])
            return False
        self.fullness -= 10

    def pet_interaction(self):
        self.happiness += 5
        cprint('{} гладил кота {}'.format(self.name, self.house.pet), self.color)

    def eat(self):
        if self.house.ref_food >= 10:
            self.fullness += 40
            self.house.ref_food -= 10
            cprint('{} поел{}'.format(self.name, '' if self.__class__.__name__ == 'Husband' else 'а'), self.color)
        else:
            cprint('{} собрался поесть'.format(self.name), self.color)
            cprint('Недостаточно еды!', 'red', attrs=['reverse'])

    def move_in(self, house):
        self.house = house
        self.house.family.append(self)

    def __str__(self):
        if self.house.dirt >= 90:
            self.happiness -= 10
        return 'Сытость {}, уровень счастья {}'.format(self.fullness, self.happiness)

    def __len__(self):
        return len(self.__str__())


class Husband(Human):
    def __init__(self, name):
        super().__init__(name=name)
        self.color = 'blue'

    def act(self):
        if super().act() is False:
            return
        if self.fullness <= 10:
            self.eat()
            return
        if self.house.money < 180:
            self.work()
            return
        dice = randint(1, 6)
        if dice in range(1, 2, 3):
            self.work()
        elif dice == 4:
            self.eat()
        elif dice == 5:
            if self.house.pet:
                self.pet_interaction()
            else:
                self.gaming()
        else:
            self.gaming()

    def work(self):
        house = self.house
        cprint('{} весь день работал'.format(self.name), self.color)
        house.money += 150

    def gaming(self):
        dice = randint(1, 6)
        if dice == 1:
            self.happiness += 10
            cprint('{} весь день бездельничал'.format(self.name), self.color)
        elif dice == 2:
            self.happiness += 10
            cprint('{} весь день смотрел телевизор'.format(self.name), self.color)
        else:
            self.happiness += 10
            cprint('{} весь день играл в доту'.format(self.name), self.color)


class Wife(Human):

    def __init__(self, name):
        super().__init__(name=name)
        self.color = 'magenta'

    def act(self):
        if super().act() is False:
            return
        if self.fullness <= 20:
            self.eat()
            return
        if self.happiness < 20:
            self.nagging()
            return
        if self.house.dirt >= 100:
            self.clean_house()
            return
        if self.house.ref_food < 20:
            self.shopping()
            return
        if self.house.cat_food < 20:
            self.cat_food_replenish()
            return
        dice = randint(1, 6)
        if dice == 1:
            self.buy_fur_coat()
        elif dice == 4:
            self.eat()
        elif dice == 6:
            if self.house.ref_food < self.house.ref_capacity:
                self.shopping()
            else:
                cprint('{} бездельничала'.format(self.name), self.color)
        else:
            cprint('{} бездельничала'.format(self.name), self.color)

    def nagging(self):
        for fam_member in self.house.family:
            if fam_member.__class__.__name__ == 'Husband':
                self.happiness += 50
                fam_member.happiness -= 50
                cprint('{} капает на мозги {}'.format(self.name, fam_member.name), self.color)
            else:
                return False

    def cat_food_replenish(self):
        cprint('{} отправилась в магазине купить еды для кота {}'.format(self.name, self.house.pet))
        remain = self.house.pet_food_capacity - self.house.cat_food
        if self.house.money < 100:
            cprint('Недостаточно денег!', 'red', attrs=['reverse'])
            return
        elif remain < 100:
            self.house.money -= remain
            self.house.cat_food += remain
        else:
            self.house.cat_food += 180
            self.house.money -= 180

    def shopping(self):
        cprint('{} отправилась в магазин купить еды'.format(self.name), self.color)
        remain = self.house.ref_capacity - self.house.ref_food
        if self.house.money < 180:
            cprint('Недостаточно денег!', 'red', attrs=['reverse'])
            return
        elif remain < 180:
            self.house.money -= remain
            self.house.ref_food += remain
        else:
            self.house.ref_food += 180
            self.house.money -= 180
        cprint('{} купила еды'.format(self.name), self.color)

    def buy_fur_coat(self):
        if self.house.money < 350:
            cprint('{} хотела купить шубу'.format(self.name), self.color)
            cprint('Недостаточно денег!', 'red', attrs=['reverse'])
            self.happiness -= 10
            return
        self.house.money -= 350
        self.happiness += 60
        cprint('{} купила шубу'.format(self.name), self.color)

    def clean_house(self):
        self.house.dirt -= 100
        cprint('{} убиралась в доме'.format(self.name), self.color)


class Child(Human):

    def __init__(self, name):
        super().__init__(name=name)
        self.color = 'green'

    def act(self):
        if super().act() is False:
            return
        if self.fullness <= 20:
            self.eat()
            return
        dice = randint(1, 6)
        if dice == 1:
            self.eat()
        elif dice == 2:
            self.sleep()
        else:
            self.sleep()

    def eat(self):
        while True:
            fam_member = choice(self.house.family)
            if fam_member.__class__.__name__ == 'Husband' or fam_member.__class__.__name__ == 'Wife':
                break
        if len(self.house.family) <= 1:
            cprint('{} ОСТАЛСЯ ОДИН!, НЕКОМУ ЕГО ПОКОРМИТЬ!'.format(self.name))
            return
        if self.house.ref_food >= 10:
            self.fullness += 30
            self.house.ref_food -= 10
            if fam_member.__class__.__name__ == 'Husband':
                cprint('{} покормил {}а'.format(fam_member.name, self.name), self.color)
            elif fam_member.__class__.__name__ == 'Wife':
                cprint('{} покормила {}а'.format(fam_member.name, self.name), self.color)
        else:
            cprint('{} собирается покормить {}...'.format(fam_member, self.name), self.color)
            cprint('Недостаточно еды!', 'red', attrs=['reverse'])
            return

    def sleep(self):
        cprint('{} спал целый день'.format(self.name), self.color)

    def __str__(self):
        return 'Сытость {}, уровень счастья {}'.format(self.fullness, self.happiness)


class Cat:

    def __init__(self, name, house):
        self.name = name
        self.fullness = 30
        self.house = house
        self.color = 'yellow'

    def act(self):
        if self.fullness < 0:
            del self.house.family[self.house.family.index(self)]
            self.house.results = House().results
            cprint('Кот {} умер с голода'.format(self.name), 'red', attrs=['reverse'])
            return
        if self.fullness < 10:
            self.eat()
            return
        dice = randint(1, 6)
        if dice in range(1, 2):
            self.eat()
        elif dice == 2:
            self.soil()
        else:
            self.sleep()
        self.house.results = 'Денег в доме {}, еды в доме {}, неубранность {} \nКошачьей еды в доме {}'.format(
            self.house.money, self.house.ref_food, self.house.dirt, self.house.cat_food)

    def eat(self):
        if self.house.cat_food >= 10:
            cprint('Кот {} покушал'.format(self.name), self.color)
            self.fullness += 20
            self.house.cat_food -= 10
        else:
            self.fullness -= 10
            cprint('Кот {} собрался покушать...'.format(self.name), self.color)
            cprint('Недостаточно кошачьей еды!', 'red', attrs=['reverse'])

    def sleep(self):
        self.fullness -= 10
        cprint('Кот {} спал целый день'.format(self.name), self.color)

    def soil(self):
        self.fullness -= 10
        self.house.dirt += 5
        cprint('Кот {} подрал обои'.format(self.name), self.color)

    def move_in(self):
        self.house.family.append(self)
        if hasattr(self.house, 'cat_food'):
            return
        else:
            setattr(self.house, 'cat_food', 30)
        self.house.pet = self.name

    def __str__(self):
        return 'Сытость {}'.format(self.fullness)

home = House()
hus = Husband('Сережа')
wife = Wife('Маша')
cat = Cat('Сосиска', home)
hus.move_in(home)
wife.move_in(home)
cat.move_in()

child = Child('Артур')
child.move_in(home)


# for member in home.family:
#     member.move_in(home)
# masha = Wife(name='Маша')


for day in range(1, 365):
    if not home.family:
        break
    cprint('================== День {} =================='.format(day), color='red')
    for member in home.family:
        member.act()
        cprint('{}'.format(member), member.color)
    cprint(home, 'cyan')




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

