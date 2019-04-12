#!/usr/bin/env python3
# -*- coding:utf-8 -*-


'''
Minesweeper: Reset Edition
'''


__author__ = 'guanruiqing'


import random, hashlib, json, datetime, re, copy

from ORM import Database_Reset, Database_add, Database_delete, Database_update, Database_select


class Minesweeper(object):
    '''
    game body

    Attributes:
        name: user name.
        password: user password.
        login: login status.
    '''
    def __init__(self):
        self.name = 'Tourist'
        self.__password = '123456'
        self.__login = False

    def User_Create(self, name, password):
        salt_value = str(random.random())
        hash_password = hashlib.md5((password + salt_value).encode('utf-8')).hexdigest()
        status = Database_add(name, salt_value, hash_password)
        return status

    def User_Login(self, name, password):
        if not name and not password:
            name, password = 'Tourist', '123456'
        user = Database_select(name)
        if user == False:
            return 'name error'
        elif user.hash_password == hashlib.md5((password+user.salt_value).encode('utf-8')).hexdigest():
            self.name = user.name
            self.__password = user.hash_password
            self.__login = True
            if self.name == 'root':
                self.Database_Reset = Database_Reset()
            return True
        else:
            return 'password error'

    def User_Save(self, user):
        if self.__login:
            user.save_time = datetime.datetime.now()
            user_cache = copy.deepcopy(user)
            user_cache.map_setting = json.dumps(user.map_setting)
            user_cache.system_map = json.dumps(user.system_map)
            user_cache.player_map = json.dumps(user.player_map)
            save_status = Database_update(user_cache)
            return save_status
        else:
            return 'no login'

    def User_Reload(self):
        if self.__login:
            user = Database_select(self.name)
            user.map_setting = json.loads(user.map_setting)
            user.system_map = json.loads(user.system_map)
            user.player_map = json.loads(user.player_map)
            return user
        else:
            return 'no login'

    def User_Exit(self, user):
        self.name = 'Tourist'
        self.__password = '123456'
        self.__login = False
        return True

    def Map_Set(self, level, *, length=1, width=1, bomb=1):
        if level == 1:
            map_setting = {'level':1, 'length':9, 'width':9, 'bomb':10}
        elif level == 2:
            map_setting = {'level':2, 'length':16, 'width':16, 'bomb':40}
        elif level == 3:
            map_setting = {'level':3, 'length':30, 'width':16, 'bomb':99}
        elif level == 4:
            map_setting = {'level':4, 'length':length, 'width':width, 'bomb':bomb}
        return map_setting

    def Map_Generate(self, map_setting):
        create_time = datetime.datetime.now()
        length, width, bomb = map_setting['length'], map_setting['width'], map_setting['bomb']
        system_map = {}
        player_map = {}
        for i in (str(i1)+'x'+str(i2) for i1 in range(1,length+1) for i2 in range(1,width+1)):
            system_map[i] = 0
            player_map[i] = 'N'
        bomb_map = set()
        while len(bomb_map) < bomb:
            i = str(random.randint(1,length))+'x'+str(random.randint(1,width))
            bomb_map.add(i)
            system_map[i] = 'B'
        for i in bomb_map:
            number = surround(i)
            for i in number:
                if i in system_map and system_map[i] != 'B':
                    system_map[i] = system_map[i] + 1
        return create_time, system_map, player_map

    def Map_Checking(self, system_map, player_map, send_value):
        if send_value[0] == 'X':
            if player_map[send_value[1]] == 'X':
                player_map[send_value[1]] = 'N'
            elif player_map[send_value[1]] == 'N':
                player_map[send_value[1]] = 'X'
            return system_map, player_map, True
        elif send_value[0] == '':
            if player_map[send_value[1]] == 'X':
                return system_map, player_map, True
            player_map[send_value[1]] = system_map[send_value[1]]
            if player_map[send_value[1]] == 'B':
                return system_map, player_map, False
            elif player_map[send_value[1]] == 0:
                display_key = set()
                display_key.add(send_value[1])
                display_key_cache = set()
                while display_key != display_key_cache:
                    display_key_cache = copy.copy(display_key)
                    for i in display_key_cache:
                        if system_map[i] == 0:
                            number = surround(i)
                            for i in number:
                                if i in system_map:
                                    display_key.add(i)
                for i in display_key:
                    player_map[i] = system_map[i]
                return system_map, player_map, True
            elif 0 < player_map[send_value[1]] < 9:
                return system_map, player_map, True

    def Map_Print(self, user):
        print('-'*30)
        print('Minesweeper: Reset Edition')
        print(user.map_setting)
        bomb = user.map_setting['bomb']
        for i in user.player_map.values():
            if i == 'X':
                bomb = bomb - 1
        print('user:%s    level:%d    step_count:%d    bomb:%d    save_time:%s'%(
                user.name, user.map_setting['level'], user.step_count, bomb, user.save_time))
        long2 = user.map_setting['width']
        long1 = user.map_setting['length']
        for i2 in range(long2, -1, -1):
            print(' ' * (len(str(long2)) - len(str(i2))) + str(i2), end = '')
            for i1 in range(1, long1+1):
                if i2 != 0:
                    #print(' ' * (len(str(long1)) - 1) + str(user.player_map[str(i1) + 'x' + str(i2)]), end = '')
                    print(' ' * (len(str(long1))) + str(user.player_map[str(i1) + 'x' + str(i2)]), end = '')
                else:
                    #print(str(i1) + ' ' * (len(str(long1)) - len(str(i1))), end = '')
                    print(' ' * (len(str(long1)) - len(str(i1)) + 1) + str(i1), end = '')
            print()
        print('-'*30)

    def Map_Send(self, player_map, input_value):
        input_value = re.split('[x,.; ]+',input_value)
        if len(input_value) == 2: input_value.insert(0, '')

        if len(input_value) != 3: return False
        if input_value[0] != '' and input_value[0] != 'X': return False
        if input_value[1]+'x'+input_value[2] not in player_map: return False

        send_value = (input_value[0],input_value[1]+'x'+input_value[2])
        return send_value


