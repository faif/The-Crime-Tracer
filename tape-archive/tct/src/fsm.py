# -*- coding: utf-8 -*-

#    Finite State Machine.
#
#    This file is part of The Crime Tracer.
#
#    Copyright (C) 2009-11 Free Software Gaming Geeks <fsgamedev@googlegroups.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''Finite State Machine.

This module contains the implementation
of the finite state machine of the game.
'''

try:
    import constants
    from base import Base
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['State', 'FSM']

class InitError(ValueError):
    '''Raised when a wrong argument is passed on __init__'''
    
class State(Base):
    '''This class is the template of an FSM's state.
    It can be used by several FSM implementations.'''

    def __init__(self, name):
        if not name:
            raise InitError('Invalid state name: {0}'.format(name))
        self.name = name

    def do_actions(self):
        '''what to do when the state is enabled'''

    def check_conditions(self):
        '''what should be satisfied for enabling the state'''

    def entry_actions(self):
        '''what to do before enabling the state'''

    def exit_actions(self):
        '''what to do after disabling the state'''

    def __str__(self):
        return self.name

class StateError(ValueError):
    '''raised when invalid states are passed as arguments'''

class FSM(Base):
    '''this class is the skeleton of an FSM'''

    def __init__(self):
        self.states = dict()
        self.active_state = None

    def add_state(self, state):
        self.states[state.name] = state

    def run(self):
        '''perform the active's state's actions and
        then check whether it should be altered'''

        if not self.active_state:
            return

        self.active_state.do_actions()

        new_state_name = self.active_state.check_conditions()

        if new_state_name:
            self.set_state(new_state_name)

    def set_state(self, new_state_name):
        '''switch to a new active state'''

        if self.active_state:
            self.active_state.exit_actions()

        if not (new_state_name in self.states):
            raise StateError('Invalid state: {0}'.format(new_state_name))

            self.active_state = self.states[new_state_name]
            self.active_state.entry_actions()
