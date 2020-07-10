from steamworks import STEAMWORKS
steamworks = STEAMWORKS()
steamworks.initialize()

my_steam_name = steamworks.Friends.GetPlayerName()

print(my_steam_name.decode('UTF-8'))
