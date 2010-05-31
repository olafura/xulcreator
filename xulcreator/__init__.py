#!/usr/bin/env python
# -*- coding: ascii -*-

"""
xulapp
---

This is a XUL generator that helps make XUL applications
more manageble.

:copyright: 2010 Olafur Arason, see AUTHORS for more details
:license: license_name, see LICENCE for more details
"""


from xml.dom.minidom import Document, CDATASection

class SelfReference(Exception):
    """This is a exception that is used to catch it 
    when you try to add your self as a child.
    >>> x = Xul(); x += x
    Traceback (most recent call last):
       ...
    SelfReference: 'Your adding your self'
    """
    def __init__(self, value):
        super(SelfReference, self).__init__(self, value)
        self.value = value
    def __str__(self):
        return repr(self.value)

class EmptyList(Exception):
    """This is a exception that is used to catch it 
    when you have have list in the begining of a
    list.
    >>> x = Xul(); x += [[H()]]
    Traceback (most recent call last):
       ...
    EmptyList: 'You cant start with two lists'
    """
    def __init__(self, value):
        super(EmptyList, self).__init__(self, value)
        self.value = value
    def __str__(self):
        return repr(self.value)

class ParentList(Exception):
    """This is a exception that is used to catch it 
    when you have two lists that are next to each
    other that can't be added to a parent. 
    >>> x = Xul(); x += [[H()]]
    Traceback (most recent call last):
       ...
    EmptyList: 'You cant start with two lists'
    """
    def __init__(self, value):
        super(ParentList, self).__init__(self, value)
        self.value = value
    def __str__(self):
        return repr(self.value)

class StrictError(Exception):
    """This is a exception that is used to catch it 
    when your document is not well formed. 
    >>> strict = True; x = H(foo="bar")
    Traceback (most recent call last):
       ...
    StrictError: 'Your trying to add an attribute that is not supported by the element'
    """
    def __init__(self, value):
        super(StrictError, self).__init__(self, value)
        self.value = value
    def __str__(self):
        return repr(self.value)

class List(object):
    """This is a helper class so it's possible to
    add parent reference to list. 
    >>> x = Xul(); list = List([1, 2, 3]); list.parent = x 
    >>> for i in list: print i
    1
    2
    3
    """
    def __init__(self, list):
        self.list = list
        self.parent = None
        # This index for the loop is set to
        # -1 because the index has to
        # incremented before the return and
        # python does not support post
        # increment 
        self.index = -1
    def __iter__(self):
        return self
    def next(self):
        """This function iters through the
        list.
        """
        #Check if we have hit the end of
        #the list 
        if self.index == len(self.list) - 1:
            """
            This resets the index so we
            can do this as often as
            needed
            """
            self.index = -1
            raise StopIteration
        self.index = self.index + 1 
        return self.list[self.index]

# Here we have the strict check that is by
# default set to False unless your debugging.
# This causes the library to check if the
# xml code is according to the spec. But
# this should not be on by default unless
# you are willing to take the performace hit.
# But you should run this if you don't want
# trouble in the rendering engine.
STRICT = True