def surround(map_key):
    x, y = [int(i) for i in re.split('x', map_key)]
    number = (str(x-1)+'x'+str(y+1), str(x)+'x'+str(y+1), str(x+1)+'x'+str(y+1),
              str(x-1)+'x'+str(y),                        str(x+1)+'x'+str(y),
              str(x-1)+'x'+str(y-1), str(x)+'x'+str(y-1), str(x+1)+'x'+str(y-1)
             )
    return number


def game_help():
    print('-'*30)
    print('''
          本程序一共3层主界面，使用唯一选项进入(返回)下层(上层)界面
          在输入界面直接输入数字代号即可
            0.help    1.create    2.login    3.exit
                0.help -- 查看帮助
                1.create -- 创建用户，重复创建会导致失败
                2.login -- 登录用户，如果不输入信息，则默认登录游客账户，登录后将进入第2层界面
                3.exit -- 退出本程序

            0.help    1.save    2.reload    3.exit
                0.help -- 查看帮助
                1.save -- 保存用户信息，您必须读取用户信息后才能保存
                2.reload -- 读取用户信息，读取后将进入第3层界面
                3.exit -- 退出登录状态，返回上一层

            0.help    1.generate    2.send    3.exit
                0.help -- 查看帮助
                1.generate -- 生成地图，选择后将进入难度选择界面
                    1.Simple    2.Ordinary    3.Difficult    4.customize
                2.send -- 进入地图循环，输入1x1选择位置，输入Xx1x1标记位置，其中x可以使用'x,.; '替代，输入错误不会造成影响，输入exit退出
                3.exit -- 退出游戏主题，返回上一层
          ''')
    print('-'*30)


