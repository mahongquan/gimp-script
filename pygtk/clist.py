#!/usr/bin/env python

# example clist.py

import gtk

class CListExample:
    # User clicked the "Add List" button.
    def button_add_clicked(self, data):
        # Something silly to add to the list. 4 rows of 2 columns each
        drink = [ [ "Milk",    "3 Oz" ],
                  [ "Water",   "6 l" ],
                  [ "Carrots", "2" ],
                  [ "Snakes",  "55" ] ]

        # Here we do the actual adding of the text. It's done once for
        # each row.
        for indx in range(4):
            data.append(drink[indx])
        return

    # User clicked the "Clear List" button.
    def button_clear_clicked(self, data):
        # Clear the list using clear(). This is much faster than
        # calling remove() once for each row.
        data.clear()
        return

    # The user clicked the "Hide/Show titles" button.
    def button_hide_show_clicked(self, data):
        # Just a flag to remember the status. 0 = currently visible
        if self.flag == 0:
            # Hide the titles and set the flag to 1
            data.column_titles_hide()
            self.flag = self.flag+1
        else:
            # Show the titles and reset flag to 0
            data.column_titles_show()
            self.flag = self.flag-1
        return

    # If we come here, then the user has selected a row in the list.
    def selection_made(self, clist, row, column, event, data=None):
        # Get the text that is stored in the selected row and column
        # which was clicked in. We will receive it as a pointer in the
        # argument text.
        text = clist.get_text(row, column)

        # Just prints some information about the selected row
        print ("You selected row %d. More specifically you clicked"
               " in column %d, and the text in this cell is %s\n" % (
            row, column, text))
        return

    def __init__(self):
        titles = [ "Ingredients", "Amount" ]
        self.flag = 0
        window = gtk.GtkWindow(gtk.WINDOW_TOPLEVEL)
        window.set_usize(300, 150)

        window.set_title("GtkCList Example")
        window.connect("destroy", gtk.mainquit)

        vbox = gtk.GtkVBox(gtk.FALSE, 5)
        vbox.set_border_width(5)
        window.add(vbox)
        vbox.show()

        # Create a scrolled window to pack the CList widget into
        scrolled_window = gtk.GtkScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        vbox.pack_start(scrolled_window, gtk.TRUE, gtk.TRUE, 0)
        scrolled_window.show()

        # Create the CList. For this example we use 2 columns
        clist = gtk.GtkCList( 2, titles)

        # When a selection is made, we want to know about it. The callback
        # used is selection_made, and its code can be found further down
        clist.connect("select_row", self.selection_made)

        # It isn't necessary to shadow the border, but it looks nice :)
        clist.set_shadow_type(gtk.SHADOW_OUT)

        # What however is important, is that we set the column widths as
        # they will never be right otherwise. Note that the columns are
        # numbered from 0 and up (to 1 in this case).
        clist.set_column_width(0, 150)

        # Add the CList widget to the vertical box and show it.
        scrolled_window.add(clist)
        clist.show()

        # Create the buttons and add them to the window. See the button
        # tutorial for more examples and comments on this.
        hbox = gtk.GtkHBox(gtk.FALSE, 0)
        vbox.pack_start(hbox, gtk.FALSE, gtk.TRUE, 0)
        hbox.show()

        button_add = gtk.GtkButton("Add List")
        button_clear = gtk.GtkButton("Clear List")
        button_hide_show = gtk.GtkButton("Hide/Show titles")

        hbox.pack_start(button_add, gtk.TRUE, gtk.TRUE, 0)
        hbox.pack_start(button_clear, gtk.TRUE, gtk.TRUE, 0)
        hbox.pack_start(button_hide_show, gtk.TRUE, gtk.TRUE, 0)

        # Connect our callbacks to the three buttons
        button_add.connect_object("clicked", self.button_add_clicked, clist)
        button_clear.connect_object("clicked", self.button_clear_clicked,
                                    clist)
        button_hide_show.connect_object("clicked",
                                        self.button_hide_show_clicked,
                                        clist)

        button_add.show()
        button_clear.show()
        button_hide_show.show()

        # The interface is completely set up so we show the window and
        # enter the gtk_main loop.
        window.show()

def main():
    gtk.mainloop()
    return 0

if __name__ == "__main__":
    CListExample()
    main()
