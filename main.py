import time
from copy import copy
from datetime import timedelta
from tkinter import Frame, Tk, Button, Label, Widget
from tkinter.constants import BOTH, W, N, E, S

COPYRIGHT_FONT = ('Helvetica', 28)
LABELS_FONT = ('Helvetica', 50)
SECTION_FONT = ('Helvetica', 76)
TIME_FONT = ('Helvetica', 84)

EXAM_SECTIONS = (
    ('Introduction', timedelta(minutes=.5)),
    ('Part I.', timedelta(minutes=2.5)),
    ('Part II. A', timedelta(minutes=1.5)),
    ('Part II. B', timedelta(minutes=1.)),
    ('Part II. C', timedelta(minutes=1.5)),
    ('Part III.', timedelta(minutes=5)),
    ('Part IV.', timedelta(minutes=3)),
    ('The End', timedelta(minutes=3)),
)

format_delta = lambda delta: '{}:{:02}'.format(delta.seconds // 60, delta.seconds % 60)


class TimerFrame(Frame):
    # tkinter widgets
    start_btn = current_time_lbl = copyright_lbl = remaining_time_frame = None
    section_title_lbl = elapsed_time_lbl = remaining_time_lbl = None
    inverting_parts = []

    # timer logic
    actual_section = -1
    section_remaining = timedelta()

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.setup_ui()
        self._update_current_time()

    def setup_ui(self):
        self.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.start_btn = Button(self, command=self.start_timer, text='START!', font=LABELS_FONT)
        self.start_btn.grid(row=2, column=1, sticky=S)

        self.current_time_lbl = Label(self, font=LABELS_FONT)
        self.current_time_lbl.grid(row=2, column=0, sticky=W + S)

        self.copyright_lbl = Label(self, text='© Josef Kolář, 2016', font=COPYRIGHT_FONT)
        self.copyright_lbl.grid(column=2, row=0, sticky=N + E)

        self.section_title_lbl = Label(self, text=EXAM_SECTIONS[0][0], font=SECTION_FONT)
        self.section_title_lbl.grid(column=1, row=0, sticky=N)

        self.elapsed_time_lbl = Label(self, text='0:00', font=LABELS_FONT)
        self.elapsed_time_lbl.grid(column=0, row=0, sticky=N + W)

        self.remaining_time_frame = Frame(self)
        self.remaining_time_frame.grid(column=1, row=1)

        self.remaining_time_lbl = Label(self.remaining_time_frame, text='0:00', font=TIME_FONT)
        self.remaining_time_lbl.pack()

        self.inverting_parts.extend((
            self.current_time_lbl,
            self.copyright_lbl,
            self.section_title_lbl,
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

    def start_timer(self):
        self._set_next_section()
        self.master.after(1000, self.update_timer)

    def update_timer(self):
        self.section_remaining -= timedelta(seconds=1)

        if self.section_remaining.total_seconds() == 0:
            self._set_next_section()
        elif self.section_remaining.total_seconds() <= 5:
            self._invert_ui()

        self.remaining_time_lbl.configure(text=format_delta(self.section_remaining))
        self.master.after(1000, self.update_timer)

    def _set_next_section(self):
        self.actual_section += 1
        section_title, section_length = EXAM_SECTIONS[self.actual_section]
        self.section_title_lbl.configure(text=section_title)
        self.section_remaining = copy(section_length)


if __name__ == '__main__':
    master = Tk()
    timer_frame = TimerFrame(master)

    timer_frame.pack(fill=BOTH)

    master.attributes('-zoomed', True)
    master.mainloop()
