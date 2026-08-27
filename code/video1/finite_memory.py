from manim import *

# Pi, split at the point where the machine runs out of room.
STORED   = "3.141592"                            # ~7 significant digits: about a float32's worth
OVERFLOW = ["6", "5", "3", "5", "9", r"\ldots"]  # more than it can hold

CELL_SIZE  = 0.7
DIGIT_SIZE = 48


def memory_cell(char: str, *, stored: bool) -> VGroup:
    """A digit of pi sitting in one cell of memory.

    Every digit gets a cell, so the spacing stays even along the whole sequence, but
    the cell is only drawn for digits the machine can actually store: the ones that
    overflow are left floating in red, with nothing to hold them.
    """
    cell  = Square(side_length=CELL_SIZE, color=BLUE)
    digit = MathTex(char, font_size=DIGIT_SIZE, color=BLACK if stored else RED)
    if not stored:
        cell.set_stroke(opacity=0)
    return VGroup(cell, digit)


def reveal(mobject):
    """Write() the parts of `mobject` one at a time.

    Under the OpenGL renderer, Write() on a VGroup whose children have different
    shapes -- a Square next to a MathTex, or two MathTex of unequal length --
    crashes inside DrawBorderThenFill: it zips the mobject families and then tries
    to interpolate point arrays that do not line up ("could not broadcast input
    array from shape (12,3) into shape (6,3)"). Animating each child separately
    looks the same on screen and avoids that path entirely.
    """
    parts = mobject.submobjects if isinstance(mobject, VGroup) else [mobject]
    return [Write(part) for part in parts]


class FiniteMemory(Scene):
    """Dives into a computer to show pi running out of memory mid-expansion."""

    def construct(self):
        # --- THE COMPUTER & "ZOOM IN" EFFECT ---
        monitor_frame  = Rectangle(width=6.0, height=4.0, color=BLACK, fill_opacity=1)
        monitor_screen = Rectangle(width=5.5, height=3.5, color=WHITE, fill_color="#F5FAFF", fill_opacity=1)
        stand          = Rectangle(width=1.0, height=0.8, color=BLACK, fill_opacity=1)
        base           = Rectangle(width=2.5, height=0.3, color=BLACK, fill_opacity=1)

        stand.next_to(monitor_frame, DOWN, buff=0)
        base.next_to(stand, DOWN, buff=0)

        computer = VGroup(monitor_frame, monitor_screen, stand, base)
        computer.center()

        self.play(FadeIn(computer), run_time=1.5)
        self.wait(0.5)

        # Scaling the computer up massively, then fading it out, gives the illusion
        # of passing "through" the screen.
        self.play(
            computer.animate.scale(15),
            run_time=1.5,
            rate_func=rush_into,
        )
        self.play(FadeOut(computer), run_time=0.4)
        self.wait(0.5)

        # --- PI SEQUENCE ---
        equation_intro = VGroup(
            MathTex(r"\pi", color=BLACK),
            MathTex("=",    color=BLACK),
        )
        equation_intro.arrange(RIGHT, buff=0.3)

        memory_sequence = VGroup()
        for char in STORED:
            # The decimal point is punctuation, not a stored digit, so it gets no cell.
            if char == ".":
                memory_sequence.add(MathTex(char, font_size=DIGIT_SIZE, color=BLACK))
            else:
                memory_sequence.add(memory_cell(char, stored=True))
        memory_sequence.add(*(memory_cell(char, stored=False) for char in OVERFLOW))
        memory_sequence.arrange(RIGHT, buff=0.1)

        full_equation = VGroup(equation_intro, memory_sequence)
        full_equation.arrange(RIGHT, buff=0.4)
        full_equation.center()
        # Shift it slightly left so the long tail of digits doesn't clip off-screen.
        full_equation.shift(LEFT * 0.5)

        # --- ANIMATING THE MATH ---
        self.play(*reveal(equation_intro))
        self.wait(0.5)

        first_overflow = len(memory_sequence) - len(OVERFLOW)
        for i, cell in enumerate(memory_sequence):
            # Hold on the memory limit for a beat, to let it land.
            if i == first_overflow:
                self.wait(0.5)
            self.play(*reveal(cell), run_time=0.3)

        self.wait(2)
