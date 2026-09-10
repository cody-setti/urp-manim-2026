from manim import *
import numpy as np

# --- POST CONFIGURATION ---
POST_RADIUS = 0.15
POST_COLOR  = "#552F22"

POST_BUFF   = 1
POST_COUNT  = 5

POST_NUDGE  = 0.3  # Installation error knocked into posts[1].

def post() -> Circle:
    return Circle(
               radius       = POST_RADIUS,
               color        = POST_COLOR ,
               fill_opacity = 1          ,
           )

# --- RAIL CONFIGURATION ---
RAIL_WIDTH  = 0.1
RAIL_EXTRA  = 0.5  # Overhang past each end of the base length.
RAIL_COLOR  = "#BB8844"

def rail_against(first: Circle, second: Circle, base_length: float) -> Rectangle:
    tangent_dir = normalize(second.get_center() - first.get_center())
    normal_dir  = rotate_vector(tangent_dir, -PI / 2)

    start = first.get_boundary_point(normal_dir)
    end   = start + base_length * tangent_dir

    return Rectangle(
               width        = RAIL_WIDTH                   ,
               height       = base_length + 2 * RAIL_EXTRA ,
               color        = RAIL_COLOR                   ,
               fill_opacity = 1                            ,
           ).rotate(
               # width axis -> normal, height axis -> tangent
               angle_of_vector(normal_dir),
           ).move_to(
               (start + end) / 2,
           )


class FenceTopView(Scene):
    def construct(self):
        # --- CREATE AND DISPLAY POSTS ---
        posts = VGroup(*(post() for _ in range(POST_COUNT)))
        posts.arrange(UP, buff=POST_BUFF)

        self.play(
            LaggedStart(
                *(FadeIn(p) for p in posts),
                lag_ratio = 0.15,
            ),
            run_time = 1.5,
        )

        # --- CREATE AND DISPLAY RAIL ---
        rail_base = posts[-1].get_center()[1] - posts[0].get_center()[1]
        rail = always_redraw(lambda: rail_against(posts[0], posts[1], rail_base))

        self.play(FadeIn(rail))

        # --- NUDGE THE SECOND POST ---
        self.wait(0.5)
        self.play(posts[1].animate.shift(RIGHT * POST_NUDGE), run_time=2)
        self.wait(1.5)
