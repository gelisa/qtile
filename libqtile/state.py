# Copyright (c) 2012, Tycho Andersen. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class QtileState(object):
    """
        Represents the state of the qtile object. Primarily used for restoring
        state across restarts; any additional state which doesn't fit nicely
        into X atoms can go here.
    """
    def __init__(self, qtile):
        # Note: window state is saved and restored via _NET_WM_STATE, so
        # the only thing we need to restore here is the layout and screen
        # configurations.
        self.groups = {}
        self.screens = {}
        self.layouts ={}
        self.windows={}
        _windows = {}
        for group in qtile.groups:
            #try:
            self.windows[group.name]=str(group.windows)
            _windows[group.name]=list(group.windows)
            self.groups[group.name] = group.layout.name
            qtile.log.info('current layout:\n'+str(group.layout))
            self.layouts[group.name] = {}
            #qtile.log.info(str(
            if group.layout.name == 'stack':
                for indx in range(group.layout.num_stacks):
                    currStack = group.layout.stacks[indx]
                    qtile.log.info('indx '+str(indx)+' group.name '+str(group.name))
                    self.layouts[group.name][indx]=([],)
                    if not currStack.lst==[]:
                        windowList=[]
                        for window in currStack.lst:
                            qtile.log.info(str(window))
                            windowList.append(
                                _windows[group.name].index(window))
                        currentWindow=\
                            _windows[group.name].index(currStack.cw)
                        self.layouts[group.name][indx]=(windowList,currentWindow)
                        
        for index, screen in enumerate(qtile.screens):
            self.screens[index] = screen.group.name
    
    def __str__(self):
        str1= 'My state is:\n'
        str1+='Groups:\t'+str(self.groups)+'\n'
        str1+='Screens:\t'+str(self.screens)+'\n'
        str1+='Stack Layouts:\t'+str(self.layouts)+'\n'
        str1+='Windows:\t'+str(self.windows)+'\n'
        return str1
    
    def __repr__(self):
        return self.__str__()
    
    def apply(self, qtile):
        """
            Rearrange the windows in the specified Qtile object according to
            this QtileState.
        """
        qtile.log.info(str(self))
        for (group, layout) in self.groups.items():
            try:
                qtile.groupMap[group].layout = layout
                
            except KeyError:
                pass  # group missing
            

        for (screen, group) in self.screens.items():
            try:
                group = qtile.groupMap[group]
                qtile.screens[screen].setGroup(group)
            except (KeyError, IndexError):
                pass  # group or screen missing
            
        for (group, layout) in self.layouts.items():
            currGroup = qtile.groupMap[group]
            _windows = list(currGroup.windows)
            for stackNum in layout.keys():
                currLayout = currGroup.layouts[currGroup.currentLayout]
                qtile.log.info(str(currLayout))
                if currLayout.name == 'stack':
                    for indx in range(currLayout.num_stacks):
                        currStack = currLayout.stacks[indx]
                        currStack.lst = [_windows[i] for i in layout[indx][0]]
                        currStack.current = layout[indx][1]
        stateAgain = QtileState(qtile)
        qtile.log.info(self)
        qtile.log.info(stateAgain)