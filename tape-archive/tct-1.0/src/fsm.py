# -*- coding: utf-8 -*-

#    Game's Finite State Machine.
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


## @package fsm
#  Game's Finite State Machine.
#
# This module contains the implementation
# of the finite state machine of the game.

try:
    import constants
    from base import Base
except ImportError as err:
    try:
        import os
        path = os.path.basename(__file__)
        print((': '.join((path, str(err)))))
    # importing os failed, print a custom message...
    except ImportError:
        print((': '.join(("couldn't load module", str(err)))))
    exit(2)

## objects imported when `from <module> import *' is used
__all__ = ['State', 'FSM']


## class of a template state
#
# This class is the template of an FSM's state.
# It can be used by several FSM implementations.
class State(Base):

    ## create a new state
    #
    # @param self the object pointer
    # @param name the state's name
    def __init__(self, name):
        ## the name of the state
        assert(name is not '')
        self.name = name

    ## what to do when the state is enabled
    #
    # @param self the object pointer
    def do_actions(self):
        pass

    ## what should be satisfied for enabling the state
    #
    # @param self the object pointer
    def check_conditions(self):
        pass

    ## what to do before enabling the state
    #
    # @param self the object pointer
    def entry_actions(self):
        pass

    ## what to do after disabling the state
    #
    # @param self the object pointer
    def exit_actions(self):
        pass

    ## the string representation of the state
    #
    # @param self the object pointer
    # @return the state's name as a plain string
    def __str__(self):
        return self.name


## class of an FSM manager
#
# This class is the skeleton of an FSM.
class FSM(Base):

    ## initialize the FSM
    #
    # @param self the object pointer
    def __init__(self):

        ## dictionary of states
        self.states = dict()

        ## the active state
        self.active_state = None

    ## add a new state 
    #
    # @param self the object pointer    
    # @param state a state instance
    def add_state(self, state):
        self.states[state.name] = state

    ## perform the active's state's actions and
    ## then check whether it should be altered
    #
    # @param self the object pointer    
    def run(self):
        if self.active_state is None:
            return
        
        self.active_state.do_actions()

        new_state_name = self.active_state.check_conditions()

        if new_state_name:
            self.set_state(new_state_name)

    ## switch to a new active state
    #
    # @param self the object pointer
    # @param new_state_name the name of the new active state
    def set_state(self, new_state_name):
        if self.active_state:
            self.active_state.exit_actions()

        # make sure that the given state exists
        assert (new_state_name in self.states)

        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()
