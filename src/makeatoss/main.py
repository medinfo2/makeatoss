#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import random
from copy import deepcopy
import memcache

class Card(object):
    '''
    じゃんけんカードの親クラス。カードの優劣で比較演算子を動かす定義を記述
    '''
    def __init__(self, superior, inferior):
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


class Rock(Card):
    '''じゃんけんグー'''
    def __init__(self):
        Card.__init__(self, Paper, Scissors)

    def __str__(self):
        return 'rock'


class Scissors(Card):
    '''じゃんけんチョキ'''
    def __init__(self):
        Card.__init__(self, Rock, Paper)

    def __str__(self):
        return 'scissors'


class Paper(Card):
    '''じゃんけんパー'''
    def __init__(self):
        Card.__init__(self, Scissors, Rock)

    def __str__(self):
        return 'paper'


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
    def __init__(self):
        self.players = set()
        self.history = []
        self.player_status = {}

    def register(self, player):
        self.players.add(player)

    def initialize(self):
        for player in self.players:
            self.player_status[player] = PlayerStatus()

    def simulate(self):
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
    def __init__(self, name):
        self.name = name

    def duel(self, status, opponent, history):
        return random.choice(status.cards)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    rock = Rock()
    scissors = Scissors()
    paper = Paper()

    print "~~~ testing card behavior ~~~"

    print "rock > scissors:\t", rock > scissors
    print "rock < paper:\t\t", rock < paper
    print "rock == rock:\t\t", rock == rock

    print "scissors > paper:\t", scissors > paper
    print "scissors < rock:\t", scissors < rock
    print "scissors == scissors:\t", scissors == scissors

    print "paper > rock:\t\t", paper > rock
    print "paper < scissors:\t", paper < scissors
    print "paper == paper:\t\t", paper == paper

    print os.linesep * 2
    print "~~~ testing player status behavior ~~~"
    status = PlayerStatus()
    print "pop rock: ", status.pop(Rock)
    print "remains: ", status
    print "pop scissors: ", status.pop(Scissors)
    print "remains: ", status
    print "pop paper: ", status.pop(Paper)
    print "remains: ", status
    status.coins -= 1
    print "remove coin: ", status

    print os.linesep * 2
    print "~~~ game simulate ~~~"
    game = Game()
    game.register(Player('hoge'))
    game.register(Player('foo'))
    game.register(Player('bar'))
    game.initialize()
    print game

    print "wanna start game ? >",
    raw_input()

    while True:
        try:
            if not game.simulate():
                break
            print game
            raw_input()
        except KeyboardInterrupt, e:
            break

    print "all tasks completed..."
