#!/usr/bin/env python
# -*- coding: utf-8 -*-

import memcache
import logging
import pickle
import random

from makeatoss.main import Game
from makeatoss.main import Player
from makeatoss.main import Rock, Scissors, Paper

memcached = memcache.Client(["localhost"])


def game():
    game_expr = memcached.get('game')
    # print 'game: ', game_expr
    if not game_expr:
        logging.debug('no game found. gonna create')
        game = Game()
        memcached.set('game', pickle.dumps(game))
        return game
    else:
        return pickle.loads(game_expr)


def register(name, func):
    game_ = game()
    # print game_.__dict__
    player = Player(name, func)
    game_.register(player)
    memcached.set('game', pickle.dumps(game_))

def remove(name):
    game_ = game()
    if name in game_.players:
        del game_.players[name]
    memcached.set('game', pickle.dumps(game_))


def trial(player_list):
    game = Game()
    if len(player_list) > 1:
        for name, func in player_list:
            game.register(Player(name, func))
    else:
        game.register(Player(player_list[0][0], player_list[0][1]))
        game.register(Player(name, lambda x, y, z: random.choice(x.cards)))
        game.register(Player(name, lambda x, y, z: random.choice(x.cards)))

    while game.simulate(): print game

    print "all match completed"


def evaluate():
    pass

def clear():
    memcached.delete('game')


if __name__ == '__main__':
    main()
