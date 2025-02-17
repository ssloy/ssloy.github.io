terminals = ['+', '1']
grammar = [['s', ['e']          ],
           ['e', ['1']          ],
           ['e', ['e', '+', 'e']]]

class Task:
    def __init__(self, rule, dot, start):
        self.rule  = rule  # index of the parse rule in the grammar
        self.dot   = dot   # index of next symbol in the rule (dot position)
        self.start = start # we saw this many tokens when we started the rule

    def next_symbol(self):
        prod = grammar[self.rule][1]
        return prod[self.dot] if self.dot<len(prod) else None

    def __eq__(self, other):
        return self.rule == other.rule and self.dot == other.dot and self.start == other.start

    def __repr__(self):
        prod = grammar[self.rule][1]
        a = ' '.join(prod[:self.dot])
        b = ' '.join(prod[self.dot:])
        week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        return f'({grammar[self.rule][0]}->{a}.{b}, {week[self.start]})'

def recognize(tokens):
    worklists = [ [ Task(0,0,0) ] ]

    def add_task(i, task):
        if len(worklists)==i:
            worklists.append([])
        if task not in worklists[i]:                    # avoid infinite loops, do not add the same task twice
            worklists[i].append(task)

    token_counter = 0
    while True:                                         # fetch tokens one by one until end of file
        token = next(tokens, None)
        if token_counter == len(worklists):             # the worklist is empty => not good
            return False
        i = 0                                           # task id
        while i < len(worklists[token_counter]):        # iterate through all tasks in current worklist
            task  = worklists[token_counter][i]
            next_symbol = task.next_symbol()            # next symbol in the production rule
            if next_symbol is None:                     # if no symbol: completed task
                for prev in worklists[task.start]:
                    if prev.next_symbol() == grammar[task.rule][0]:
                        add_task(token_counter, Task(prev.rule, prev.dot+1, prev.start))
            elif next_symbol in terminals:              # if next symbol is a terminal,
                if token and next_symbol == token:      # scan a token
                    add_task(token_counter+1, Task(task.rule, task.dot+1, task.start))
            else:                                       # if next symbol is nonterminal, emit a prediction task
                for idx, (lhs, rhs) in enumerate(grammar):
                    if lhs == next_symbol:
                        add_task(token_counter, Task(idx, 0, token_counter))
            i += 1
        token_counter += 1
        if not token: break                             # end of file
    cur = [ task for task in worklists[-1] if task == Task(0, len(grammar[0][1]), 0) ] # all completed tasks at the end of the parse
    print(worklists)
    return bool(cur)

print(recognize(iter(['1',
                      '+',
                      '1'
                     ])))

