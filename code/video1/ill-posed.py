from manim import *

class IllPosed(Scene):
    def construct(self):
        
        ## Customize text font.
        #Tex.set_default(    tex_template = TexFontTemplates.palatino)
        #MathTex.set_default(tex_template = TexFontTemplates.palatino)
        
        
        # --- DRAW WELL POSED SYSTEM ---
        line1 = FunctionGraph(
            lambda x: 0,
            color        = BLUE,
            stroke_width = 6,
            z_index      = 1,
        )
        self.play(Create(line1))
        
        line2 = FunctionGraph(
            lambda x: 8 * x,
            x_range      = [-0.6,0.6],  # Limits drawing to visible area.
            color        = GREEN,
            stroke_width = 6,
            z_index      = 1,
        )
        self.play(Create(line2))
        line2.scale(4) # Silently increases the line for subsequent rotation.
        
        solution = Dot(color=PURPLE, radius=0.17, z_index=2)
        self.play(Create(solution))
        self.wait(0.5)
        
        
        # --- PERTURB SYSTEM ---
        line1_ref = line1.copy().set_opacity(0.3)
        solution_ref = solution.copy().set_opacity(0.5)
        self.add(line1_ref, solution_ref)
        
        solution.add_updater(
            lambda mob: mob.move_to(
                line_intersection(
                    (line1.get_start(), line1.get_end()),
                    (line2.get_start(), line2.get_end())
                )
            )
        )
        
        pert = DOWN
        ancor = np.array([5.,0.,0.])
        pert_arrow = DashedLine(
            ancor,
            ancor + pert,
            dash_length  = 0.05,
            dashed_ratio = 0.5,
            color        = YELLOW,
            z_index      = -1,
        ).add_tip()
        pert_label = MathTex(r"\delta", color=YELLOW).next_to(pert_arrow, RIGHT)
        self.play(
            line1.animate.shift(pert),
            Create(pert_arrow),
            FadeIn(pert_label),
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
        error_label = always_redraw(
            lambda: MathTex("e", color=RED).next_to(error.get_center(), UP, buff=0.15)
        )
        self.play(
            FadeIn(error),
            FadeIn(error_label),
        )
        self.wait()
        
        
        # --- MALEFICIAR SISTEMA ---
        self.play(Rotate(line2,-PI/2 + 0.3), run_time=4)
        self.wait(2)
