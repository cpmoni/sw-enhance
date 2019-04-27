import json

from monster import Monster
from rune import Rune, Grind, Gem
from constant_maps import *

class Summoner:
    def __init__(self,filename):
        self.data_file = filename
        print(f'Loading data from {filename}')
        
        with open(filename) as fin:
            data = json.load(fin)
            
        self.mons = {}
        self.runes = {}
        self.grinds = []
        self.gems = []
        
        self.parse_mons(data['unit_list'])
        self.parse_runes(data['runes'])
        self.parse_grinds(data['rune_craft_item_list'])
        
        self.grinds.sort(key=lambda x: (x.set, x.stat, -x.grade))
        
    def parse_mons(self,mon_list):
        for mon in mon_list:
            m = Monster(mon)
            self.mons[m.id] = m
            self.parse_runes(mon['runes'])
                
    def parse_grinds(self,rune_craft_list):
        for gg in rune_craft_list:
            if gg['craft_type'] == 1 or gg['craft_type'] == 3: self.gems.append(Gem(gg['craft_type_id'],gg['sell_value']))
            else: self.grinds.append(Grind(gg['craft_type_id'],gg['sell_value']))
            
    def parse_runes(self,rune_list):
        for rune in rune_list:
            r = Rune(rune)
            self.runes[r.id] = r
        
    def find_rune(self,rune_id):
        location = self.runes[rune_id].location
        if location != 0:
            location = self.mons[location]
        else: location = 'Inventory'
        return location
        
    def print_runes(self):
        for rune_id in self.runes:
            print(self.runes[rune_id].str_with_subs())
            print(self.find_rune(rune_id))
            print()
            
    def analyze_reapps(self,n=10):
        poss = []
        for rune_id in self.runes:
            s = self.runes[rune_id].reapp 
            if s > 0:
               poss.append((rune_id,s)) 
               
        poss.sort(key=lambda x: x[1],reverse=True)
        for i in range(n):
            print('Option',i+1)
            
            rune_id, s = poss[i]
            print(self.runes[rune_id].str_with_subs())
            print('On {}, Score {}'.format(self.find_rune(rune_id),s))
            
    def analyze_grinds(self):
        counts = {}
        poss = {}
        for grind in self.grinds:
            k = (grind.set,grind.stat,grind.grade)
            if k in counts: counts[k] += 1
            else:
                counts[k] = 1
                poss[k] = []
                
                for rune_id in self.runes:
                    r = self.runes[rune_id]
                    if r.level < 12 or r.reapp > .5: continue
                    if r.set != grind.set and grind.set != 99: continue
                    for sub in r.subs:
                        if sub['stat'] == grind.stat:
                            if sub['grind'] < grind.get_max():
                                poss[k].append((r,grind.get_max()-sub['grind'],grind.stat))
                                
        for k in poss:
            sset, stat, grade = k
            s = 'Grind'
            c = counts[k]
            if c > 1: s+= 's'
            print('{} {} {} {} {}'.format(c,rune['quality'][grade],rune['sets'][sset],rune['effectTypes'][stat],s))
            runes = poss[k]
            runes.sort(key=lambda x: (-x[1],-(x[0].set),-(x[0].location)))
            for x in runes:
                print(f"{x[0]} at {self.find_rune(x[0].id)} can improve {x[1]} {rune['effectTypes'][x[2]]}")
            print()
                            
            