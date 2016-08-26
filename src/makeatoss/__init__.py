#!/usr/bin/env python
# -*- coding: utf-8 -*-

import memcache
import logging
import pickle
import random
from pprint import pformat

try:
    from makeatoss.main import Game
    from makeatoss.main import Player
    from makeatoss.main import Rock, Scissors, Paper
except:
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
        game.register(Player('computer1', lambda x, y, z: random.choice(x.cards)))
        game.register(Player('computer2', lambda x, y, z: random.choice(x.cards)))

    game.initialize()
    while game.simulate(): print game

    print("all match completed")


def evaluate(epochs=100):
    game_ = game()
    sum_of_coins = {}
    for i in xrange(100):
        game_.initialize()
        while game_.simulate(): print game_
        for player, status in game_.player_status.items():
            if player.name in sum_of_coins:
                sum_of_coins[player.name] += status.coins
            else:
                sum_of_coins[player.name] = status.coins
    print pformat(sum_of_coins)
    return sum_of_coins


def clear():
    memcached.delete('game')


if __name__ == '__main__':
    def duel(status, opponent, history):
        return status.cards[0]

    trial([('sample', duel)])

    clear()

    register('sample', duel)
    register('computer1', lambda x, y, z: random.choice(x.cards))
    register('computer2', lambda x, y, z: random.choice(x.cards))

    evaluate()
