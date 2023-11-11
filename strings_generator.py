class rules():
    rules = dict()
    def add_rule(self, key, value):
        self.rules[key] = value
    def apply_rules(self, char):
        return self.rules[char]

def generate_sequence(rules, string):
    accum = ""
    for c in string:
      try:
            accum += rules.apply_rules(c)
      except:
            accum += c
    return accum

def generate_pattern(rules, string, n):
    if(n <= 0):
        return string
    return generate_pattern(rules, generate_sequence(rules, string, ""), n-1)



