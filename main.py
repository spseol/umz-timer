import time
from tkinter import Frame, Tk, Button, Label, Widget
from tkinter.constants import BOTH, W, N, E, S

COPYRIGHT_FONT = ('Helvetica', 28)
LABELS_FONT = ('Helvetica', 50)
SECTION_FONT = ('Helvetica', 76)
TIME_FONT = ('Helvetica', 84)


class TimerFrame(Frame):
    start_btn = current_time_lbl = copyright_lbl = remaining_time_frame = remaining_time_lbl = section_lbl = None
    inverting_parts = []

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.setup_ui()
        self._update_current_time()

    def setup_ui(self):
        self.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.start_btn = Button(self, command=self._invert_ui, text='START!', font=LABELS_FONT)
        self.start_btn.grid(row=2, column=1, sticky=S)

        self.current_time_lbl = Label(self, font=LABELS_FONT)
        self.current_time_lbl.grid(row=2, column=0, sticky=W + S)

        self.copyright_lbl = Label(self, text='© Josef Kolář, 2016', font=COPYRIGHT_FONT)
        self.copyright_lbl.grid(column=2, row=2, sticky=S + E)

        self.section_lbl = Label(self, text='Introduction', font=SECTION_FONT)
        self.section_lbl.grid(column=1, row=0, sticky=N)

        self.elapsed_time_lbl = Label(self, text='0:00', font=LABELS_FONT)
        self.elapsed_time_lbl.grid(column=0, row=0, sticky=N+W)

        self.remaining_time_frame = Frame(self)
        self.remaining_time_frame.grid(column=1, row=1)

        self.remaining_time_lbl = Label(self.remaining_time_frame, text='0:00', font=TIME_FONT)
        self.remaining_time_lbl.pack()

        self.inverting_parts.extend((
            self.current_time_lbl,
            self.copyright_lbl,
            self.section_lbl,
            self.remaining_time_lbl,
            self.start_btn,
            self.master
        ))

    def _update_current_time(self):
        self.current_time_lbl.configure(text=time.strftime('%H:%M:%S'))
        self.master.after(1000, self._update_current_time)

    def _invert_ui(self):
        for part in self.inverting_parts:
            if isinstance(part, Widget):
                part['background'], part['foreground'] = part['foreground'], part['background']


if __name__ == '__main__':
    root = Tk()
    timer_frame = TimerFrame(root)

    timer_frame.pack(fill=BOTH)

    root.attributes('-zoomed', True)
    root.mainloop()
