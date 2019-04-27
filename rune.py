from constant_maps import *
import math
from extract_digit import extract_digit

def get_set(sset):
    return rune['sets'][sset]
    
def get_stat(stat):
    return rune['effectTypes'][stat]
    
def get_grade(grade):
    return rune['quality'][grade]

class Rune:
    def __init__(self,rj):
        self.id = rj['rune_id']
        self.location = rj['occupied_id']
        self.slot = rj['slot_no']
        self.stars = rj['class']
        self.grade = rj['extra']
        self.set = rj['set_id']
        self.level = rj['upgrade_curr']
        self.sell_value = rj['sell_value']
        
        self.main_stat = rj['pri_eff'][0]
        self.main_value = rj['pri_eff'][1]
        
        self.innate_stat = rj['prefix_eff'][0]
        self.innate_value = rj['prefix_eff'][1]
        
        self.subs = []
        for subj in rj['sec_eff']:
            sub = {}
            sub['stat'] = subj[0]
            sub['value'] = subj[1]
            sub['enchant'] = bool(subj[2])
            sub['grind'] = subj[3]
            self.subs.append(sub)
            
        self.calc_efficiency()
        self.calc_reapp()
        
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
        
        self.efficiency = current
        
    def calc_reapp(self):
        self.reapp = 0.0
        
        scores = []
        w = []
        
        if self.slot in [2,4,6]: main_slot = 1
        else: main_slot = 0
        scores.append(main_slot)
        w.append(1)
        
        priority_sets = ['Violent', 'Swift', 'Despair', 'Will', 'Vampire', 'Fight', 'Revenge']
        if self.stars != 6 or self.level < 12: return
        if not (self.get_set() == 'Violent' and self.grade >= 4 and main_slot) and self.grade < 5: return
        if self.get_set() not in priority_sets and not main_slot: return
        
        bad_stats = ['HP+','ATK+','DEF+']
        good_stats = ['SPD','HP%','ACC']
        support_stats = ['RES']
        nuker_stats = ['ATK%','CR','CD']
        
        bad_rolls = 0
        good_rolls = 0
        support_rolls = 0
        nuker_rolls = 0
        def_rolls = 0
        
        for i in range(len(self.subs)):
            stat = self.get_sub_stat(i)
            rolls = self.guess_rolls(i)
            
            if stat in bad_stats: bad_rolls += rolls
            elif stat in good_stats: good_rolls += rolls
            elif stat in support_stats: support_rolls += rolls
            elif stat in nuker_stats: nuker_rolls += rolls
            elif stat == 'DEF%': def_rolls += rolls
            
        count_bad = bad_rolls
        if main_slot and self.get_main_stat() in nuker_stats: 
            count_bad += support_rolls
            if self.get_main_stat() in ['ATK%','CR']: count_bad += def_rolls
        elif main_slot and self.get_main_stat() in support_stats: count_bad += nuker_rolls
        if nuker_rolls > 2 and support_rolls > 2: count_bad += min(support_rolls,nuker_rolls)
        scores.append(count_bad/8.0)
        w.append(2.0)
        
        scores.append(1-self.efficiency/100.)
        w.append(1.0)
        
        if self.get_innate_stat() == 'SPD': spd_hidden = 0
        else: spd_hidden = 1
        scores.append(spd_hidden)
        w.append(.25)
        
        if self.get_set() in priority_sets: priority_set = 1
        else: priority_set = 0
        scores.append(priority_set)
        w.append(1)
        
        score = 0.0
        for i in range(len(scores)): score += scores[i]*w[i]
        score /= sum([abs(x) for x in w])
        
        self.reapp = score
        
    def get_set(self): return get_set(self.set)
    def get_main_stat(self): return get_stat(self.main_stat)
    def get_innate_stat(self): return get_stat(self.innate_stat)
    def get_sub_stat(self,i): 
        if i < len(self.subs): return get_stat(self.subs[i]['stat'])
        return '' 
    def guess_rolls(self,i):
        if i >= len(self.subs): return 0
        sub = self.subs[i] 
        m = rune['substat'][sub['stat']]['max'][self.stars]
        return math.ceil(sub['value']/m)
    def get_grade(self): return get_grade(self.grade)
    
    def str_with_subs(self):
        ans = '{} {}{} {} Slot {} {} Rune'.format(self.get_grade(),self.stars,'\u2605',self.get_set(),self.slot,self.get_main_stat())
        if self.innate_stat != 0:
            ans += '\n    Innate: {} {}'.format(self.innate_value,self.get_innate_stat())
        for i in range(len(self.subs)):
            sub = self.subs[i]
            if sub['enchant']: e = "(E)"
            else: e = ''
            ans += '\n    Sub {}: {} + {} = {} {} {}'.format(i+1,sub['value'],sub['grind'],sub['value']+sub['grind'],self.get_sub_stat(i),e)
        return ans    
            
        
    def __str__(self):
        #return '{} Star {} {} Slot {} Rune'.format(self.stars,rune['sets'][self.set],rune['effectTypes'][self.main_stat],self.slot)
        return '{} Slot {}'.format(self.get_set(),self.slot)

def get_stats(craft):
    sset = extract_digit(craft,0,2,n=6)
    stat = extract_digit(craft,2,2,n=6)
    grade = extract_digit(craft,5,n=6)
    
    return sset, stat, grade

class Grind:
    def __init__(self,craft,sell_value):
        self.sell_value = sell_value
        self.set, self.stat, self.grade = get_stats(craft)
        
    def get_grade(self): return get_grade(self.grade)
    def get_set(self): return get_set(self.set)
    def get_stat(self): return get_stat(self.stat) 
        
    def get_max(self):
        return grindstone[self.stat]['range'][self.grade]['max']    
        
    def __str__(self):
        return '{} {} {} Grind'.format(self.get_grade(),self.get_set(),self.get_stat())
        
class Gem:
    def __init__(self,craft,sell_value):
        self.sell_value = sell_value
        self.set, self.stat, self.grade = get_stats(craft)
        
    def get_grade(self): return get_grade(self.grade)
    def get_set(self): return get_set(self.set)
    def get_stat(self): return get_stat(self.stat)
        
        
    def get_max(self):
        return enchanted_gem[self.stat]['range'][self.grade]['max']
        
    def __str__(self):
        return '{} {} {} Gem'.format(self.get_grade(),self.get_set(),self.get_stat())    
                