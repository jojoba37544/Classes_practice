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





class House:
    ref_capacity = 360
    pet_food_capacity = 180

    class LifeResults:
        food = 0
        fur_coat = 0
        money = 0
        cats = 0
        cats_died = 0

        def __str__(self):
            return 'Всего еды куплено {}\nВсего шуб куплено {}\nДенег заработано {}\nКотов было {}' \
                   '\nКотов умерло {}'.format(self.food, self.fur_coat, self.money, self.cats, self.cats_died)

    def __init__(self, days, quantity_food, quantity_money):
        self.money = 100
        self.ref_food = 50
        self.dirt = 0
        self.days = days
        self.family = []
        self.cat_list = []
        self.food_event_quan = quantity_food
        self.money_event_quan = quantity_money
        self.pet = None
        self.results = '{} денег в доме, еды в доме {}, грязь {}'.format(self.money, self.ref_food, self.dirt)
        self.day_counter = 0
        self.event = 0
        self.dice_food = randint(1 + self.event, (self.days // self.food_event_quan) + self.event)
        self.dice_money = randint(1 + self.event, (self.days // self.money_event_quan) + self.event)

    def unexpected_event(self):
        if self.day_counter == self.dice_food:
            self.event += self.days // self.food_event_quan
            self.ref_food //= 2
            cprint('Из холодильника пропала половина еды!', 'grey', attrs=['reverse'])
        if self.day_counter == self.dice_money:
            self.event += self.days // self.money_event_quan
            self.money //= 2
            cprint('Пропали деньги!', 'green', attrs=['reverse'])
        else:
            pass

    def __str__(self):
        self.dirt += 5
        self.day_counter += 1
        self.unexpected_event()
        if any(isinstance(fam_member, Cat) for fam_member in self.family):
            return 'Денег в доме {}, еды в доме {}, грязь {}\nКошачьей еды в доме {}' \
                .format(self.money, self.ref_food, self.dirt, self.cat_food)
        else:
            return '{} денег в доме, еды в доме {}, грязь {}'.format(self.money, self.ref_food, self.dirt)

    def __len__(self):
        return len(self.__str__())


class Human:
    happiness_maximum = 100

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
        self.happiness += 5 if self.happiness <= 95 else self.happiness_maximum - self.happiness
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
        self.pet = choice(self.house.cat_list).name if self.house.cat_list else None
        # results = self.house.results
        # setattr(self.house, self.house.results, results)
        return 'Сытость {}, уровень счастья {}'.format(self.fullness, self.happiness)

    def __len__(self):
        return len(self.__str__())


class Husband(Human):
    def __init__(self, name, salary):
        super().__init__(name=name)
        self.color = 'blue'
        self.salary = salary

    def act(self):
        if super().act() is False:
            return
        if self.fullness <= 10:
            self.eat()
            return
        if self.house.pet is not None:
            if self.house.cat_food < 20 * int(len(self.house.cat_list)):
                self.work()
                return
        if self.house.money < self.salary:
            self.work()
            return
        dice = randint(1, 6)
        if dice in range(1, 2):
            self.work()
        elif dice == 4:
            self.eat()
        elif dice == 5:
            if self.house.pet is not None:
                self.pet_interaction()
            else:
                self.gaming()
        else:
            self.gaming()

    def work(self):
        cprint('{} весь день работал'.format(self.name), self.color)
        self.house.money += self.salary
        self.house.LifeResults.money += self.salary

    def gaming(self):
        dice = randint(1, 6)
        if dice == 1:
            self.happiness += 20 if self.happiness <= 80 else self.happiness_maximum - self.happiness
            cprint('{} весь день бездельничал'.format(self.name), self.color)
        elif dice == 2:
            self.happiness += 20 if self.happiness <= 80 else self.happiness_maximum - self.happiness
            cprint('{} весь день смотрел телевизор'.format(self.name), self.color)
        else:
            self.happiness += 20 if self.happiness <= 80 else self.happiness_maximum - self.happiness
            cprint('{} весь день играл в доту'.format(self.name), self.color)


class Wife(Human):

    def __init__(self, name):
        super().__init__(name=name)
        self.color = 'magenta'

    def act(self):
        if super().act() is False:
            return
        if self.fullness <= 20:
            if self.house.ref_food < 0:
                self.shopping()
                return
            else:
                self.eat()
                return
        if self.happiness < 20:
            if self.house.money < 350:
                self.buy_fur_coat()
                return
            elif self.house.pet is not None:
                self.pet_interaction()
            else:
                cprint('{} несчастна и ничего не может на данный момент унять ее грусть'.format(self.name, self.color))
        if self.house.dirt >= 90:
            self.clean_house()
            return
        if self.house.ref_food < 20:
            self.shopping()
            return
        if any(isinstance(fam_member, Cat) for fam_member in self.house.family):
            if self.house.cat_food < 20 * int(len(self.house.cat_list)):
                self.cat_food_replenish()
                return
        dice = randint(1, 6)
        if dice == 1:
            self.buy_fur_coat()
        elif dice == 4:
            self.eat()
        elif dice == 5:
            if self.house.pet is not None:
                self.pet_interaction()
            else:
                cprint('{} бездельничала'.format(self.name), self.color)
        elif dice == 6:
            if self.house.ref_food < self.house.ref_capacity:
                self.shopping()
            else:
                self.free_time()
        else:
            self.free_time()

    def free_time(self):
        dice = randint(1, 3)
        if dice == 1:
            for fam_member in self.house.family:
                if fam_member.__class__.__name__ == 'Child':
                    cprint('{} нянчилась с {}'.format(self.name, fam_member.name), self.color)
                    return
        else:
            cprint('{} бездельничала'.format(self.name), self.color)

    def nagging(self):
        for fam_member in self.house.family:
            if fam_member.__class__.__name__ == 'Husband':
                self.happiness += 30 if self.happiness <= 70 else self.happiness_maximum - self.happiness
                fam_member.happiness -= 30
                cprint('{} капает на мозги {}'.format(self.name, fam_member.name), self.color)
            else:
                return False

    def cat_food_replenish(self):
        cprint('{} отправилась в магазине купить кошачьей еды'.format(self.name), self.color)
        remain = self.house.pet_food_capacity - self.house.cat_food
        if self.house.money < 100:
            cprint('Недостаточно денег!', 'red', attrs=['reverse'])
            return
        elif remain < 100:
            self.house.money -= remain
            self.house.cat_food += remain
        else:
            self.house.cat_food += 100
            self.house.money -= 100

    def shopping(self):
        cprint('{} отправилась в магазин купить еды'.format(self.name), self.color)
        remain = self.house.ref_capacity - self.house.ref_food
        if self.house.money < 180:
            cprint('Недостаточно денег!', 'red', attrs=['reverse'])
            return
        elif remain < 180:
            self.house.money -= remain
            self.house.LifeResults.food += remain
            self.house.ref_food += remain
        else:
            self.house.ref_food += 180
            self.house.LifeResults.food += 180
            self.house.money -= 180
        cprint('{} купила еды'.format(self.name), self.color)

    def buy_fur_coat(self):
        if self.house.money < 350:
            cprint('{} хотела купить шубу'.format(self.name), self.color)
            cprint('Недостаточно денег!', 'red', attrs=['reverse'])
            return
        self.house.money -= 350
        self.house.LifeResults.fur_coat += 1
        self.happiness += 60 if self.happiness <= 40 else self.happiness_maximum - self.happiness
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
        if not any(isinstance(fam_member, Human) for fam_member in self.house.family):
            cprint('{} ОСТАЛСЯ ОДИН!, НЕКОМУ ЕГО КОРМИТЬ!'.format(self.name))
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
        if self.house.ref_food >= 10:
            self.fullness += 30
            self.house.ref_food -= 10
            if fam_member.__class__.__name__ == 'Husband':
                cprint('{} покормил {}а'.format(fam_member.name, self.name), self.color)
            elif fam_member.__class__.__name__ == 'Wife':
                cprint('{} покормила {}а'.format(fam_member.name, self.name), self.color)
        else:
            cprint('{} собирается покормить {}...'.format(fam_member.name, self.name), self.color)
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
            del self.house.cat_list[self.house.cat_list.index(self)]
            self.house.LifeResults.cats_died += 1
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
        self.house.cat_list.append(self)
        self.house.LifeResults.cats += 1
        if hasattr(self.house, 'cat_food'):
            return
        else:
            setattr(self.house, 'cat_food', 30)

    def __str__(self):
        return 'Сытость {}'.format(self.fullness)


# for member in home.family:
#     member.move_in(home)
# masha = Wife(name='Маша')

class Simulation:
    days = 366
    food = 3
    money = 3
    salary = 180

    def __init__(self, days=days, food=food, money=money, salary=salary, cats=0):
        self.cat_names = ['Сосиска', 'Сарделька', 'Колбаска', 'Сигизмунд', 'Козел', 'Шнур', 'Семен', 'Петя', 'Авгуша',
                          'Помидорка', 'Убийца', 'Степа', 'Бася', ]
        self.home = House(days, food, money)
        self.salary = salary
        self.hus = Husband('Сережа', self.salary)
        self.wife = Wife('Маша')
        self.hus.move_in(self.home)
        self.wife.move_in(self.home)
        self.child = Child('Артур')
        self.child.move_in(self.home)
        self.days = 1
        self.results = 0
        for cat in range(cats):
            some_cat = Cat(choice(self.cat_names), self.home)
            some_cat.move_in()

        for day in range(1, days):
            self.days += 1
            if not self.home.family:
                break
            cprint('================== День {} =================='.format(day), color='red')
            for member in self.home.family:
                member.act()
                cprint('{}'.format(member), member.color)
            cprint(self.home, 'cyan')
        cprint(self.home.LifeResults(), 'red')


    def __str__(self):
        return

    def max_cats(self, salary, cats):
        self.__setattr__('salary', salary)
        cats = cats
        Simulation()
        if self.days == 365:
            if self.home.cat_list:
                print(cats)
            else:
                print('dead')



life = Simulation(366, 3, 3, 180, 3)
life.max_cats(180, 2)

# for food_incidents in range(6):
#     for money_incidents in range(6):
#         life = Simulation(366, food_incidents, money_incidents, 2)
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
