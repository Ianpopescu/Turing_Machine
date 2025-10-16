"""
M3L110: Computers and Computing
Project 1 – Binary Addition Turing Machine
Author: Ian Popescu
Date: October 2025

Description:
This program implements a single-tape, single-head Turing Machine that performs
binary addition of two numbers written on the tape in little-endian form (least
significant bit on the right). The two numbers are separated by '+'.
Example:  0101+101  represents 1010 + 101 in standard binary.
"""

class TuringMachine:
    def __init__(self, tape, blank='+', start_state='q0', halt_state='qhalt'):
        # Tape represented as a list of characters with some blank padding
        self.tape = [blank] * 10 + list(tape) + [blank] * 10
        self.blank = blank
        self.head = 10  # start at the rightmost symbol
        self.state = start_state
        self.halt_state = halt_state

    def step(self, transitions):
        key = (self.state, self.tape[self.head])
        if key not in transitions:
            print(f"No transition for {key}, halting.")
            self.state = self.halt_state
            return
        next_state, write, move = transitions[key]
        self.tape[self.head] = write
        if move == 'R':
            self.head += 1
        elif move == 'L':
            self.head -= 1
        self.state = next_state

    def run(self, transitions):
        while self.state != self.halt_state:
            self.step(transitions)
        else:
            return ''.join(self.tape).strip(self.blank)

transitions = {
    # q0: read the next bit from the right (start at rightmost)
    ('q0', '0'): ('q0', '0', 'R'),
    ('q0', '1'): ('q0', '1', 'R'),
    ('q0', '+'): ('q1', '+', 'R'),

    ('q1', '0'): ('q1', '0', 'R'),
    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', '+'): ('q2', '+', 'L'),

    ('q2', '0'): ('q2', '1', 'L'),
    ('q2', '1'): ('q3', '0', 'L'),
    ('q2', '+'): ('q5', '+', 'R'),

    ('q3', '0'): ('q3', '0', 'L'),
    ('q3', '1'): ('q3', '1', 'L'),
    ('q3', '+'): ('q4', '+', 'L'),

    ('q4', '0'): ('q0', '1', 'R'),
    ('q4', '1'): ('q4', '0', 'L'),
    ('q4', '+'): ('q0', '1', 'R'),

    ('q5', '1'): ('q5', '0', 'R'),
    ('q5', '+'): ('qclean', '+', 'L'),

    ('qclean', '0'): ('qclean', '+', 'L'),
    ('qclean', '+'): ('qhalt', '+', 'L')


}



tm = TuringMachine("1010+101")
result = tm.run(transitions)
print(("Result:",tm.run(transitions)))
