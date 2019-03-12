
# Mike

[mike](https://github.com/emre/mike) is a Discord bot sends notifications to your discord handle if you get attacked in the @drugwars game. Currently, when somebody attacks you, you have *5-20* minutes of reaction times based on the army of the attacker.

### Installation
***

```
$ (sudo) pip install drugwars_mike
```

### Configuration and Running
***

`mike` uses `meeseeker` to stream custom json operations. If you don't have a `meeseker` yet, you need to install it.

Example command to run `meeseker` to have custom json channels:

***
```
MEESEEKER_PUBLISH_OP_CUSTOM_ID=true MEESEEKER_EXPIRE_KEYS=300 meeseeker sync
```
***

Environment parameters:

***
| Variable                   | Description                | Required |
|----------------------------|----------------------------|----------|
| MIKE_BOT_TOKEN             | Discord bot token          | True     |
| MIKE_BATTLE_LOG_CHANNEL_ID | Channel ID for battle logs | False    |
| MIKE_DB                    | Connection URI for DB      | True     |
| MIKE_REDIS_HOST            | Redis host                 | True     |
| MIKE_REDIS_PORT            | Redis port                 | True     |
***

***

You can run mike by typing:

```
$ MIKE_BOT_TOKEN=<token> MIKE_DB=sqlite:///mydatabase.db MIKE_REDIS_HOST=localhost MIKE_REDIS_PORT=6379 mike
```

### Repository and License

Repository is located at [github/emre/mike](https://github.com/emre/mike) and it's licensed under [MIT](https://github.com/emre/mike/blob/master/LICENSE).

### Disclaimer

Even though, mike works perfectly at the moment, there is no guarentee that it will notify you every time. Due to potential bugs or lags in the backend blockchain streaming, you may miss some notifications. However, I will be doing my best to keep it always working.

