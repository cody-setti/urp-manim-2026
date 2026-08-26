import random
from manim import *
from manim.opengl import *

class Fence(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # --- POSTS ---
        # Cylinders point towards the z axis by default (OUT in Manims coordinates).
        post_height  = 3.0
        post_radius  = 0.2
        post_color   = "#EB9A6B"
        bases_color  = "#D08050"
        
        post1 = Cylinder(
            radius              = post_radius            ,
            height              = post_height            ,
            checkerboard_colors = [post_color,post_color],
            stroke_width        = 0                      ,
            show_ends           = True                   ,
        )
        post1[-1].set_style(fill_color=bases_color, fill_opacity=1, stroke_width = 0,)
        post1[-2].set_style(fill_color=bases_color, fill_opacity=1, stroke_width = 0,)
        post1.shift(LEFT * 2)
        
        post2 = Cylinder(
            radius              = post_radius            ,
            height              = post_height            ,
            checkerboard_colors = [post_color,post_color],
            stroke_width        = 0                      ,
            show_ends           = True                   ,
        )
        post2[-1].set_style(fill_color=bases_color, fill_opacity=1, stroke_width = 0,)
        post2[-2].set_style(fill_color=bases_color, fill_opacity=1, stroke_width = 0,)
        post2.shift(RIGHT * 2)
        
        # --- RAILS ---
        rail_color = "#A0522D"
        rail_width = 0.1
        offset     = post_radius + (rail_width / 2)# = 0.25
        
        # We start by deforming a 1x1x1 cube
        # Scaling factors: [X (legnth), Y (width), Z (height)]
        top_rail = Cube(side_length=1, fill_color=rail_color, fill_opacity=1)
        top_rail.scale([4.4, 0.1, 0.3])
        top_rail.shift(OUT  * 0.8   )
        top_rail.shift(DOWN * offset)
        
        bot_rail = Cube(side_length=1, fill_color=rail_color, fill_opacity=1)
        bot_rail.scale([4.4, 0.1, 0.3])
        bot_rail.shift(IN   * 0.8   )
        bot_rail.shift(DOWN * offset)
        
        # --- FENCE ---
        fence = VGroup(post1, post2, top_rail, bot_rail)

        # --- GRASS ---
        floor_z_level = IN * (post_height / 2)# = -1.5*e3
        grass = Square(
            side_length  = 20       ,
            fill_color   = "#6F7F72",
            fill_opacity = 1        ,
            stroke_width = 0        ,
        )
        grass.shift(floor_z_level)

        # --- ANIMATIONS ---
        self.play(FadeIn(grass), run_time=0.75)
        
        self.play(
            FadeIn(post1, shift=OUT),
            FadeIn(post2, shift=OUT),
            run_time=0.5
        )
        self.play(
            FadeIn(top_rail, shift=LEFT ),
            FadeIn(bot_rail, shift=RIGHT),
            run_time=0.5
        )
        
        self.move_camera(theta=45 * DEGREES, run_time=4)
        self.wait()
