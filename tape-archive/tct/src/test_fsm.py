# -*- coding: utf-8 -*-

#    Unit Tests for FSM.
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


'''Unit Tests for FSM.

Test the Finite State Machine's behaviour against invalid input, etc.
'''

try:
    import unittest
    import fsm
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

class StateBadInput(unittest.TestCase):
    '''Test how State reacts when bad input is given'''
    s = fsm.State('test')

    def testEmpty(self):
        '''State.__init__ should fail with empty string'''
        self.assertRaises(fsm.InitError, fsm.State.__init__, self.s, '')

    def testNull(self):
        '''State.__init__ should fail with null string'''
        self.assertRaises(fsm.InitError, fsm.State.__init__, self.s, None)

class FSMBadInput(unittest.TestCase):
    '''Test how FSM reacts when bad input is given'''
    f = fsm.FSM()

    def testInvalidState(self):
        '''set_state should fail with invalid state'''
        self.assertRaises(fsm.StateError, fsm.FSM.set_state, self.f, '')

    def testNullState(self):
        '''set_state should fail with null state'''
        f = fsm.FSM()
        self.assertRaises(fsm.StateError, fsm.FSM.set_state, self.f, None)

if __name__ == '__main__':
    unittest.main()
