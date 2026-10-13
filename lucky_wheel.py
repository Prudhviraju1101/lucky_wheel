import math
import random
import tkinter as tk

# ---------- Settings ----------
TOTAL = 32                 # 1 nundi 32 varaku
SIZE = 720
CX = CY = SIZE // 2
R_OUTER = 330              # wheel outer edge
R_INNER = 235              # numbers ring inner edge
R_NUM = 283                # numbers ee radius lo untayi
R_BALL = 207               # ball track radius
R_HUB = 165                # center hub
SPIN_MS = 4500
FRAME_MS = 16
SEG = 360 / TOTAL

# ---------- Colors ----------
BG = "#12121c"
SEG_A = "#262a45"
SEG_B = "#1b1e33"
RIM = "#3b4070"
TEXT = "#d9dcf5"
GOLD = "#ffd166"
BALL = "#ffffff"
HUB = "#171827"
BTN = "#ff6b6b"
BTN_HOVER = "#ff8787"
BTN_OFF = "#4a4c66"


def center_angle(n):
    """Number n (1..TOTAL) center angle, degrees. 1 top lo, clockwise."""
    return -90 + (n - 1) * SEG


class NumberWheel:
    def __init__(self, root):
        self.root = root
        root.title("Lucky wheel")
        root.configure(bg=BG)
        root.resizable(False, False)
        self.c = tk.Canvas(root, width=SIZE, height=SIZE, bg=BG, highlightthickness=0)
        self.c.pack()

        self.segments, self.labels = {}, {}
        self.history = []
        self.winner = None
        self.busy = False
        self.angle = math.radians(center_angle(1))

        self.draw_wheel()
        self.draw_hub()
        self.draw_ball()

    # ---------- Drawing ----------
    def draw_wheel(self):
        c = self.c
        c.create_oval(CX - R_OUTER - 14, CY - R_OUTER - 14, CX + R_OUTER + 14, CY + R_OUTER + 14,
                      fill=RIM, outline="")
        for n in range(1, TOTAL + 1):
            mid = center_angle(n)
            start = -(mid + SEG / 2)  # tkinter angles counter-clockwise
            fill = SEG_A if n % 2 else SEG_B
            self.segments[n] = c.create_arc(
                CX - R_OUTER, CY - R_OUTER, CX + R_OUTER, CY + R_OUTER,
                start=start, extent=SEG, fill=fill, outline=BG, width=2)
        # inner circle ee numbers ring ni complete chestundi
        c.create_oval(CX - R_INNER, CY - R_INNER, CX + R_INNER, CY + R_INNER, fill=BG, outline=RIM, width=3)
        for n in range(1, TOTAL + 1):
            a = math.radians(center_angle(n))
            self.labels[n] = c.create_text(
                CX + R_NUM * math.cos(a), CY + R_NUM * math.sin(a),
                text=str(n), fill=TEXT, font=("Helvetica", 17, "bold"))

    def draw_hub(self):
        c = self.c
        c.create_oval(CX - R_HUB, CY - R_HUB, CX + R_HUB, CY + R_HUB, fill=HUB, outline=RIM, width=2)
        self.result = c.create_text(CX, CY - 55, text="?", fill=GOLD, font=("Helvetica", 84, "bold"))
        self.btn_shape = c.create_oval(CX - 80, CY + 20, CX + 80, CY + 72, fill=BTN, outline="", tags="btn")
        self.btn_text = c.create_text(CX, CY + 46, text="SPIN", fill="white",
                                      font=("Helvetica", 18, "bold"), tags="btn")
        self.hist = c.create_text(CX, CY + 118, text="", fill="#8b8fb8", font=("Helvetica", 12))
        c.tag_bind("btn", "<Button-1>", lambda e: self.spin())
        c.tag_bind("btn", "<Enter>", lambda e: self.set_btn(BTN_HOVER if not self.busy else BTN_OFF))
        c.tag_bind("btn", "<Leave>", lambda e: self.set_btn(BTN if not self.busy else BTN_OFF))

    def draw_ball(self):
        self.shadow = self.c.create_oval(0, 0, 0, 0, fill="#000000", outline="")
        self.ball = self.c.create_oval(0, 0, 0, 0, fill=BALL, outline=GOLD, width=3)
        self.move_ball(self.angle)

    def set_btn(self, color):
        self.c.itemconfig(self.btn_shape, fill=color)

    def move_ball(self, a):
        x, y, r = CX + R_BALL * math.cos(a), CY + R_BALL * math.sin(a), 13
        self.c.coords(self.ball, x - r, y - r, x + r, y + r)
        self.c.coords(self.shadow, x - r + 3, y - r + 4, x + r + 3, y + r + 4)

    # ---------- Spin ----------
    def spin(self):
        if self.busy:
            return
        self.busy = True
        self.set_btn(BTN_OFF)
        self.c.itemconfig(self.btn_text, text="...")
        self.c.itemconfig(self.result, text="?")
        if self.winner:  # previous highlight tiseyyi
            n = self.winner
            self.c.itemconfig(self.segments[n], fill=SEG_A if n % 2 else SEG_B)
            self.c.itemconfig(self.labels[n], fill=TEXT)

        self.winner = random.randint(1, TOTAL)
        start = self.angle
        target = math.radians(center_angle(self.winner))
        extra = (target - start) % (2 * math.pi)
        total = extra + 2 * math.pi * random.randint(5, 8)
        self.animate(start, total, 0)

    def animate(self, start, total, elapsed):
        t = min(elapsed / SPIN_MS, 1)
        ease = 1 - (1 - t) ** 3  # fast ga start, slow ga aagutundi
        self.angle = start + total * ease
        self.move_ball(self.angle)
        if t < 1:
            self.root.after(FRAME_MS, self.animate, start, total, elapsed + FRAME_MS)
        else:
            self.finish()

    def finish(self):
        n = self.winner
        self.c.itemconfig(self.segments[n], fill=GOLD)
        self.c.itemconfig(self.labels[n], fill="#1b1b2b")
        self.c.itemconfig(self.result, text=str(n))
        self.history = ([n] + self.history)[:6]
        self.c.itemconfig(self.hist, text="Last: " + "  ".join(map(str, self.history)))
        self.c.itemconfig(self.btn_text, text="SPIN")
        self.busy = False
        self.set_btn(BTN)


if __name__ == "__main__":
    root = tk.Tk()
    NumberWheel(root)
    root.mainloop()
