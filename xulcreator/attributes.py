
"""
xulapp.attributes
---

This holds the attributes structure and documentation

:copyright: 2010 Olafur Arason, see AUTHORS for more details
:license: license_name, see LICENCE for more details
:licence_doc: Creative Commons: Attribution-Sharelike >= v2.5
:licence_doc_code: MIT Licence
"""

__attributes = {"align": 
               {"type": "multiple:start, center, end, baseline, stretch,\
                        left, right", 
                "doc":  """\
The align attribute specifies how child elements of the box are aligned 
when the size of the box is larger than the total size of the children. For
boxes that have horizontal orientation, it specifies how its children will 
be aligned vertically. For boxes that have vertical orientation, it is used 
to specify how its children are aligned horizontally. The pack attribute is
related to the alignment but is used to specify the position in the 
opposite direction. You can also specify the value of align using the style 
property -moz-box-align.

start: Child elements are aligned starting from the left or top edge of the
box. If the box is larger than the total size of the children, the extra
space is placed on the right or bottom side.

center: Extra space is split equally along each side of the child elements,
resulting in the children being placed in the center of the box.
end: Child elements are placed on the right or bottom edge of the box. If
the box is larger than the total size of the children, the extra space is
placed on the left or top side.

baseline: This value applies to horizontally oriented boxes only. It causes
the child elements to be aligned so that their text labels are lined up.
stretch: The child elements are stretched to fit the size of the box. For a
horizontal box, the children are stretched to be the height of the box. For
a vertical box, the children are stretched to be the width of the box. If
the size of the box changes, the children stretch to fit. Use the flex
attribute to create elements that stretch in the opposite direction.

left: Deprecated The elements are aligned on their left edges.

right: Deprecated The elements are aligned on their right edges.

Reference: 
https://developer.mozilla.org/en/XUL/Attribute/align

                """
               },
               "allowevents":
               {"type": "boolean",
                "doc":  """\
If true, events are passed to children of the element. Otherwise, events 
are passed to the element only.

On listitem[1] and titlebar[2] elements, mouse events normally do not get 
sent to their children; instead they are retargeted to the listitem[1] and 
titlebar[2] element itself. This means that elements placed inside a listitem 
do not respond to events, and instead clicking the mouse simply selects that
item within the list. By setting the allowevents attribute to true, this
special behavior is disabled, and the events are targeted the same as other
elements.

For menu[3] , menuseparator[4] , menuitem[5] and treecol[6] elements, as 
well as menu buttons, and the popup datepicker[7] , mouse events are also 
retargeted to the element itself. However, the allowevents attribute is 
handled in a different way. Instead, the allowevents may be set to true on 
a descendant instead.

This does the same thing in that it allows events to be targeted normally,
but allows this to be different for each descendant.

This behavior is used for menus, for instance, to allow a menu button to
behave as a menu when clicking on it, yet have part of the menu behave as
a button. For the latter, the allowevents attribute is set to true to have
a click on the child button receive events instead of targeting all events
at the menu.

[1] https://developer.mozilla.org/en/XUL/listitem
[2] https://developer.mozilla.org/en/XUL/titlebar
[3] https://developer.mozilla.org/en/XUL/menu
[4] https://developer.mozilla.org/en/XUL/menuseparator
[5] https://developer.mozilla.org/en/XUL/menuitem
[6] https://developer.mozilla.org/en/XUL/treecol
[7] https://developer.mozilla.org/en/XUL/datepicker

Reference:
https://developer.mozilla.org/en/XUL/Attribute/allowevents

                """ 
               },
               "class":
               {"type": "string",
                "doc": """\
The style class of the element. Multiple classes may be specified by 
separating them with spaces.

Reference:
https://developer.mozilla.org/en/XUL/Attribute/class

                """
               },
               "coalesceduplicatearcs":
               {"type": "boolean",
                "doc": """\
Valid on any element that has a datasources[1] attribute. When multiple 
datasources are used, one may override an assertion from another. This 
attribute, if true, which is the default, allows a datasource to negate 
an earlier assertion.

[1] https://developer.mozilla.org/en/XUL/Attribute/datasources

Reference:
https://developer.mozilla.org/en/XUL/Attribute/coalesceduplicatearcs

                """
               },
               "collapsed":
               {"type": "boolean",
                "doc": """\
If true, then the element is collapsed and does not appear. It is 
equivalent to setting the CSS visibility property to collapse.

Reference:
https://developer.mozilla.org/en/XUL/Attribute/collapsed

                """
               },
               "container":
               {"type": "boolean",
                "doc": """\
Set to true if the element is to act as a container which can have child 
elements. This would be used for folders. This will be set by the template 
builder as needed.

Reference:
https://developer.mozilla.org/en/XUL/Attribute/container

                """
               },
               "containment":
               {"type": "uri",
                "doc": """\
This attribute specifies RDF properties that indicate that a resource is a 
container. When generating content from a template this is used to determine
which resources from the datasource are containers and thus can have child
nodes and which ones are not containers.

This attribute should be placed on the same element that the datasources[1] 
and the ref attribute is on. It may be set to a space-separated list[2] of 
RDF properties or resources.

[1] https://developer.mozilla.org/en/XUL/Attribute/datasources
[2] https://developer.mozilla.org/en/XUL/Attribute/ref

Reference:
https://developer.mozilla.org/en/XUL/Attribute/containment

                """
               },
               "context":
               {"type": "id",
                "doc": """\
Should be set to the value of the id of the popup element that should appear
when the user context-clicks on the element. A context-click varies on each
platform. Usually it will be a right click. You can use the special value
'_child' to indicate the first menupopup child of the element.

Reference:
https://developer.mozilla.org/en/XUL/Attribute/context

                """
               },
               "contextmenu":
               {"type": "id",
                "doc": """\
Alternate name for the context attribute, but also has a corresponding script
property contextMenu[1].

[1] https://developer.mozilla.org/en/XUL/Property/contextMenu

Reference:
https://developer.mozilla.org/en/XUL/Attribute/contextmenu

                """
               }, 
              }
