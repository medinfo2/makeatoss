#!/usr/bin/env python
# -*- coding: utf-8 -*-

import memcache
import logging
import cPickle as pickle

from main import Game
from main import Player
from main import Rock, Scissors, Paper

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


def register(player):
    game_ = game()
    # print game_.__dict__
    game_.register(player)
    memcached.set('game', pickle.dumps(game_))


def clear():
    memcached.delete('game')
