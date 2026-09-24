from manim import *

# --- POST CONFIGURATION ---
def post() -> Rectangle:
    return Rectangle(
               width        = POST_WIDTH ,
               height       = POST_HEIGHT,
               color        = POST_COLOR ,
               fill_opacity = 1          ,
           )

POST_WIDTH  = 0.3
POST_HEIGHT = 3.0
POST_COLOR  = "#BB8844"

POST_BUFF   = 2.5
POST_COUNT  = 5

# --- RAIL CONFIGURATION ---
def rail(base_length: float) -> Rectangle:
    return Rectangle(
               width        = base_length + 2 * RAIL_EXTRA,
               height       = RAIL_HEIGHT                 ,
               color        = RAIL_COLOR                  ,
               fill_opacity = 1                           ,
           )

RAIL_HEIGHT =  0.3
RAIL_EXTRA  =  0.5
RAIL_COLOR  = "#552F22"

RAIL_BUFF   =  1.5

RAIL_DIM    =  0.5  # Opacity of the lower rail after dimming.

# --- SCREW CONFIGURATION ---
def screw(post: Rectangle) -> Dot:
    return Dot(
               point   = post.get_center() + UP * SCREW_RISE,
               radius  = SCREW_RADIUS,
               color   = SCREW_COLOR ,
           )

SCREW_RISE   = 0.5*RAIL_HEIGHT + 0.5*RAIL_BUFF
SCREW_RADIUS = 0.06
SCREW_COLOR  = "#CCCCCC"

SCREW_NUDGE  = 0.3  # Installation error in where the rail got screwed on.

def screwed_rail(screws: (Dot, Dot), base_length: float) -> Rectangle:
    # Create rail mobject.
    screwed_rail = rail(base_length)
    
    # Align the rail's direction with the one intersepting both screws.
    tangent_dir   = normalize(screws[1].get_center() - screws[0].get_center())
    tangent_angle = angle_of_vector(tangent_dir)
    screwed_rail.rotate(tangent_angle)
    
    # Move the rail's center-point to screws' mid-point.
    start = screws[0].get_center()
    end   = start + base_length * tangent_dir
    screwed_rail.move_to((start + end) / 2)
    
    return screwed_rail


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
        base_length = posts[-1].get_center()[0] - posts[0].get_center()[0]
        top_rail    = rail(base_length)
        bottom_rail = rail(base_length)
        
        rails = VGroup(top_rail, bottom_rail)
        rails.arrange(DOWN, buff=RAIL_BUFF)
        rails.shift(DOWN * 0.75)
        
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
        self.wait(0.5)
        
        # ---                            ---
        # --- FOCUS ON SCREWING TOP RAIL ---
        # ---                            ---
        self.play(rails[1].animate.set_opacity(RAIL_DIM), run_time=1)
        
        # --- SCREW TO THE END POSTS ---
        screws = VGroup(screw(posts[0]), screw(posts[4]))
        
        top_rail.add_updater(lambda m: m.become(screwed_rail(screws, base_length)))
        
        self.play(
            LaggedStart(
                *(GrowFromCenter(s) for s in screws),
                lag_ratio = 0.3,
            ),
        )
        self.wait(1.5)
        
        # --- SHIFT THE PINNING POINT ON THE LAST POST ---
        self.play(screws[1].animate.shift(UP * SCREW_NUDGE), run_time=2)
        self.wait(1.5)
        
        # --- SLIDE THAT PINNING POINT IN TO THE SECOND POST ---
        self.play( screws[1].animate.set_x(posts[3].get_x()) )
        self.wait(2)
        
        self.play( screws[1].animate.set_x(posts[2].get_x()) )
        self.wait(2)
        
        self.play( screws[1].animate.set_x(posts[1].get_x()) )
        self.wait(2)
