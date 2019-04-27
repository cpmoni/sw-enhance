from constant_maps import *
from extract_digit import extract_digit
from datetime import datetime
from rune import Rune

class Monster:
    
    def __init__(self,mj):
        self.id = mj['unit_id']
        self.number = mj['unit_master_id']
        if mj['homunculus'] == 0: 
            if str(self.number)[-2] == '1': self.name = monster['names'][self.number]
            else: self.name = '{} {}'.format(monster['attributes'][extract_digit(self.number,4)],monster['names'][extract_digit(self.number,0,3)])
        else: self.name = mj['homunculus_name']
        
        self.level = mj['unit_level']
        self.grade = mj['class']
        self.attribute = mj['attribute']
        
        self.hp = mj['con']*15
        self.atk = mj['atk']
        self.df = mj['def']
        self.spd = mj['spd']
        self.res = mj['resist']
        self.acc = mj['accuracy']
        self.cr = mj['critical_rate']
        self.cd = mj['critical_damage']
        
        self.create_time = datetime.strptime(mj['create_time'],'%Y-%m-%d %H:%M:%S')
        
        self.skills = [tuple(x) for x in mj['skills']]
        
        #print(f'Added {self}')
        
    def __str__(self):
        ans = f'{self.name}'
        return ans