#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import logging
import random
from copy import deepcopy
import marshal
import types


class Card(object):
    '''
    じゃんけんカードの親クラス。カードの優劣で比較演算子を動かす定義を記述
    '''
    def __init__(self, name, superior, inferior):
        self.name = name
        self.superior = superior
        self.inferior = inferior

    def __eq__(self, obj):
        return isinstance(obj, self.__class__)

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __gt__(self, obj):
        return isinstance(obj, self.inferior)

    def __ge__(self, obj):
        return not isinstance(obj, self.superior)

    def __lt__(self, obj):
        return isinstance(obj, self.superior)

    def __le__(self, obj):
        return not isinstance(obj, self.inferior)

    def __str__(self):
        return self.name


class Rock(Card):
    '''じゃんけんグー'''
    def __init__(self):
        Card.__init__(self, 'rock', Paper, Scissors)


class Scissors(Card):
    '''じゃんけんチョキ'''
    def __init__(self):
        Card.__init__(self, 'scissors', Rock, Paper)


class Paper(Card):
    '''じゃんけんパー'''
    def __init__(self):
        Card.__init__(self, 'paper', Scissors, Rock)


class PlayerStatus(object):
    '''
    じゃんけんゲームにおけるプレーヤの状態を格納するクラス
    '''
    def __init__(self):
        self.cards = [
            Rock(), Rock(), Rock(), Rock(),
            Scissors(), Scissors(), Scissors(), Scissors(),
            Paper(), Paper(), Paper(), Paper()
        ]
        self.coins = 4

    def pop(self, clazz):
        '''
        カードクラスを指定すると、持ち札から取り出す便利関数
        '''
        for card in self.cards:
            if isinstance(card, clazz): break
        self.cards.remove(card)
        return card

    def __str__(self):
        return '[%d] ' % self.coins + ', '.join([str(c) for c in self.cards])


class Game(object):
    '''
    ゲームを取り仕切るマネージャクラス
    '''
    def __init__(self):
        self.players = set()
        self.history = []
        self.player_status = {}

    def register(self, player):
        '''
        プレーヤを登録します。同じプレーヤは一つしか登録できません。
        '''
        self.players.add(player)

    def initialize(self):
        '''
        プレーヤの状態を初期化します。
        '''
        for player in self.players:
            self.player_status[player] = PlayerStatus()

    def simulate(self):
        '''
        プレーヤの組み合わせを決め、一回勝負を行い、結果を更新します。initializeをしていないと動きません。
        '''
        players = [
            player for player in self.players
            if self.player_status[player].cards and self.player_status[player].coins > 0
        ]
        if not players or len(players) < 2:
            logging.debug('no more matches enabled.')
            return False

        random.shuffle(players)
        for idx in range(len(self.player_status) / 2):
            player1 = players[idx * 2]
            player2 = players[idx * 2 + 1]

            p1card = player1.duel(self.player_status[player1], player2.name, self.history)
            self.player_status[player1].pop(p1card.__class__)
            p2card = player2.duel(self.player_status[player2], player1.name, self.history)
            self.player_status[player2].pop(p2card.__class__)
            self.history.append({
                player1.name: p1card,
                player2.name: p2card
            })

            logging.debug('{} [{}] vs {} [{}]'.format(player1, p1card, player2, p2card))
            if p1card > p2card:
                logging.debug('{} wins'.format(player1))
                self.player_status[player1].coins += 1
                self.player_status[player2].coins -= 1
            elif p2card > p1card:
                logging.debug('{} wins'.format(player2))
                self.player_status[player1].coins -= 1
                self.player_status[player2].coins += 1
            else:
                logging.debug('draw')

        return True

    def __str__(self):
        buf = []
        for player in self.players:
            buf.append('{}: {}'.format(player, self.player_status[player]))
        return os.linesep.join(buf)


class Player(object):
    '''
    プレーヤの基底クラスです。duelを上書きして、それぞれのプレーヤを作ります。
    '''
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def duel(self, status, opponent, history):
        '''
        手札を決める関数です。以下の引数を持ちます。デフォルトの実装は手札からランダムに出すというものです。

        status: 自分のstatusです。cardsとcoinsフィールドを持ちます。
        opponent: 対戦相手の名前です。historyの検索に使います。
        history: これまでの対戦履歴です。どの対戦者がどのカードを出したか履歴がわかります。
        '''
        return self.func(status, opponent, history)

    def __str__(self):
        return self.name

    def __getstate__(self):
        '''
        pickle時に呼ばれる関数の実装。関数のコードをシリアライズする
        '''
        return {
            'name': self.name,
            'func': marshal.dumps(self.func.func_code)
        }

    def __setstate__(self, state):
        '''
        unpickle時に呼ばれる関数の実装。関数のコードから機能をデシリアライズする
        '''
        code = marshal.loads(state['func'])
        func = types.FunctionType(code, globals())
        self.__dict__.update({
            'name': state['name'],
            'func': func
        })

    def __hash__(self):
        '''
        一致判定で使う関数の定義。
        '''
        return hash(self.name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    rock = Rock()
    scissors = Scissors()
    paper = Paper()

    print("~~~ testing card behavior ~~~")

    print("rock > scissors:\t", rock > scissors)
    print("rock < paper:\t\t", rock < paper)
    print("rock == rock:\t\t", rock == rock)

    print("scissors > paper:\t", scissors > paper)
    print("scissors < rock:\t", scissors < rock)
    print("scissors == scissors:\t", scissors == scissors)

    print("paper > rock:\t\t", paper > rock)
    print("paper < scissors:\t", paper < scissors)
    print("paper == paper:\t\t", paper == paper)

    print(os.linesep * 2)
    print("~~~ testing player status behavior ~~~")
    status = PlayerStatus()
    print("pop rock: ", status.pop(Rock))
    print("remains: ", status)
    print("pop scissors: ", status.pop(Scissors))
    print("remains: ", status)
    print("pop paper: ", status.pop(Paper))
    print("remains: ", status)
    status.coins -= 1
    print("remove coin: ", status)

    print(os.linesep * 2)
    print("~~~ game simulate ~~~")
    game = Game()
    game.register(Player('hoge', lambda status, op, history: random.choice(status.cards)))
    game.register(Player('foo', lambda status, op, history: random.choice(status.cards)))
    game.register(Player('bar', lambda status, op, history: random.choice(status.cards)))
    game.initialize()
    print(game)

    print("wanna start game ? >", end="")
    raw_input()

    while True:
        try:
            if not game.simulate():
                break
            print(game)
            raw_input()
        except KeyboardInterrupt:
            break

    print("all tasks completed...")
