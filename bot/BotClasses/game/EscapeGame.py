import random

from .map import map
from ..Keyboards import keyboard
from ..User import User


class EscapeGame:
    def __init__(self, chat_user: User):
        self.chat_user = chat_user
        self.map = map
        self.mob_list = []
        self.user = User('Гавкомышь', 1)
        self._set_user_pos()
        self.delta = {'x': 0, 'y': 0}
        self.generate_mob(5)
        print(self.mob_list)

    def game_over(self):
        print("game is over....")
        return self.user.balance

    def attack(self):
        if not self.mob_list:
            return False
        self.mob_to_attack = []
        for mob in self.mob_list:
            mob_x = mob.position['x']
            user_x = self.user.position['x']
            mob_y = mob.position['y']
            user_y = self.user.position['y']
            abs_x = abs(mob_x - user_x)
            abs_y = abs(mob_y - user_y)
            if (abs_x == 0 or abs_x == 1) and abs(abs_y == 0 or abs_y == 1):
                self.mob_to_attack.append(mob)
                print('mob in moblist ', mob_x, mob_y)
        print('ATTACK!!!', self.mob_to_attack)
        self._damage_mob()
        return True

    def _damage_mob(self):
        damage = self.user.attack
        for enemy in self.mob_to_attack:
            print('enemy:: ', enemy.health, enemy.position )
            if enemy.health > damage:
                enemy.health = enemy.health - damage
            else:
                self._kill_mob(enemy)

    def _kill_mob(self, mob):
        for enemy in self.mob_to_attack:
            mob_x = mob.position['x']
            mob_y = mob.position['y']
            self.map[mob_y][mob_x][0] = '💀'
            print(enemy.position, mob.position)
            if enemy.position == mob.position:
                self.mob_to_attack.remove(enemy)
                for mob_ in self.mob_list:
                    if mob_.position == enemy.position:
                        self.mob_list.remove(mob_)
                        print('removing', enemy.position)
                        self.user.balance += mob_.reward

    def generate_mob(self, count):
        for _ in range(0, count):
            x = random.randint(1, 7)
            y = random.randint(1, 7)
            while x == 4 or x == 5:
                x = random.randint(1, 7)
                y = random.randint(1, 7)
            pos = {'x': x, 'y': y}
            mob = Mob(3 + random.randint(1,10), 20, pos)
            self.mob_list.append(mob)
            self.map[y][x][0] = '👹'

    def _set_user_pos(self):
        x = self.user.position['x']
        y = self.user.position['y']
        self.map[y][x][0] = '🦹🏿‍♂'

    def get_map(self, game_over=False):
        if game_over:
            return
        return keyboard('game_map', self.chat_user, buttons=self.map).get_inline_keyboard()

    def move(self, direction: str):
        self.delta['x'] = self.user.position['x']
        self.delta['y'] = self.user.position['y']
        if direction == 'up':
            self.delta['y'] = self.user.position['y'] - 1 if self.delta['y'] != 0 else 0
        elif direction == 'down':
            self.delta['y'] = self.user.position['y'] + 1 if self.delta['y'] != 10 else 10
        elif direction == 'right':
            self.delta['x'] = self.user.position['x'] + 1 if self.delta['x'] != 7 else 7
        elif direction == 'left':
            self.delta['x'] = self.user.position['x'] - 1 if self.delta['x'] != 0 else 0
        self.map[self.user.position['y']][self.user.position['x']][0] = '⬜'
        self.user.position['x'] = self.delta['x']
        self.user.position['y'] = self.delta['y']
        self._set_user_pos()


class User:
    def __init__(self, name: str, category: int):
        self.name = name
        self.category = category
        self.position = {'x': 4, 'y': 5}
        self.balance = 0
        if self.category == 1:
            self.class_name = 'Студент'
            self.health = 10
            self.armor = 5
            self.attack = 4
        elif self.category == 2:
            self.class_name = 'Профессор'
            self.health = 12
            self.armor = 3
            self.attack = 3


class Mob:
    def __init__(self, health: int, reward: int, position: dict):
        self.health = health
        self.reward = reward
        self.position = position