if __name__ == '__main__':

    import logging

    logging.basicConfig(format = '%(asctime)s %(levelname)s %(message)s', filename = 'user.log', level = logging.DEBUG)
    logging.info('Game Start')

    body = Minesweeper()

    user = False
    player_status = False
    body_status = True
    while body_status:
        while not user:
            print('-'*30)
            print('Please login, if you have a user.')
            print('if you want to log in as a visitor, please choose not to enter the user after login.')
            print('menu:    0.help    1.create    2.login    3.exit')
            print('-'*30)
            menu = input('Please select: ')
            if menu == '0':
                game_help()
                logging.info('%s View help', 'Tourist')
            elif menu == '1':
                name = input('name: ')
                password = input('password: ')
                if body.User_Create(name, password):
                    print('success')
                    logging.info('%s create user "%s" success', body.name, name)
                else:
                    print('failure')
                    logging.info('%s create user "%s" failure', body.name, name)
            elif menu == '2':
                name = input('name: ')
                password = input('password: ')
                login_status = body.User_Login(name, password)
                if login_status == 'name error' or login_status == 'password error':
                    print('failure: %s'%login_status)
                    logging.info('%s login user "%s" failure:%s', body.name, name, login_status)
                else:
                    print('success')
                    logging.info('%s login user "%s" success', body.name, name)
                    user_status = True
                    if name == 'root':
                        while True:
                            reset_status = input('Do you want to reset the database?Y/N: ')
                            if reset_status == 'Y' or reset_status == 'y':
                                Database_Reset
                                print('ok')
                                logging.info('%s reset database of %s', body.name, reset_status)
                                break
                            elif reset_status == 'N' or reset_status == 'n':
                                logging.info('%s reset database of %s', body.name, reset_status)
                                break
                    break
            elif menu == '3':
                    body_status = False
                    user_status = False
                    logging.info('%s exit game', 'Tourist')
                    break
            else:
                print('Please enter restart')
        
        while user_status:
            print('-'*30)
            print('menu:    0.help    1.save    2.reload    3.exit')
            print('-'*30)
            menu = input('Please select: ')
            if menu == '0':
                game_help()
                logging.info('%s View help', body.name)
            elif menu == '1':
                if user:
                    save_status = body.User_Save(user)
                    print(save_status)
                    logging.info('%s save success:%s', body.name, save_status)
                else:
                    print('failure')
                    logging.info('%s save failure', body.name)
            elif menu == '2':
                user = body.User_Reload()
                user_status = False
                player_status = True
                logging.info('%s reload user', body.name)
            elif menu == '3':
                if user:
                    body.User_Exit(user)
                user = False
                user_status = False
                player_status = False
                logging.info('%s exit user', body.name)
            else:
                print('Please enter restart')

        while player_status:
            print('-'*30)
            print('menu:    0.help    1.generate    2.send    3.exit')
            print('-'*30)
            menu = input('Please select: ')
            if menu == '0':
                game_help()
                logging.info('%s View help', body.name)
            elif menu == '1':
                print('menu:    1.Simple    2.Ordinary    3.Difficult    4.customize')
                level = input('Please select: ')
                if level == '1':
                    user.map_setting = body.Map_Set(1)
                    logging.info('%s set map level = %s', body.name, level)
                elif level == '2':
                    user.map_setting = body.Map_Set(2)
                    logging.info('%s set map level = %s', body.name, level)
                elif level == '3':
                    user.map_setting = body.Map_Set(3)
                    logging.info('%s set map level = %s', body.name, level)
                elif level == '4':
                    while True:
                        try:
                            length = int(input('length: '))
                            width = int(input('width: '))
                            bomb = int(input('bomb: '))
                        except ValueError:
                            print('!!!input error!!!')
                        else:
                            if length * width >= bomb:
                                break
                            else:
                                print('!!!input error!!!')
                    user.map_setting = body.Map_Set(4, length = length, width = width, bomb = bomb)
                    logging.info('%s set map level = %s', body.name, level)
                else:
                    print('!!!input error!!!')
                    continue
                user.create_time, user.system_map, user.player_map = body.Map_Generate(user.map_setting)
                user.step_count = 0
                logging.info('%s generate map level = %s', body.name, level)
            elif menu == '2':
                if user.player_map:
                    logging.info('%s start send', body.name)
                    while True:
                        body.Map_Print(user)
                        input_value = input('send: ')
                        if input_value == 'exit':
                            logging.info('%s exit send', body.name)
                            break
                        send_value = body.Map_Send(user.player_map, input_value)
                        logging.info('%s send %s', body.name, send_value)
                        if send_value:
                            user.step_count = user.step_count + 1
                            print(send_value)
                            user.system_map, user.player_map, map_status = body.Map_Checking(user.system_map, user.player_map,send_value)
                            if not map_status:
                                body.Map_Print(user)
                                print('!!!game over!!!')
                                user.system_map = ''
                                user.player_map = ''
                                logging.info('%s send bomn, map over', body.name)
                                break
                            cache = 0
                            for i in user.player_map.values():
                                if i == 'N':
                                    cache = cache + 1
                            if cache == user.map_setting['bomb']:
                                body.Map_Print(user)
                                print('!!!You Win!!!')
                                user.system_map = ''
                                user.player_map = ''
                                logging.info('%s send Win, map over', body.name)
                                break
                        else:
                            print('!!!input error!!!')
                else:
                    print('!!!not have map!!!')
            elif menu == '3':
                player_status = False
                user_status = True
                logging.info('%s exit map', body.name)

    logging.info('Game Over')
