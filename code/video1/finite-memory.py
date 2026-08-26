from manim import *

class FiniteMemory(Scene):
    def construct(self):
        # --- THE COMPUTER & "ZOOM IN" EFFECT ---
        
        # Build a simple stylized computer icon
        monitor_frame  = Rectangle(height=4.0, width=6.0, color=BLACK)
        monitor_frame.set_fill(BLACK, opacity=1)
        monitor_screen = Rectangle(height=3.5, width=5.5, color=WHITE)
        monitor_screen.set_fill("#F5FAFF", opacity=1)
        
        stand = Rectangle(height=0.8, width=1, color=BLACK)
        stand.set_fill(BLACK, opacity=1)
        stand.next_to(monitor_frame, DOWN, buff=0)
        
        base = Rectangle(height=0.3, width=2.5, color=BLACK)
        base.set_fill(BLACK, opacity=1)
        base.next_to(stand, DOWN, buff=0)
        
        computer = VGroup(monitor_frame, monitor_screen, stand, base)
        computer.center()

        # Animate the computer appearing
        self.play(FadeIn(computer), run_time=1.5)
        self.wait(0.5)

        # "Zoom in" by scaling the computer up massively, then fading it out
        # This gives the illusion of passing "through" the screen
        self.play(
            computer.animate.scale(15), 
            run_time=1.5, 
            rate_func=rush_into
        )
        self.play(FadeOut(computer), run_time=0.4)
        self.wait(0.5)

        # --- PI SEQUENCE ---
        # Create the Pi symbol and Equal sign
        pi_symbol = MathTex(r"\pi", color=BLACK)
        eq_symbol = MathTex("=", color=BLACK)
        
        equation_intro = VGroup(pi_symbol, eq_symbol)
        equation_intro.arrange(RIGHT, buff=0.3)

        # The digits we want to show: 3.141592 | 65359...
        # '6' is at index 8 in this array
        digits = ["3", ".", "1", "4", "1", "5", "9", "2", "6", "5", "3", "5", "9", r"\ldots"]
        
        # Group to hold all the memory boxes and overflowing text
        memory_sequence = VGroup()
        
        for i, char in enumerate(digits):
            text = MathTex(char, font_size=48, color=BLACK)
            
            # Digits before '6' (indices 0 to 7) fit in memory boxes
            if i < 8:
                if i == 1:
                    memory_sequence.add(text)
                else:
                    box = Square(side_length=0.7, color=BLUE)
                    # Group the text and the box together
                    box_group = VGroup(box, text)
                    memory_sequence.add(box_group)
            
            # The '6' and beyond overflow the memory (colored red, no box)
            else:
                box = Square(side_length=0.7, color=RED)
                # Group the text and the box together
                box_group = VGroup(box, text)
                text.set_color(RED)
                memory_sequence.add(box_group)

        # Arrange the sequence of boxes and red digits horizontally
        memory_sequence.arrange(RIGHT, buff=0.1)

        # Combine everything (Pi = [boxes][red digits]) and center it on screen
        full_equation = VGroup(equation_intro, memory_sequence)
        full_equation.arrange(RIGHT, buff=0.4)
        full_equation.center()

        # Shift it slightly left so the long tail of digits doesn't clip off-screen
        full_equation.shift(LEFT * 0.5)

        # --- ANIMATING THE MATH ---
        
        self.play(Write(equation_intro))
        self.wait(0.5)

        # Reveal digits one by one
        for i, item in enumerate(memory_sequence):
            # Slow down slightly when we hit the memory limit at '6' to emphasize it
            if i == 8:
                self.wait(0.5)
            
            self.play(Write(item), run_time=0.3)
            
        self.wait(2)
