from manim import *

# --- POST CONFIGURATION ---
POST_WIDTH  = 0.3
POST_HEIGHT = 3.0
POST_COLOR  = "#552F22"

POST_BUFF   = 2.5
POST_COUNT  = 5

def post() -> Rectangle:
    return Rectangle(
               width        = POST_WIDTH ,
               height       = POST_HEIGHT,
               color        = POST_COLOR ,
               fill_opacity = 1          ,
           )

# --- RAIL CONFIGURATION ---
RAIL_WIDTH  = 12.0
RAIL_HEIGHT =  0.3
RAIL_COLOR  = "#BB8844"

RAIL_BUFF   =  1.5
RAIL_COUNT  =  2

def rail() -> Rectangle:
    return Rectangle(
               width        = RAIL_WIDTH ,
               height       = RAIL_HEIGHT,
               color        = RAIL_COLOR ,
               fill_opacity = 1          ,
           )


class FenceFrontView(Scene):
    def construct(self):
        # --- CREATE AND DISPLAY POSTS ---
        posts = VGroup(*(post() for _ in range(POST_COUNT)))
        posts.arrange(RIGHT, buff=POST_BUFF)
        posts.shift(DOWN * 0.75)
        
        self.play(
            LaggedStart(
                *(FadeIn(p, shift=UP * 3) for p in posts),
                lag_ratio = 0.15,
            ),
            run_time = 1.5,
        )

        # --- CREATE AND DISPLAY RAILS ---
        rails = VGroup(*(rail() for _ in range(RAIL_COUNT)))
        rails.arrange(DOWN, buff=RAIL_BUFF)
        rails.shift(DOWN * 0.75)

        # A FadeIn starts at (target - shift), so LEFT enters from the right and vice versa.
        self.play(
            LaggedStart(
                *(
                    FadeIn(r, shift=(LEFT if i % 2 == 0 else RIGHT) * 8)
                    for i, r in enumerate(rails)
                ),
                lag_ratio = 0.15,
            ),
            run_time = 1.5,
        )
