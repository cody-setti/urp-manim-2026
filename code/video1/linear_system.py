from manim import *


def coefficient(value: float) -> str:
    r"""`value` to one decimal place, always reserving the width of a leading '-'.

    Holding the sign slot open with \phantom keeps a coefficient the same width whether it
    is positive or negative, so the equation's LaTeX layout is identical frame to frame.
    """
    text = f"{value:.1f}"
    return text if text.startswith("-") else rf"\phantom{{-}}{text}"


def equation(a: ValueTracker, b: ValueTracker, c: ValueTracker, color: str, anchor) -> MathTex:
    """Build "ax + by = c" from the trackers, pinned by its "y =" part to `anchor`.

    always_redraw() rebuilds this mobject every frame, and every Manim positioning method
    aligns by the *ink* bounding box, which breathes as the digits change -- a '0' fills
    its slot while a '1' does not -- so re-aligning each frame makes the equation jiggle.

    Instead "y =" is broken out as a part of its own: those two glyphs never change shape,
    and coefficient() keeps every other glyph at a fixed LaTeX offset from them, so pinning
    that one part alone holds every character still. Assumes the coefficients stay inside
    (-10, 10), where no number grows a second integer digit.
    """
    tex = MathTex(
        rf"{coefficient(a.get_value())}x {b.get_value():+.1f}",
        r"y =",
        coefficient(c.get_value()),
        color = color,
    )
    return tex.shift(anchor - tex[1].get_corner(DL))


