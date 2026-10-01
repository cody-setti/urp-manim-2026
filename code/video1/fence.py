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
RAIL_DIM    =  0.5  # Opacity of the lower rail after dimming.

RAIL_BUFF   =  1.5

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


class NakedFence(Scene):
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
        self.play( rails[1].animate.set_opacity(RAIL_DIM) )
        
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
        self.play( screws[1].animate.shift(UP * SCREW_NUDGE), run_time=2 )
        self.wait(2)
        
        # --- SLIDE THAT PINNING POINT IN TO THE SECOND POST ---
        self.play( screws[1].animate.set_x(posts[3].get_x()) )
        self.wait(2)
        
        self.play( screws[1].animate.set_x(posts[2].get_x()) )
        self.wait(2)
        
        self.play( screws[1].animate.set_x(posts[1].get_x()) )
        self.wait(2)

class FenceMath(Scene):
    def construct(self):
        # --- REBUILD FINAL STATE OF `NakedFence` ---
        posts = VGroup(*(post() for _ in range(POST_COUNT)))
        posts.arrange(RIGHT, buff=POST_BUFF)
        posts.shift(DOWN * 0.75)
        
        base_length = posts[-1].get_center()[0] - posts[0].get_center()[0]
        top_rail    = rail(base_length)
        bottom_rail = rail(base_length).set_opacity(RAIL_DIM)
        rails = VGroup(top_rail, bottom_rail)
        rails.arrange(DOWN, buff=RAIL_BUFF)
        rails.shift(DOWN * 0.75)
        
        screws = VGroup(screw(posts[0]), screw(posts[1]).shift(UP * SCREW_NUDGE))
        
        opacity_vt = ValueTracker(1)
        top_rail.add_updater(
            lambda m: m.become(
                screwed_rail(screws, base_length)
                .set_opacity(opacity_vt.get_value())
                .scale(posts[0].height / POST_HEIGHT, about_point=screws[0].get_center())
            )                ,
            call_updater=True,
        )
        
        self.add(posts, rails, screws)
        
        # --- ADD COORDINATE SYSTEM ---
        AX_COLOR = "#000000"
        ax = Axes(
            x_range     = [           0, 1.07*base_length, 1],
            y_range     = [-POST_HEIGHT,      POST_HEIGHT, 1],
            x_length    = 1.07*base_length                   ,
            y_length    = 2.00*POST_HEIGHT                   ,
            axis_config = {
                "color"        : AX_COLOR,
                "include_ticks": False   ,
                "include_tip"  : True    ,
                "tip_width"    : 0.1     ,
            }                                                ,
        )
        ax.shift(screws[0].get_center() - ax.get_origin())
        x_label   = MathTex("x", color=AX_COLOR).next_to(ax.x_axis.get_end(), RIGHT)
        y_label   = MathTex("y", color=AX_COLOR).next_to(ax.y_axis.get_end(), UP   )
        ax_labels = VGroup(x_label, y_label)
        
        self.play(Create(ax), Write(ax_labels), run_time=2)
        
        # --- INTERPRET RAIL AS A LINE ---
        LINE_COLOR = "#938AFF"
        line = always_redraw(
            lambda:
            Line(
                # [0, 1, 2, 3] <=> [UR, UL, DL, DR]
                midpoint( top_rail.get_vertices()[1], top_rail.get_vertices()[2] ),
                midpoint( top_rail.get_vertices()[0], top_rail.get_vertices()[3] ),
                stroke_width = 7                                                  ,
                color        = LINE_COLOR                                         ,
            ).scale(1.1)
        )
        self.play(Create(line), opacity_vt.animate.set_value(RAIL_DIM))
        
        line_eq = MathTex("y", "=", "a", "x", "+", "b", color="#000000").shift([0, 2.5, 0])
        line_eq[2].set_color(LINE_COLOR)  # 2 -> a
        line_eq[5].set_color(LINE_COLOR)  # 5 -> b
        self.play(Write(line_eq))
        
        # --- ZOOM IN ON SCREWS ---
        ZOOM        = 4
        zoom_target = midpoint(screws[0].get_center(), screws[1].get_center())
        
        ax.add_updater(
            lambda m: m.shift( screws[0].get_center() - ax.get_origin() ),
            call_updater=True                                            ,
        )
        x_label.add_updater(lambda m: m.next_to(ax.x_axis.get_end(), RIGHT))
        y_label.add_updater(lambda m: m.next_to(ax.y_axis.get_end(), UP   ))
        
        self.play(
            posts      .animate.shift(-zoom_target).scale(ZOOM, about_point=ORIGIN),
            bottom_rail.animate.shift(-zoom_target).scale(ZOOM, about_point=ORIGIN),
            screws     .animate.shift(-zoom_target).scale(ZOOM, about_point=ORIGIN),
            run_time = 4                                                     ,
        )
        ax.clear_updaters()
        
        # --- DRAW VERTICAL ERRORS ---
        ERROR_COLOR = "#0BF4A6"
        
        arrow_y2 = Arrow(
            [screws[1].get_x(), ax.get_origin()[1], 0],
            screws[1].get_center()                    ,
            color       = ERROR_COLOR                 ,
            tip_style   = {"width":0.2, "height":1 }  ,
            buff        = 0                           ,
        )
        y2_eq = MathTex(r"y_2", color=ERROR_COLOR).next_to(arrow_y2, buff=0.05)
        self.play(Create(arrow_y2), Write(y2_eq))
        
        self.play( screws[0].animate.shift(0.75*DOWN) )
        arrow_y1 = Arrow(
            [screws[0].get_x(), ax.get_origin()[1], 0],
            screws[0].get_center()                    ,
            color       = ERROR_COLOR                 ,
            tip_style   = {"width":0.2, "height":1 }  ,
            buff        = 0                           ,
        )
        y1_eq = MathTex(r"y_1", color=ERROR_COLOR).next_to(arrow_y1, buff=0.05)
        self.play(Create(arrow_y1), Write(y1_eq))
        
        # --- 1st EQUATION ---
        screw1_eq = MathTex("y_1", "=", "a", r"\,0", "+", "b", color="#000000").shift([0, 2.5, 0])
        screw1_eq[0].set_color(ERROR_COLOR)  # 0 -> y1
        screw1_eq[2].set_color( LINE_COLOR)  # 2 -> a 
        screw1_eq[5].set_color( LINE_COLOR)  # 5 -> b 
        label1    =     Tex(r"1$^\text{o}$ parafuso:", color="#000000").next_to(screw1_eq, LEFT)
        self.play( 
            posts[1] .animate.set_opacity(0.5),
            screws[1].animate.set_opacity(0.5),
            arrow_y2 .animate.set_opacity(0.5),
            y2_eq    .animate.set_opacity(0.5),
            Write(label1)                     ,
            *(
                ReplacementTransform(src, dst) for src, dst in zip(line_eq, screw1_eq)
            )                                 ,
        )
        self.wait(2)
        
        # --- 2nd EQUATION ---
        arrow_x2 = Arrow(
            ax.get_origin()                            ,
            [screws[1].get_x(), ax.get_origin()[1], 0] ,
            color       = "#000000"                    ,
            tip_style   = {"width":0.24, "height":1.2 },
            buff        = 0                            ,
        )
        x2_eq = MathTex(r"d", color="#000000").next_to(arrow_x2, DOWN, buff=0.5)
        self.play( 
            Create(arrow_x2)                ,
            Write(x2_eq)                    ,
            posts[1] .animate.set_opacity(1),
            screws[1].animate.set_opacity(1),
            arrow_y2 .animate.set_opacity(1),
            y2_eq    .animate.set_opacity(1),
        )
        self.wait(0.5)
        
        screw2_eq = MathTex("y_2", "=", "a", r"\,d", "+", "b", color="#000000").next_to(screw1_eq, DOWN)
        screw2_eq[0].set_color(ERROR_COLOR)  # 0 -> y1
        screw2_eq[2].set_color( LINE_COLOR)  # 2 -> a 
        screw2_eq[5].set_color( LINE_COLOR)  # 5 -> b 
        label2    =     Tex(r"2$^\text{o}$ parafuso:", color="#000000").next_to(screw2_eq, LEFT)
        self.play(
            posts[0] .animate.set_opacity(0.5),
            screws[0].animate.set_opacity(0.5),
            arrow_y1 .animate.set_opacity(0.5),
            y1_eq    .animate.set_opacity(0.5),
            Write(label2)                     ,
            Write(screw2_eq)                  ,
        )
        self.wait(2)
        
        # --- SWAP EQUATION TERMS ---
        # [y, =, a, x, +, b] -> [x, a, +, b, =, y]: old part i lands on new part SWAP[i].
        SWAP = [5, 4, 1, 0, 2, 3]
        
        screw1_swap = MathTex("0", "a", "+", "b", "=", "y_1", color="#000000").next_to(label1, RIGHT)
        screw1_swap[5].set_color(ERROR_COLOR)  # 5 -> y1
        screw1_swap[1].set_color( LINE_COLOR)  # 1 -> a
        screw1_swap[3].set_color( LINE_COLOR)  # 3 -> b
        
        screw2_swap = MathTex("d", "a", "+", "b", "=", "y_2", color="#000000").next_to(label2, RIGHT)
        screw2_swap[5].set_color(ERROR_COLOR)  # 5 -> y2
        screw2_swap[1].set_color( LINE_COLOR)  # 1 -> a
        screw2_swap[3].set_color( LINE_COLOR)  # 3 -> b
        
        # Transform whole top-level groups: the OpenGL scene won't remove a lone submobject,
        # which is why `line_eq` (not `screw1_eq`) is what's still showing the 1st equation.
        screw1_shown = VGroup(*(screw1_swap[j] for j in SWAP))
        screw2_shown = VGroup(*(screw2_swap[j] for j in SWAP))
        self.play(
            posts[1] .animate.set_opacity(0.5),
            screws[1].animate.set_opacity(0.5),
            arrow_y2 .animate.set_opacity(0.5),
            y2_eq    .animate.set_opacity(0.5),
            FadeOut(label1)                   ,
            FadeOut(label2)                   ,
            ReplacementTransform(line_eq  , screw1_shown),
            ReplacementTransform(screw2_eq, screw2_shown),
            run_time = 2,
        )
        self.wait(2)
        
        # --- SUBSTITUTE FOR A MATRIX EQUATION ---
        MATRIX_H_BUFF = 0.8  # Column spacing (Matrix default: 1.3).

        # Row spacing equal to the old equations' line spacing, so each row lands on its line.
        old_eq_signs = VGroup(screw1_swap[4], screw2_swap[4])
        row_gap      = screw1_swap[4].get_y() - screw2_swap[4].get_y()

        coeffs   = Matrix([["0", "1"], ["d", "1"]], h_buff=MATRIX_H_BUFF, v_buff=row_gap)  # [0, 1, 2, 3] <=> [0, 1, d, 1]
        unknowns = Matrix([["a"], ["b"]]          ,                       v_buff=row_gap)
        eq_sign  = MathTex("=")
        rhs      = Matrix([["y_1"], ["y_2"]]      ,                       v_buff=row_gap)

        matrix_eq = VGroup(coeffs, unknowns, eq_sign, rhs).arrange(RIGHT, buff=SMALL_BUFF)
        matrix_eq.set_color("#000000")
        unknowns.get_entries().set_color( LINE_COLOR)
        rhs     .get_entries().set_color(ERROR_COLOR)
        # Put the new = right between the two old ones.
        matrix_eq.shift(old_eq_signs.get_center() - eq_sign.get_center())
        
        # The b-coefficients and the brackets have no counterpart in the old equations.
        new_parts = VGroup(
            coeffs.get_entries()[1], coeffs.get_entries()[3],
            *coeffs.get_brackets(), *unknowns.get_brackets(), *rhs.get_brackets(),
        )
        
        # Both equations' a, b and = merge into the single copy each has in `matrix_eq`.
        self.play(
            Transform(screw1_swap[0], coeffs  .get_entries()[0]),  # 0   -> 0
            Transform(screw2_swap[0], coeffs  .get_entries()[2]),  # d   -> d
            Transform(screw1_swap[1], unknowns.get_entries()[0]),  # a   -> a
            Transform(screw2_swap[1], unknowns.get_entries()[0]),  # a   -> a
            Transform(screw1_swap[3], unknowns.get_entries()[1]),  # b   -> b
            Transform(screw2_swap[3], unknowns.get_entries()[1]),  # b   -> b
            Transform(screw1_swap[4], eq_sign                  ),  # =   -> =
            Transform(screw2_swap[4], eq_sign                  ),  # =   -> =
            Transform(screw1_swap[5], rhs     .get_entries()[0]),  # y_1 -> y_1
            Transform(screw2_swap[5], rhs     .get_entries()[1]),  # y_2 -> y_2
            FadeOut(screw1_swap[2])                             ,  # +
            FadeOut(screw2_swap[2])                             ,  # +
            FadeIn(new_parts)                                   ,
            run_time = 2,
        )
        # Swap the morphed pieces for the real thing, again whole top-level groups only.
        self.remove(screw1_shown, screw2_shown, new_parts)
        self.add(matrix_eq)
        self.wait(2)
        
        # --- ZOOM BACK OUT TO THE WHOLE FENCE ---
        self.play(
            FadeOut(VGroup(ax, ax_labels, line, arrow_y1, y1_eq, arrow_y2, y2_eq, arrow_x2, x2_eq)),
        )
        self.play(
            posts      .animate.scale(1/ZOOM, about_point=ORIGIN).shift(zoom_target).set_opacity(1),
            bottom_rail.animate.scale(1/ZOOM, about_point=ORIGIN).shift(zoom_target).set_opacity(1),
            screws     .animate.scale(1/ZOOM, about_point=ORIGIN).shift(zoom_target).set_opacity(1),
            opacity_vt .animate.set_value(1)                                                       ,
            run_time = 4                                                                           ,
        )
        self.wait(2)
