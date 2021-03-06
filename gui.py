import urwid

from guihelper import FilePanel, SearchPanel, StatusBar

PALETTE = [
    ('match', 'dark red', 'black')
]

class GUI():
    def __init__(self, files):
        self.searchpanel = SearchPanel()
        self.filepanel = FilePanel(files)
        self.statusbar = StatusBar(files)
        self.confirm = None

        frame = urwid.Pile([('pack', self.searchpanel.get_widget())
                            , self.filepanel.get_widget()
                            , ('pack', self.statusbar.get_widget())])
        self.loop = urwid.MainLoop(frame, PALETTE, unhandled_input=self.handle_input)

    def handle_input(self, key):
        if key in ['esc']:
            raise urwid.ExitMainLoop()
        elif key in ['ctrl r'] and self.confirm != None:
            self.confirm()
            self.searchpanel.reset()

    def search(self, searchtext, files):
        matches = self.filepanel.search(searchtext, files)
        self.statusbar.search(matches)

    def replace(self, replacement, delimiters, replaced):
        self.filepanel.replace(replacement, delimiters, replaced)

    def show(self):
        self.loop.run()

    def register_confirm_handler(self, handler):
        self.confirm = handler

    def register_search_listener(self, listener):
        urwid.connect_signal(self.searchpanel.search, 'change', listener)

    def register_replace_listener(self, listener):
        urwid.connect_signal(self.searchpanel.replace, 'change', listener)
