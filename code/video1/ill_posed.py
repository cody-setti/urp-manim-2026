from manim import *


class IllPosed(Scene):
    """Nudges one line of a 2x2 system, then swings the other towards it.

    The same small perturbation barely moves the solution while the lines are near
    perpendicular, and throws it off screen once they are near parallel: the key
    animation for the 2D conditioning section.
    """

    def construct(self):
        # --- DRAW WELL POSED SYSTEM ---
        # These are straight lines, but FunctionGraph is deliberate, not incidental: it
        # samples the function into a few hundred short bezier segments, which the
        # OpenGL stroke shader draws at the full requested width. The same line built
        # as a single long Line() segment renders visibly thinner.
        line1 = FunctionGraph(
            lambda x: 0,
            color        = BLUE,
            stroke_width = 6,
            z_index      = 1,
        )
        self.play(Create(line1))

        # Steep, so the two lines start out nearly perpendicular: a well conditioned system.
        line2 = FunctionGraph(
            lambda x: 8 * x,
            x_range      = [-0.6, 0.6],  # Just long enough to cross the frame.
            color        = GREEN,
            stroke_width = 6,
            z_index      = 1,
        )
        self.play(Create(line2))
        # Now that it has been drawn at frame size, extend it off screen so it still
        # spans the frame once the rotation at the end swings it towards horizontal.
        line2.scale(4)

        solution = Dot(color=PURPLE, radius=0.17, z_index=2)
        self.play(Create(solution))
        self.wait(0.5)

        # --- PERTURB SYSTEM ---
        # Ghosts of the unperturbed system, to compare the solution against.
        line1_ref    = line1.copy().set_opacity(0.3)
        solution_ref = solution.copy().set_opacity(0.5)
        self.add(line1_ref, solution_ref)

        solution.add_updater(
            lambda mob: mob.move_to(
                line_intersection(
                    (line1.get_start(), line1.get_end()),
                    (line2.get_start(), line2.get_end()),
                )
            )
        )

        perturbation = DOWN
        anchor       = RIGHT * 5
        pert_arrow = DashedLine(
            anchor,
            anchor + perturbation,
            dash_length  = 0.05,
            dashed_ratio = 0.5,
            color        = YELLOW,
            z_index      = -1,
        ).add_tip()
        self.play(
            line1.animate.shift(perturbation),
            Create(pert_arrow),
        )

        error = always_redraw(
            lambda: DashedLine(
                ORIGIN,
                solution.get_center(),
                dash_length  = 0.05,
                stroke_width = 6.5,
                color        = RED,
                z_index      = 3,
            ).add_tip(tip_length=0.25, tip_width=0.25)
        )
        self.play(FadeIn(error))
        self.wait()

        # --- WORSEN SYSTEM CONDITIONING ---
        # Swing line2 down towards line1. The same perturbation now drags the solution
        # far off screen.
        self.play(Rotate(line2, -PI / 2 + 0.3), run_time=4)
        self.wait(2)
