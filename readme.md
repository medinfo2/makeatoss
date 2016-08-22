# はじめに

このプロジェクトはじゃんけんゲームを行うプレーヤプログラムを簡単に行うAPIを提供します。

# インストール

pipでインストールしてください。

```
$ pip install git+https://github.com/medinfo2/makeatoss.git
```

# アンインストール

pipでアンインストールしてください。

```
$ pip uninstall makeatoss
```

# 使い方

各スクリプトで使う札を決定するduel関数を実装し、makeatoss.register関数に登録してください。
下記に２つの異なる実装をしたPlayerを登録し、対戦をシミュレートする３つのスクリプトを示します。

```python
import makeatoss
from makeatoss import Player
import logging
reload(logging)
logging.basicConfig(level=logging.DEBUG)


def duel(status, opponent, history):
    return status.cards[0]

makeatoss.clear()
makeatoss.register('team1', duel)
```

```python
import makeatoss
from makeatoss import Player
import logging
reload(logging)
logging.basicConfig(level=logging.DEBUG)

def duel(status, opponent, history):
    return status.cards[-1]

makeatoss.register('team2', duel)
```

```python
game = makeatoss.game()

print 'users: ', game.players

game.initialize()
print game
while game.simulate(): print game
```
