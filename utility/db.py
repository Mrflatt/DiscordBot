'''import sqlite3

db = sqlite3.connect('ok')
cr = db.cursor()

# cr.execute("""CREATE TABLE IF NOT EXISTS guilds(guild_id INTEGER PRIMARY KEY, guild_name TEXT DEFAULT NULL, prefix TEXT DEFAULT '$', language TEXT DEFAULT 'en')""")
#cr.execute(
#     "CREATE TABLE IF NOT EXISTS twitter(channel_id INTEGER PRIMARY KEY,guild_name TEXT DEFAULT NULL, channels CHARSET(20) NULL)")
#cr.execute(
#     "CREATE TABLE IF NOT EXISTS blacklist(user_id INTEGER PRIMARY KEY, user_name INTEGER DEFAULT NULL, blacklist BLOB DEFAULT false)"
# )
# cr.execute("CREATE TABLE IF NOT EXISTS cooldown(user_id INTEGER PRIMARY KEY)")


def get_cooldown():
    user = cr.execute("SELECT user_id FROM cooldown")
    all_user = user.fetchall()
    list_users = []
    for i in all_user:
        list_users.append(i[0])
    return list_users


def set_log(ctx, channel):
    log_channel = cr.execute("UPDATE log SET channel_id = ? WHEN guild_id = ?", (channel.id, ctx.guild.id))
    return log_channel.fetchone()[0]


def get_log(guild):
    log_channel = cr.execute("SELECT channel_id FROM log WERE guild_id = ?", (guild.id,))
    return log_channel.fetchone()


def get_lang(ctx):
    lang = cr.execute("SELECT language FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    return lang.fetchone()[0]


def get_prefix(ctx):
    prefix = cr.execute("SELECT prefix FROM guilds WHERE guild_id = ?", ctx.guild.id)
    return prefix.fetchone()[0]


def get_blacklist(id):
    i = cr.execute("SELECT ? FROM blacklist", (id,))
    return i


def add_blacklist(user):
    cr.execute("UPDATE blacklist SET blacklist = ? WERE user_id = ?", (True, user.id))
    commit()


def remove_blacklist(user):
    cr.execute("UPDATE blacklist SET blacklist = ? WERE user_id = ?", (False, user.id))
    commit()


def commit():
    db.commit()'''