class Xul(object):
    """This is the base xul element which all
    other elements inherit from. Also is used
    as the base container for the document
    >>> x = Xul(); x+=Window(); print x
    <?xml version="1.0" ?>
    <?xml-stylesheet type="text/css" href="chrome://global/skin"?>
    <window title="Xul Application" width="800" xmlns="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul" xmlns:html="http://www.w3.org/1999/xhtml"/>
    <BLANKLINE>
    """
    def __init__(self, element=None, kwargs=None, addprop=None):
        """This is a init function that is used to initilize common
        thing across the different children.
        """
        self._properties = { "align": "string", "allowevents": "string", 
        "allownegativeassertions": "string", "eclass": "string", 
        "class": "string", "coalesceduplicatearcs": "string", 
        "collapsed": "string", "container": "string", 
        "containment": "string", "context": "string", 
        "contextmenu": "string", "datasources": "string", 
        "dir": "string", "edir": "string", "empty": "string", 
        "equalsize": "string", "flags": "string", "flex": "string", 
        "height": "string", "hidden": "string", "eid": "string", 
        "id": "string", "insertafter": "string", "insertbefore": "string", 
        "left": "string", "maxheight": "string", "maxwidth": "string", 
        "menu": "string", "minheight": "string", "minwidth": "string", 
        "mousethrough": "string", "observes": "string", "ordinal": "string",
        "orient": "string", "pack": "string", "persist": "string", 
        "popup": "string", "position": "string", 
        "preference-editable": "string", "querytype": "string", 
        "ref": "string", "removeelement": "string", 
        "sortDirection": "string", "sortResource": "string", 
        "sortResource2": "string", "statustext": "string", "style": "string", 
        "template": "string", "tooltip": "string", "tooltiptext": "string", 
        "top": "string", "uri": "string", "wait-cursor": "string", 
        "width": "string", "xmlns": "string", "xmlns:html": "string" } 
        if(addprop):
            self._properties = dict(self._properties, **addprop)
        self._doc = Document()
        type(self).__name__="xulelement"
        if(element):
            self._element = self._doc.createElement(element)
        else:
            self._element = self._doc
            self._doc.appendChild(self._doc.createProcessingInstruction(\
            "xml-stylesheet","type=\"text/css\" href=\"chrome://global/skin\""))
        if(kwargs):
            for key in kwargs:
                if(key=="eid"):
                    self.__setattr__("id", kwargs[key])
                elif(key=="eclass"):
                    self.__setattr__("class", kwargs[key])
                elif(key=="eopen"):
                    self.__setattr__("open", kwargs[key])
                elif(key=="etype"):
                    self.__setattr__("type", kwargs[key])
                elif(key=="edir"):
                    self.__setattr__("dir", kwargs[key])
                else:
                    self.__setattr__(key, kwargs[key])
    def __setattr__(self, name, value):
        if name in self.__dict__ or name in ["_element", "_doc", "_properties"]:
            super(Xul, self).__setattr__(name, value)
        else:
            element = self.getelement() 
            if STRICT:
                if name in self._properties:
                    element.setAttribute(str(name), str(value))
                else:
                    raise StrictError("Your trying to add an attribute that is not supported by the element")
            else:
                element.setAttribute(str(name), str(value))

    def __getattr__(self, name):
        if name in self.__dict__:
            super(Xul, self).__getattr__(name)
        else:
            element = self.getelement()
            return element.getAttribute(name)
    def _adder(self, other, parent):
        """This is a helper function so it's possible to go
        recursively through adding elements"""
        if(self == other):
            raise SelfReference('Your adding your self') 
        if type(other).__name__=="list" or type(other).__name__=="List":
            last = None
            for other_element in other:
                if type(other_element).__name__=="list":
                    if(last):
                        self._adder(other_element, last)
                        last = List(other_element)
                        last.parent = parent
                    else:
                        raise EmptyList("You cant start with two lists")
                elif type(other_element).__name__=="str" or type(other).__name__=="int":
                    cdata = CDATASection()
                    cdata.data = str(other_element)
                    element = parent.getelement()
                    element.appendChild(cdata)
                    last = other_element
                elif type(other_element).__name__=="xulelement":
                    if type(parent).__name__=="List":
                        if parent.parent:
                            element = parent.parent.getelement()
                            eelement = other_element.getelement()
                            element.appendChild(eelement)
                            last = other_element 
                        else:
                            raise ParentList("You can't have list as an parent")
                    elif type(parent).__name__=="list":
                        raise ParentList("You can't have list as an parent")
                    else:
                        element = parent.getelement()
                        eelement = other_element.getelement()
                        element.appendChild(eelement)
                        last = other_element
                else:
                    print("What is happening")
                    print("type: "+type(other).__name__)
        elif type(other).__name__=="str" or type(other).__name__=="int":
            cdata = CDATASection()
            cdata.data = str(other)
            element = parent.getelement() 
            element.appendChild(cdata)
        elif type(other).__name__=="xulelement":
            element = parent.getelement()
            oelement = other.getelement()
            element.appendChild(oelement)
        else:
            print("What is happening")
            print("type: "+type(other).__name__)

    def __iadd__(self, other):
        self._adder(other, self)
        return self
    def __str__(self):
        element = self.getelement()
        return element.toprettyxml(indent="  ")
    def __repr__(self):
        return self.__str__()
    def getelement(self):
        """This returns the xml element to you
        so you can change it.
        """
        return self._element

