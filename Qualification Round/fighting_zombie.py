import collections
import functools

class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
       self.func = func
       self.cache = {}
    def __call__(self, *args):
       if not isinstance(args, collections.Hashable):
          # uncacheable. a list, for instance.
          # better to not cache than blow up.
          return self.func(*args)
       if args in self.cache:
          return self.cache[args]
       else:
          value = self.func(*args)
          self.cache[args] = value
          return value
    def __repr__(self):
       '''Return the function's docstring.'''
       return self.func.__doc__
    def __get__(self, obj, objtype):
       '''Support instance methods.'''
       return functools.partial(self.__call__, obj)

def chance_for_spell(spell, zombie_strength):
    (num_dice, sides_per_dice), bonus = spell
    if bonus:
        zombie_strength = zombie_strength - bonus

    all_rolls = total_rolls(num_dice, sides_per_dice)
    successful_rolls = count_kill_zombie(zombie_strength, num_dice, sides_per_dice)
    return float(successful_rolls)/(all_rolls)

@memoized
def count_kill_zombie(zombie_strength, num_dice, sides_per_dice):
    assert(num_dice >= 1)
    if zombie_strength <= num_dice:
        return total_rolls(num_dice, sides_per_dice)
    if zombie_strength > num_dice*sides_per_dice:
        return 0
    if num_dice == 1:
        return sides_per_dice - zombie_strength + 1
    new_num_dice = num_dice - 1
    return sum([count_kill_zombie(zombie_strength - x, new_num_dice, sides_per_dice) for x in range(1, sides_per_dice + 1)])

@memoized
def total_rolls(num_dice, sides_per_dice):
    return sides_per_dice**num_dice

def solve(health, spell_list):
    ans = max([chance_for_spell(spell, health) for spell in spell_list])
    if ans < 1e-6:
        ans = 0
    return ans

def parse_spell(as_string):
    if '+' in as_string:
        dice, handicap = as_string.split('+')
        return (parse_dice(dice), int(handicap))

    elif '-' in as_string:
        dice, handicap = as_string.split('-')
        return (parse_dice(dice), -1 * int(handicap))

    else:
        return (parse_dice(as_string), None)

def parse_dice(as_string):
    as_list = as_string.split('d')
    return map(int, (as_list[0], as_list[1]))

T = int(raw_input())
for case in range(1, T+1):
    health, num_spells = map(int, raw_input().strip().split())
    spell_list = map(parse_spell, raw_input().strip().split())
    result = solve(health, spell_list)
    print "Case #%s: %.7f" % (case, result)
