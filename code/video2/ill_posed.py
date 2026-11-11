from manim import *
from manim.mobject.opengl.opengl_geometry import OpenGLArrow

class IllPosed(Scene):
    def construct(self):
        # --- PLOT WELL CONDITIONED SYSTEM ---
        line1 = FunctionGraph(
            lambda x: 0             ,
            stroke_width = 6        ,
            color        = "#6E61FF",
        )
        
        line2 = FunctionGraph(
            lambda x: -8*x          ,
            x_range = [-0.6, 0.6]   ,  # Just long enough to cross the frame
                                       # so that `Create()` works nicely.
            stroke_width = 6        ,
            color        = "#09C86C",
        )
        
        solution = Dot(
            point  = ORIGIN   ,
            radius = 0.15     ,
            color  = "#FFA475",
        )
        
        self.play( Create(line1)    )
        self.play( Create(line2)    )
        self.play( FadeIn(solution) )
        line2.scale(4)
        # A straight line's normal is numerically ±OUT at random; if it flips
        # between the start and end of a Transform, it's interpolated through 0
        # and the OpenGL "flat stroke" shader thins the line to nothing.
        line2.set_flat_stroke(False)
        
        
        # --- PERTURB SYSTEM ---
        line1_ref    =    line1.copy().set_opacity(0.3)
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
        
        PERT_X     = -3
        PERT_COLOR = "#F0D000"
        pert = OpenGLArrow(
            [PERT_X, line1_ref.get_y(), 0],
            [PERT_X, line1    .get_y(), 0],
            buff       = 0                ,
            thickness  = 0.06             ,
            fill_color = PERT_COLOR       ,
        )
        pert.add_updater(
            lambda mob: mob.put_start_and_end_on(
                [PERT_X, line1_ref.get_y(), 0],
                [PERT_X, line1    .get_y(), 0],
            )
        )
        self.add(pert)
        
        pert_label = MathTex(r"\mathbf{\epsilon}", color = PERT_COLOR)
        pert_label.add_updater(
            lambda mob: mob.next_to(
                [PERT_X, (line1_ref.get_y() + line1.get_y()) / 2, 0],
                RIGHT,
            )
        )
        
        self.play( line1.animate.shift(1.5*DOWN), Write(pert_label) )
        
        ERROR_COLOR = "#F4320B"
        error = OpenGLArrow(
            solution_ref.get_center(),
            solution    .get_center(),
            buff       = 0           ,
            thickness  = 0.07        ,
            fill_color = ERROR_COLOR ,
        )
        error_label = MathTex(r"\mathbf{e}", color = ERROR_COLOR)

        def place_error_label(mob):
            start, end = solution_ref.get_center(), solution.get_center()
            d = end - start
            normal = np.array([-d[1], d[0], 0])
            norm   = np.linalg.norm(normal)
            normal = normal / norm if norm > 1e-6 else RIGHT
            mob.next_to(0.5*(start + end), normal, buff = 0.2)

        error_label.add_updater(place_error_label)
        
        self.play( GrowArrow(error), Write(error_label) )
        
        error.add_updater(
            lambda mob: mob.put_start_and_end_on(
                solution_ref.get_center(),
                solution    .get_center(),
            )
        )
        
        self.play( Rotate(line2, 0.37 * PI, about_point = ORIGIN), run_time = 1.5 )
        self.wait(1)