class LinearSystem(Scene):
    def construct(self):
        cartesian_plane = NumberPlane(
            x_range               = [-10,10],
            y_range               = [-5 , 5],
            tips                  = False   ,
            axis_config           = {
                "color": "#ACACAC",
            }                               ,
            background_line_style = {
                "stroke_color": "#CFCFCF",
            }                               ,
        )
        self.add(cartesian_plane)

        # --- SINGLE LINEAR EQUATION ---
        # Show that a two-variable linear equation is
        # equivalent to a geometrical 2D line.

        # x + 2y = -1.5.
        a11, a12, b1 = 1.0, 2.0, -1.5
        a11v         = ValueTracker(a11)
        a12v         = ValueTracker(a12)
        b1v          = ValueTracker(b1)
        color1       = "#D42F2F"

        line1 = always_redraw(
            lambda: FunctionGraph(
                # a11x + a12y = b1 <=> y = (b1 - a11 x)/a12.
                lambda x: (b1v.get_value() - a11v.get_value()*x)/a12v.get_value(),
                color        = color1,
                stroke_width = 8     ,
            )
        )

        # Invisible layout frame: never added to the scene, it only fixes where this
        # row's "y =" belongs. See equation() for why the equation cannot corner itself.
        eq1_frame  = MathTex(r"\phantom{-}0.0x +0.0", r"y =", r"\phantom{-}0.0").to_corner(UR)
        eq1_anchor = eq1_frame[1].get_corner(DL)

        equation1 = always_redraw(
            lambda: equation(a11v, a12v, b1v, color1, eq1_anchor)
        )

        # Draw the initial line and equation.
        self.play(Create(line1), Write(equation1))
        self.wait(0.5)

        # Play around with b1.
        self.play(b1v.animate.set_value( 5.0), run_time=2  )
        self.play(b1v.animate.set_value(-4.0), run_time=2  )
        self.play(b1v.animate.set_value(-1.5), run_time=0.5)
        self.wait(0.5)

        # Play around with a11.
        self.play(a11v.animate.set_value( 4.0), run_time=2)
        self.play(a11v.animate.set_value(-2.0), run_time=2)
        self.play(a11v.animate.set_value( 1.0), run_time=1)
        self.wait(0.5)

        # Play around with a12.
        self.play(a12v.animate.set_value( 0.5), run_time=2)
        self.play(a12v.animate.set_value(-3.0), run_time=2)
        self.play(a12v.animate.set_value( 2.0), run_time=2)
        self.wait(1)



        # --- TWO LINEAR EQUATIONS ---
        # -2x + y = 3.
        a21, a22, b2 = -2.0, 1.0, 3.0
        a21v         = ValueTracker(-2.0)
        a22v         = ValueTracker( 1.0)
        b2v          = ValueTracker( 3.0)
        color2 = "#207500"

        line2 = always_redraw(
            lambda: FunctionGraph(
                # a21x + a22y = b2 <=> y = (b2 - a21 x)/a22.
                lambda x: (b2v.get_value() - a21v.get_value()*x)/a22v.get_value(),
                color        = color2,
                stroke_width = 8     ,
            )
        )

        # Same frame as the first equation, one line lower.
        eq2_frame  = eq1_frame.copy().next_to(eq1_frame, DOWN)
        eq2_anchor = eq2_frame[1].get_corner(DL)

        equation2 = always_redraw(
            lambda: equation(a21v, a22v, b2v, color2, eq2_anchor)
        )

        # Draw the second line and equation.
        self.play(Create(line2), Write(equation2))
        self.wait(0.5)

        # Make equations parallel.
        self.play(
            a21v.animate.set_value(-0.5),
            a22v.animate.set_value(-1.0),
            run_time=2
        )
        self.wait(1.5)

        self.play(
            a21v.animate.set_value(-2.0),
            a22v.animate.set_value( 1.0),
            run_time=2
        )
        self.wait(0.5)


        # --- TRANSITION TO ALGEBRAIC FORM ---
        self.play(
            FadeOut(cartesian_plane),
            FadeOut(line1),
            FadeOut(line2),
            FadeOut(equation1),
            FadeOut(equation2),
            run_time=1.5
        )
        self.wait(0.5)

        algebraic_system = MathTex(
            r"\begin{cases}"                                        ,  # 0
            rf"  \phantom{{-}}{a11:.0f}x {a12:+.0f}y &= {b1:.0f} \\",  # 1
            rf"  {a21:.0f}x {a22:+.0f}y &= \phantom{{-}}{b2:.0f} "  ,  # 2
            r"\end{cases}"                                          ,  # 3
            
            color = "#000000"                                     ,
        ).scale(1.5)

        # Apply the corresponding colors to each equation string
        algebraic_system[1].set_color(color1)
        algebraic_system[2].set_color(color2)

        # Draw the system on the screen
        self.play(Write(algebraic_system), run_time=2)
        self.wait(2)

        # --- TRANSITION TO MATRIX NOTATION ---
        matrix_system = MathTex(
            r"\begin{bmatrix} ",        # 0
            rf"\phantom{{-}}{a11:.0f}", # 1
            r" & ",                     # 2
            rf"{a12:.0f}",              # 3
            r" \\ ",                    # 4
            f"{a21:.0f}",               # 5
            r" & ",                     # 6
            rf"{a22:.0f}",              # 7
            r"\end{bmatrix}",           # 8
            r"\begin{bmatrix} x \\ y \end{bmatrix}", # 9
            r" = ",                     # 10
            r"\begin{bmatrix} ",        # 11
            rf"{b1:.0f}",               # 12
            r" \\ ",                    # 13
            rf"\phantom{{-}}{b2:.0f}",  # 14
            r" \end{bmatrix}",          # 15
            color = "#000000",
        ).scale(1.5)

        # Apply the corresponding colors to the rows to maintain visual continuity
        # Top row elements (Equation 1)
        matrix_system[1].set_color(color1)
        matrix_system[3].set_color(color1)
        matrix_system[12].set_color(color1)

        # Bottom row elements (Equation 2)
        matrix_system[5].set_color(color2)
        matrix_system[7].set_color(color2)
        matrix_system[14].set_color(color2)

        # Animate the transition by replacing the algebraic system with the matrix system
        self.play(FadeTransform(algebraic_system, matrix_system), run_time=2)
        self.wait(2)

        # --- TRANSITION TO SYMBOLIC MATRIX NOTATION ---
        symbolic_system = MathTex(
            r"\begin{bmatrix} ",       # 0
            r"a_{11}",                 # 1
            r" & ",                    # 2
            r"a_{12}",                 # 3
            r" \\ ",                   # 4
            r"a_{21}",                 # 5
            r" & ",                    # 6
            r"a_{22}",                 # 7
            r" \end{bmatrix}",         # 8
            r"\begin{bmatrix} x \\ y \end{bmatrix}", # 9
            r" = ",                    # 10
            r"\begin{bmatrix} ",       # 11
            r"b_1",                    # 12
            r" \\ ",                   # 13
            r"b_2",                    # 14
            r"\end{bmatrix}",          # 15
            color = "#000000",
        ).scale(1.5)

        # Apply the corresponding colors to the rows to maintain visual continuity
        # Top row elements (Equation 1)
        symbolic_system[1].set_color(color1)
        symbolic_system[3].set_color(color1)
        symbolic_system[12].set_color(color1)

        # Bottom row elements (Equation 2)
        symbolic_system[5].set_color(color2)
        symbolic_system[7].set_color(color2)
        symbolic_system[14].set_color(color2)

        # Animate the transition by replacing the matrix system with the symbolic system
        self.play(FadeTransform(matrix_system, symbolic_system), run_time=2)
        self.wait(2)

        # --- TRANSITION TO GENERAL m x n SYSTEM (EXPANDING ROWS/COLS) ---
        matrix_expanded = MathTex(
            r"\begin{bmatrix} ",                                     # 0
            r"a_{11}", r" & ", r"a_{12}", r" & \cdots & a_{1n} \\ ", # 1, 2, 3, 4 (Row 1)
            r"a_{21}", r" & ", r"a_{22}", r" & \cdots & a_{2n} \\ ", # 5, 6, 7, 8 (Row 2)
            r"\vdots & \vdots & \ddots & \vdots \\ ",                # 9 (Expansion down)
            r"a_{m1} & a_{m2} & \cdots & a_{mn} ",                   # 10 (Row m)
            r"\end{bmatrix}",                                        # 11
            r"\begin{bmatrix} ",                                     # 12
            r"x_1", r" \\ ", r"x_2", r" \\ ",                        # 13, 14, 15, 16
            r"\vdots \\ x_n ",                                       # 17 (Vector x expansion)
            r"\end{bmatrix}",                                        # 18
            r" = ",                                                  # 19
            r"\begin{bmatrix} ",                                     # 20
            r"b_1", r" \\ ",                                         # 21, 22
            r"b_2", r" \\ ",                                         # 23, 24
            r"\vdots \\ b_m ",                                       # 25 (Vector b expansion)
            r"\end{bmatrix}",                                        # 26
            color="#000000"
        ).scale(1.15) # Scaled down slightly to fit the screen width

        # Map colors to maintain visual connection with original equations
        matrix_expanded[1].set_color(color1)
        matrix_expanded[3].set_color(color1)
        matrix_expanded[4].set_color(color1)
        matrix_expanded[21].set_color(color1)

        matrix_expanded[5].set_color(color2)
        matrix_expanded[7].set_color(color2)
        matrix_expanded[8].set_color(color2)
        matrix_expanded[23].set_color(color2)

        self.play(FadeTransform(symbolic_system, matrix_expanded), run_time=2.5)
        self.wait(3)
