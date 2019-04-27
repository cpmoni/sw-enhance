from constant_maps import *
import math
from extract_digit import extract_digit

class Rune:
    def __init__(self,rj):
        self.id = rj['rune_id']
        self.location = rj['occupied_id']
        self.slot = rj['slot_no']
        self.stars = rj['class']
        self.quality = rj['rank']
        self.set = rj['set_id']
        self.level = rj['upgrade_curr']
        self.sell_value = rj['sell_value']
        
        self.main_stat = rj['pri_eff'][0]
        self.main_value = rj['pri_eff'][1]
        
        self.innate_stat = rj['prefix_eff'][0]
        self.innate_value = rj['prefix_eff'][1]
        self.extra = rj['extra']
        
        self.subs = []
        for subj in rj['sec_eff']:
            sub = {}
            sub['stat'] = subj[0]
            sub['value'] = subj[1]
            sub['enchant'] = bool(subj[2])
            sub['grind'] = subj[3]
            self.subs.append(sub)
            
        self.calc_efficiency()
        
        #print(f'Added {self}')
        
    def calc_efficiency(self,toFixed = 2):
        ratio = 0
        
        #main stat
        ratio += rune['mainstat'][self.main_stat]['max'][self.stars] / rune['mainstat'][self.main_stat]['max'][6]

        #sub stats
        for sub in self.subs:
            ratio += (sub['value'] + sub['grind']) / rune['substat'][sub['stat']]['max'][6]

        #innate stat
        if self.innate_value > 0: 
          ratio += self.innate_value / rune['substat'][self.innate_stat]['max'][6];
        
        efficiency = (ratio / 2.8) * 100;
        current = round(((ratio / 2.8) * 100),toFixed) 
        maxe = round((efficiency + ((max(math.ceil((12 - self.level) / 3.0), 0) * 0.2) / 2.8) * 100),2)
        
        self.efficiency = {'current': current, 'max': maxe}
        
    def __str__(self):
        #return '{} Star {} {} Slot {} Rune'.format(self.stars,rune['sets'][self.set],rune['effectTypes'][self.main_stat],self.slot)
        return '{} Slot {}'.format(rune['sets'][self.set],self.slot)

def get_stats(craft):
    sset = extract_digit(craft,0,2,n=6)
    stat = extract_digit(craft,2,2,n=6)
    grade = extract_digit(craft,5,n=6)
    
    return sset, stat, grade

class Grind:
    def __init__(self,craft,sell_value):
        self.sell_value = sell_value
        self.set, self.stat, self.grade = get_stats(craft)
        
        #print(f'Added {self}')
        
    def __str__(self):
        return '{} {} {} Grind'.format(rune['quality'][self.grade],rune['sets'][self.set],rune['effectTypes'][self.stat])
        
class Gem:
    def __init__(self,craft,sell_value):
        self.sell_value = sell_value
        self.set, self.stat, self.grade = get_stats(craft)
        
        #print(f'Added {self}')
        
    def __str__(self):
        return '{} {} {} Gem'.format(rune['quality'][self.grade],rune['sets'][self.set],rune['effectTypes'][self.stat])
                