from manim import *

# --- POSTS ---
POST_HEIGHT = 3.0
POST_RADIUS = 0.2
POST_SPACING = 2.0  # Distance of each post from the centre of the fence.
POST_COLOR = "#EB9A6B"
CAP_COLOR = "#D08050"  # Darker, so the flat end caps read as end-grain.

# --- RAILS ---
# The rail is a deformed unit cube: [X (length), Y (thickness), Z (height)].
RAIL_LENGTH = 4.4
RAIL_THICKNESS = 0.1
RAIL_HEIGHT = 0.3
RAIL_SPACING = 0.8  # Height of each rail above/below the middle of the posts.
RAIL_COLOR = "#A0522D"
# Push the rails out in Y until their inner face is flush against the posts' surface.
RAIL_OFFSET = POST_RADIUS + RAIL_THICKNESS / 2


def make_post(x: float) -> Cylinder:
    """A fence post standing at `x`, with darker end caps."""
    post = Cylinder(
        radius       = POST_RADIUS,
        height       = POST_HEIGHT,
        stroke_width = 0,
        show_ends    = True,
    )
    post.set_color(POST_COLOR)
    for cap in (post.base_top, post.base_bottom):
        cap.set_style(fill_color=CAP_COLOR, fill_opacity=1)
    return post.shift(RIGHT * x)


def make_rail(height: float) -> Cube:
    """A horizontal rail at `height`, resting against the front face of the posts."""
    rail = Cube(side_length=1, fill_color=RAIL_COLOR, fill_opacity=1)
    rail.scale([RAIL_LENGTH, RAIL_THICKNESS, RAIL_HEIGHT])
    return rail.shift(OUT * height + DOWN * RAIL_OFFSET)


class Fence(ThreeDScene):
    """Raises a two-post fence, for the opening 'installing a fence' analogy."""

    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        left_post  = make_post(-POST_SPACING)
        right_post = make_post(+POST_SPACING)

        top_rail = make_rail(+RAIL_SPACING)
        bot_rail = make_rail(-RAIL_SPACING)

        # The ground plane, dropped to the foot of the posts.
        grass = Square(
            side_length  = 20,
            fill_color   = "#6F7F72",
            fill_opacity = 1,
            stroke_width = 0,
        )
        grass.shift(IN * (POST_HEIGHT / 2))

        # --- ANIMATIONS ---
        self.play(FadeIn(grass), run_time=0.75)

        self.play(
            FadeIn(left_post,  shift=OUT),
            FadeIn(right_post, shift=OUT),
            run_time=0.5,
        )
        self.play(
            FadeIn(top_rail, shift=LEFT ),
            FadeIn(bot_rail, shift=RIGHT),
            run_time=0.5,
        )

        self.move_camera(theta=45 * DEGREES, run_time=4)
        self.wait()
