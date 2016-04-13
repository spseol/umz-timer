import time
from copy import copy
from datetime import timedelta
from tkinter import Frame, Tk, Button, Label
from tkinter.constants import BOTH, W, N, E, S
from tkinter.font import Font, BOLD

EXAM_SECTIONS = (
    ('Introduction', timedelta(minutes=.5)),
    ('Part I.', timedelta(minutes=2.5)),
    ('Part II. A', timedelta(minutes=1.5)),
    ('Part II. B', timedelta(minutes=1.)),
    ('Part II. C', timedelta(minutes=1.5)),
    ('Part III.', timedelta(minutes=5)),
    ('Part IV.', timedelta(minutes=3)),
    ('Part V.', timedelta(minutes=3)),
    ('The End', timedelta()),
)
LIGHT = 'gainsboro'
DARK = 'black'

format_delta = lambda delta: '{}:{:02}'.format(delta.seconds // 60, delta.seconds % 60)


class TimerFrame(Frame):
    # tkinter widgets
    start_btn = current_time_lbl = copyright_lbl = remaining_time_frame = None
    section_title_lbl = elapsed_time_lbl = remaining_time_lbl = None
    inverting_parts = []
    ui_light = True

    # timer logic
    _actual_section = 0
    section_remaining = EXAM_SECTIONS[_actual_section][1]
    timer_id = None

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.COPYRIGHT_FONT = Font(master, family='Helvetica', size=28)
        self.LABELS_FONT = Font(master, family='Helvetica', size=50)
        self.SECTION_FONT = Font(master, family='Helvetica', size=76)
        self.TIME_FONT = Font(master, family='Helvetica', size=130, weight=BOLD)

        self.setup_ui()
        self._update_current_time()

    def setup_ui(self):
        self.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.start_btn = Button(self, command=self.start_timer, text='START!', font=self.LABELS_FONT)
        self.start_btn.grid(row=2, column=1, sticky=S)

        self.reset_btn = Button(self, command=self.reset_timer,
            text='VYNULOVAT!', font=self.COPYRIGHT_FONT
        )
        self.reset_btn.grid(row=2, column=2, sticky=S + E)

        self.current_time_lbl = Label(self, font=self.LABELS_FONT)
        self.current_time_lbl.grid(row=2, column=0, sticky=W + S)

        self.copyright_lbl = Label(self, text='© Josef Kolář, 2016', font=self.COPYRIGHT_FONT)
        self.copyright_lbl.grid(column=2, row=0, sticky=N + E)

        self.section_title_lbl = Label(self, font=self.SECTION_FONT)
        self.section_title_lbl.grid(column=1, row=0, sticky=N)

        self.elapsed_time_lbl = Label(self, text='0:00', font=self.LABELS_FONT)
        self.elapsed_time_lbl.grid(column=0, row=0, sticky=N + W)

        self.remaining_time_frame = Frame(self)
        self.remaining_time_frame.grid(column=1, row=1)

        self.remaining_time_lbl = Label(self.remaining_time_frame,
            text=format_delta(EXAM_SECTIONS[0][1]), font=self.TIME_FONT
        )
        self.remaining_time_lbl.pack()

        self.inverting_parts.extend((
            self.current_time_lbl,
            self.copyright_lbl,
            self.section_title_lbl,
            self.remaining_time_lbl,
            self.start_btn,
            self.elapsed_time_lbl,
            self.reset_btn
        ))

        self.refresh_section()

    def _update_current_time(self):
        self.current_time_lbl.configure(text=time.strftime('%H:%M:%S'))
        self.master.after(1000, self._update_current_time)

    def _invert_ui(self):
        self.ui_light = not self.ui_light
        bg, fg = (LIGHT, DARK)[self.ui_light], (LIGHT, DARK)[not self.ui_light]
        self.master.configure(bg=bg)
        self.configure(bg=bg)
        for part in self.inverting_parts:
            part['background'] = bg
            part['foreground'] = fg

    def start_timer(self):
        self.start_btn.configure(text='STOP!', command=self.stop_timer)
        self.timer_id = self.master.after(1000, self.update_timer)

    def update_timer(self):
        self.section_remaining -= timedelta(seconds=1)

        if self.section_remaining.total_seconds() == 0:
            self.actual_section += 1
        elif self.section_remaining.total_seconds() <= 5:
            self._invert_ui()

        self.remaining_time_lbl.configure(text=format_delta(self.section_remaining))
        self.elapsed_time_lbl.configure(
            text=format_delta(EXAM_SECTIONS[self.actual_section][1] - self.section_remaining)
        )
        if self.section_remaining.total_seconds() > 0:
            self.timer_id = self.master.after(100, self.update_timer)

    def stop_timer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        self.start_btn.configure(text='START!', command=self.start_timer)

    def reset_timer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        self.actual_section = 0
        self.start_btn.configure(text='START!', command=self.start_timer)

    @property
    def actual_section(self):
        return self._actual_section

    @actual_section.setter
    def actual_section(self, new):
        self._actual_section = new
        self.refresh_section()

    def refresh_section(self):
        section_title, section_length = EXAM_SECTIONS[self.actual_section]
        self.section_title_lbl.configure(text=section_title)
        self.section_remaining = copy(section_length)
        self.remaining_time_lbl.configure(text=format_delta(self.section_remaining))
        self.elapsed_time_lbl.configure(
            text=format_delta(EXAM_SECTIONS[self.actual_section][1] - self.section_remaining)
        )


if __name__ == '__main__':
    master = Tk()
    master.wm_title('ÚMZ ANJ - časování')
    timer_frame = TimerFrame(master)

    timer_frame.pack(fill=BOTH)

    master.minsize(900, 350)
    master.attributes('-zoomed', True)
    master.mainloop()
