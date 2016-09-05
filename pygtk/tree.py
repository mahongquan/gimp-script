#!/usr/bin/env python

# example tree.c

import gtk

class TreeExample:
    # for all the GtkItem:: and GtkTreeItem:: signals
    def cb_itemsignal(self, item, signame):
        # It's a Bin, so it has one child, which we know to be a
        # label, so get that
        label = item.children()[0]
        # Get the text of the label
        name = label.get()
        # Get the level of the tree which the item is in
        print "%s called for item %s->%s" % (signame, name, item)

    # Note that this is never called
    def cb_unselect_child(self, root_tree, child, subtree):
        print ("unselect_child called for root tree %s, "
               "subtree %s, child %s" % (root_tree, subtree, child))

    # Note that this is called every time the user clicks on an item,
    # whether it is already selected or not.
    def cb_select_child(self, root_tree, child, subtree):
        print ("select_child called for root tree %s, subtree %s, "
               "child %s\n" % (root_tree, subtree, child))

    def cb_selection_changed(self, tree):
        print "selection_change called for tree %s" % tree
        print "selected objects are:"

        for item in tree.get_selection():
            label = item.children()[0]
            name = label.get()
            print "\t%s" % name

    def __init__(self):
        itemnames = ["Foo", "Bar", "Baz", "Quux", "Maurice"]
        # a generic toplevel window
        window = gtk.GtkWindow(gtk.WINDOW_TOPLEVEL)
        window.connect("delete_event", gtk.mainquit)
        window.set_border_width(5)

        # A generic scrolled window
        scrolled_win = gtk.GtkScrolledWindow()
        scrolled_win.set_policy(gtk.POLICY_AUTOMATIC,
                                gtk.POLICY_AUTOMATIC)
        scrolled_win.set_usize(150, 200)
        window.add(scrolled_win)
        scrolled_win.show()

        # Create the root tree
        tree = gtk.GtkTree()
        print "root tree is %s" % tree
        # connect all GtkTree:: signals
        tree.connect("select_child", self.cb_select_child, tree)
        tree.connect("unselect_child", self.cb_unselect_child, tree)
        tree.connect("selection_changed", self.cb_selection_changed)
        # Add it to the scrolled window
        scrolled_win.add_with_viewport(tree)
        # Set the selection mode
        tree.set_selection_mode(gtk.SELECTION_MULTIPLE)
        # Show it
        tree.show()

        for i in range(5):
            # Create a tree item
            item = gtk.GtkTreeItem(itemnames[i])
            # Connect all GtkItem:: and GtkTreeItem:: signals
            item.connect("select", self.cb_itemsignal, "select")
            item.connect("deselect", self.cb_itemsignal, "deselect")
            item.connect("toggle", self.cb_itemsignal, "toggle")
            item.connect("expand", self.cb_itemsignal, "expand")
            item.connect("collapse", self.cb_itemsignal, "collapse")
            # Add it to the parent tree
            tree.append(item)
            # Show it - this can be done at any time
            item.show()
            # Create this item's subtree
            subtree = gtk.GtkTree()
            print "-> item %s->%s, subtree %s" % (itemnames[i], item, subtree)

            # This is still necessary if you want these signals to be called
            # for the subtree's children.  Note that selection_change will be 
            # signalled for the root tree regardless.
            subtree.connect("select_child", self.cb_select_child, subtree)
            subtree.connect("unselect_child", self.cb_unselect_child, subtree)
            # This has absolutely no effect, because it is completely ignored 
            # in subtrees
            subtree.set_selection_mode(gtk.SELECTION_SINGLE)
            # Neither does this, but for a rather different reason - the
            # view_mode and view_line values of a tree are propagated to
            # subtrees when they are mapped.  So, setting it later on would
            # actually have a (somewhat unpredictable) effect
            subtree.set_view_mode(gtk.TREE_VIEW_ITEM)
            # Set this item's subtree - note that you cannot do this until
            # AFTER the item has been added to its parent tree!
            item.set_subtree(subtree)

            for j in range(5):
                # Create a subtree item, in much the same way
                subitem = gtk.GtkTreeItem(itemnames[j])
                # Connect all GtkItem:: and GtkTreeItem:: signals
                subitem.connect("select", self.cb_itemsignal, "select")
                subitem.connect("deselect", self.cb_itemsignal, "deselect")
                subitem.connect("toggle", self.cb_itemsignal, "toggle")
                subitem.connect("expand", self.cb_itemsignal, "expand")
                subitem.connect("collapse", self.cb_itemsignal, "collapse")
                print "-> -> item %s->%s\n" % (itemnames[j], subitem)
                # Add it to its parent tree
                subtree.append(subitem)
                # Show it
                subitem.show()
        # Show the window and loop endlessly
        window.show()

def main():
    gtk.mainloop()
    return 0

if __name__ == "__main__":
    TreeExample()
    main()