class Window(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        addprop = {"hidechrome":"string", "lightweightthemes":"string", 
        "lightweightthemesfooter":"string", "screenX":"string", 
        "screenY":"string", "sizemode":"string", "title":"string", 
        "windowtype":"string", "onopen":"string", "onclose":"string"}
        super(Window, self).__init__(element="window" , kwargs=kwargs, addprop=addprop)
        if "height" not in kwargs:
            self.height = 600
        if "width" not in kwargs:
            self.width = 800
        if "title" not in kwargs:
            self.title = "Xul Application"
        self.__setattr__("xmlns:html", "http://www.w3.org/1999/xhtml")
        self.__setattr__("xmlns", 
        "http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul")

class Vbox(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Vbox, self).__init__(element="vbox" , kwargs=kwargs)

class Hbox(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Hbox, self).__init__(element="hbox", kwargs=kwargs)

V = Vbox
H = Hbox

class Spacer(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Spacer, self).__init__(element="spacer", kwargs=kwargs)

class Menulist(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        addprop = {"accesskey": "string", "crop": "string", 
        "disableautoselect": "string", "disabled": "string", 
        "editable": "string", "focused": "string", "image": "string", 
        "label": "string", "oncommand": "string", "eopen": "string", 
        "open": "string", "preference": "string", "readonly": "string", 
        "sizetopopup": "string", "tabindex": "string", "value": "string", 
        "onselect": "string"}
        super(Menulist, self).__init__(element="menulist", kwargs=kwargs, addprop=addprop)

class Menupopup(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Menupopup, self).__init__(element="menupopup", kwargs=kwargs)

class Template(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        addprop = {"expr":"string", "container":"string", "member":"string"}
        super(Template, self).__init__(element="template", kwargs=kwargs, addprop=addprop)

class Menuitem(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        addprop = {"acceltext":"string", "accesskey":"string", 
        "allowevents":"string", "autocheck":"string", "checked":"string", 
        "closemenu":"string", "command":"string", "crop":"string", 
        "description":"string", "disabled":"string", "image":"string", 
        "key":"string", "label":"string", "name":"string", 
        "selected":"string", "tabindex":"string", "etype":"string", 
        "type":"string", "validate":"string", "value":"string"}
        super(Menuitem, self).__init__(element="menuitem", kwargs=kwargs, addprop=addprop)

class Toolbarbutton(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        addprop = {"accesskey": "string", "autoCheck": "string", 
        "checkState": "string", "checked": "string", "command": "string", 
        "crop": "string", "edir": "string", "dir": "string", 
        "disabled": "string", "dlgtype": "string", "group": "string", 
        "image": "string", "label": "string", "oncommand": "string", 
        "eopen": "string", "open": "string", "orient": "string", 
        "tabindex": "string", "etype": "string", "type": "string",
        "validate": "string"}
        super(Toolbarbutton, self).__init__(element="toolbarbutton", kwargs=kwargs, addprop=addprop)

class Label(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        addprop = {"accesskey": "string", "control": "string", 
        "crop": "string", "disabled": "string", "href": "string", 
        "value": "string"}
        super(Label, self).__init__(element="label", kwargs=kwargs, addprop=addprop)

class Textbox(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Textbox, self).__init__(element="textbox", kwargs=kwargs)

class Button(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        addprop = {"accesskey": "string", "autoCheck": "string", 
        "checkState": "string", "checked": "string", "command": "string", 
        "crop": "string", "edir": "string", "dir": "string", 
        "disabled": "string", "dlgtype": "string", "group": "string", 
        "icon": "string", "image": "string", "label": "string", 
        "eopen": "string",  "open": "string", "orient": "string", 
        "tabindex": "string", "etype": "string", "type": "string", 
        "oncommand": "string"}
        super(Button, self).__init__(element="button", kwargs=kwargs, addprop=addprop)

class Panel(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Panel, self).__init__(element="panel", kwargs=kwargs)

class Tree(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Tree, self).__init__(element="tree", kwargs=kwargs)

class Treecols(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Treecols, self).__init__(element="template", kwargs=kwargs)

class Treecol(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Treecol, self).__init__(element="treecol", kwargs=kwargs)

class Rule(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Rule, self).__init__(element="rule", kwargs=kwargs)

class Treeitem(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Treeitem, self).__init__(element="treeitem", kwargs=kwargs)

class Treerow(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Treerow, self).__init__(element="treerow", kwargs=kwargs)

class Treecell(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        super(Treecell, self).__init__(element="treecell", kwargs=kwargs)

class Datepicker(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        addprop = {"disabled": "string", "firstdayofweek": "string", 
        "readonly": "string", "etype": "string", "type": "string", 
        "tabindex": "string", "value": "string", "onchange": "string"}
        super(Datepicker, self).__init__(element="datepicker", kwargs=kwargs, addprop=addprop)

class Htmlscript(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        addprop = {"async": "string", "src": "string", "defer": "string"}
        super(Htmlscript, self).__init__(element="html:script", kwargs=kwargs, addprop=addprop)

class Htmlembed(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        addprop = {"src": "string"}
        super(Htmlembed, self).__init__(element="html:embed", kwargs=kwargs, addprop=addprop)

class Iframe(Xul):
    """Description
    """
    def __init__(self, **kwargs):
        addprop = {"showcaret": "string", "src": "string", "type": "string", 
        "transparent": "string"}
        super(Iframe, self).__init__(element="iframe", kwargs=kwargs, addprop=addprop)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
