from summoner import Summoner
import os

if __name__ == '__main__':
    airking = Summoner(os.path.expanduser('~/Desktop/Summoners War Exporter Files/Airking77-23182654.json'))
    airking.analyze_grinds()
    #airking.print_runes()
    airking.analyze_reapps(10)