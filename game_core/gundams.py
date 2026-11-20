class Gundam:
    def __init__(self, name, health, melee, ranged, defense, speed, special = None):
        """Manages core structural stats"""
        self.name = name
        
        self.max_health = float(health)
        self.base_melee = float(melee) 
        self.base_ranged = float(ranged) 
        self.base_defense = float(defense)
        self.base_speed = float(speed)

        self.health = float(health) 
        self.melee = float(melee) 
        self.ranged = float(ranged) 
        self.defense = float(defense)
        self.speed = float(speed)
   
        self.special = special

    
    def reset(self):
        "Stat baptism"
        self.health = self.max_health
        self.melee = self.base_melee
        self.ranged = self.base_ranged
        self.defense = self.base_defense
        self.speed = self.base_speed
