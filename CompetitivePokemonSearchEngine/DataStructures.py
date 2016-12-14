Stats = namedtuple('Stats', 'HP, Atk, Def, SpA, SpD, Spe')

# Things like ability and moves should be singleton classes with only static
# methods
class Pokemon:
    def __init__(self, name, type1, type2, level, base_stats, ability, nature
                IVs=[[31 for i in xrange(6)]], hidden_power_type, moves, item):
        self.type1 = type1
        self.type2 = type2
        self.level = level
        self.base_stats = Stats._make(base_stats)
        self.ability = ability
        self.nature = nature
        self.IVs = Stats._make(IVs)
        fix_IVs(hidden_power_type)
        self.EVs = Stats._make([0 for i in xrange(6)])
        self.HP = self.actual_stats.HP
        self.status = None
        self.set_moves(moves)
        self.set_item(item)
        self.stat_levels = [0 for i in xrange(5)]

    def fix_IVs(self, hidden_power_type):
        return

    def set_EVs(self, EVs):
        self.EVs = Stats._make(EVs)
        # now sanity check and fix or throw

        # generate actual stats
        self.gen_actual_stats()

    def set_moves(self, moves):
        self.moves = set(moves)
        # sanity check

    def gen_actual_stats(self):
        self.actual_stats = Stats._make(
            map(lambda x: self.calculate_actual_stat(
                self.base_stats._fields[x],
                self.base_stats[x],
                self.IVs[x],
                self.EVs[x]), range(6)))

    def set_item(self, item):
        self.item = item

    def calculate_actual_stat(self, name, base, iv, ev):
        if name == "HP":
            return 0
        else:
            return 0

    def apply_ability(self, other):
        self.ability.apply(self, other)

    def apply_status(self):
        return

# Each resulting move class should be singleton? Or just have global dictionary
# for move legality?
class Move:
    def __init__(self, name, type, power,
                 accuracy, max_pp, priority, pokemons, properties):
        return

    def apply(self, offender, defender):
        return 0

class TypeEnduranceBST():
    def __init__(self, type):
        return
    
