#!/usr/bin/env python

# example list.py


import gtk, GDK

class ListExample:
    # This is our data identification string to store
    # data in list items
    list_item_data_key="list_item_data"

    # Main function to set up the user interface
    def __init__(self):
        # Create a window to put all the widgets in
        # connect main_quit() to the "destroy" event of
        # the window to handle window manager close-window-events
        window = gtk.GtkWindow(gtk.WINDOW_TOPLEVEL)
        window.set_title("GtkList Example")
        window.connect("destroy", gtk.mainquit)

        # Inside the window we need a box to arrange the widgets
        # vertically
        vbox = gtk.GtkVBox(gtk.FALSE, 5)
        vbox.set_border_width(5)
        window.add(vbox)
        vbox.show()

        # This is the scrolled window to put the List widget inside
        scrolled_window = gtk.GtkScrolledWindow()
        scrolled_window.set_usize(250, 150)
        vbox.add(scrolled_window)
        scrolled_window.show()

        # Create the GtkList widget.
        # Connect the sigh_print_selection() signal handler
        # function to the "selection_changed" signal of the List
        # to print out the selected items each time the selection
        # has changed
        gtklist = gtk.GtkList()
        scrolled_window.add_with_viewport(gtklist)
        gtklist.show()
        gtklist.connect("selection_changed", self.sigh_print_selection)
    
        # We create a "Prison" to put a list item in )
        frame = gtk.GtkFrame("Prison")
        frame.set_usize(200, 50)
        frame.set_border_width(5)
        frame.set_shadow_type(gtk.SHADOW_OUT)
        vbox.add(frame)
        frame.show()

        # Connect the sigh_button_event() signal handler to the List
        # which will handle the "arresting" of list items
        gtklist.connect("button_release_event", self.sigh_button_event, frame)

        # Create a separator
        separator = gtk.GtkHSeparator()
        vbox.add(separator)
        separator.show()

        # Finally create a button and connect its "clicked" signal
        # to the destruction of the window
        button = gtk.GtkButton("Close")
        vbox.add(button)
        button.show()
        button.connect_object("clicked", window.destroy, window)

        # Now we create 5 list items, each having its own
        # label and add them to the List using add()
        # Also we query the text string from the label and
        # associate it with the list_item_data_key for each list item

        for i in range(5):
            buffer = "ListItemContainer with Label #%d" % i
            label = gtk.GtkLabel(buffer)
            list_item = gtk.GtkListItem()
            list_item.add(label)
            label.show()
            gtklist.add(list_item)
            list_item.show()
            string = label.get()
            list_item.set_data(self.list_item_data_key, string)

        # Here, we are creating another 5 labels, this time
        # we use GtkListItem() for the creation
        # For adding of the list items we put them all into a
        # list, and then add them by a single call to
        # append_items().

        dlist = []
        for i in range(5, 10):
            buffer = "List Item with Label %d" % i
            list_item = gtk.GtkListItem(buffer)
            dlist.append(list_item)
            list_item.show()
            list_item.set_data(self.list_item_data_key,
                               list_item.children()[0].get())

        gtklist.append_items(dlist)

        # Finally we want to see the window, don't we? )
        window.show()

    # This is the signal handler that got connected to button
    # press/release events of the List
    def sigh_button_event(self, gtklist, event, frame):
        # We only do something if the third (rightmost mouse button
        # was released
        if event.type == GDK.BUTTON_RELEASE and event.button == 3:
            # Fetch the currently selected list item which
            # will be our next prisoner )
	
            dlist = gtklist.get_selection()
            if dlist:
		new_prisoner = dlist[0]
            else:
		new_prisoner = None

            # Look for already imprisoned list items, we
            # will put them back into the list.
            dlist = frame.children()
            for list_item in dlist:
                list_item.reparent(gtklist)

            # If we have a new prisoner, remove him from the
            # List and put him into the frame "Prison".
            # We need to unselect the item first.
            if new_prisoner:
                static_dlist = [new_prisoner]
    
                gtklist.unselect_child(new_prisoner)
                new_prisoner.reparent(frame)

    # This is the signal handler that gets called if List
    # emits the "selection_changed" signal
    def sigh_print_selection(self, gtklist, func_data=None):
        # Fetch the list of selected items
        # of the List
        dlist = gtklist.get_selection()
    
        # If there are no selected items there is nothing more
        # to do than just telling the user so
        if not dlist:
            print "Selection cleared"
            return

        # Ok, we got a selection and so we print it
        str = "The selection is a "

        # Get the list item from the list
        # and then query the data associated with list_item_data_key.
        # We then just print it
        for list_item in dlist:
            item_data_string = list_item.get_data(self.list_item_data_key)
            str = str + "%s " % item_data_string

        print "%s\n" % str

def main():
    # Fire up the main event loop of gtk
    gtk.mainloop()
    # We get here after gtk_main_quit() has been called which
    # happens if the main window gets destroyed
    return 0

if __name__ == "__main__":
    ListExample()
    main()
