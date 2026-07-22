from manim import *

class mal_posto(Scene):
    def construct(self):

       ## Customizar a fonte do texto.
       #Tex.set_default(    tex_template = TexFontTemplates.palatino)
       #MathTex.set_default(tex_template = TexFontTemplates.palatino)

    
        # --- DESENHAR SISTEMA BEM POSTO ---
        linha1 = FunctionGraph(
                lambda x: 0,
                color        = BLUE,
                stroke_width = 6,
                z_index      = 1,
        )
        self.play(Create(linha1))

        linha2 = FunctionGraph(
                lambda x: 8 * x,
                x_range      = [-0.6,0.6],  # Limita desenho à área visível.
                color        = GREEN,
                stroke_width = 6,
                z_index      = 1,
        )
        self.play(Create(linha2))
        linha2.scale(4) # Silenciosamente aumenta a reta para a subsequente rotação.

        solucao = Dot(color=PURPLE, radius=0.17, z_index=2)
        self.play(Create(solucao))
        self.wait(0.5)


        # --- PERTURBAR SISTEMA ---
        linha1_ref = linha1.copy().set_opacity(0.3)
        solucao_ref = solucao.copy().set_opacity(0.5)
        self.add(linha1_ref, solucao_ref)

        solucao.add_updater(
                lambda mob: mob.move_to(
                    line_intersection(
                        (linha1.get_start(), linha1.get_end()),
                        (linha2.get_start(), linha2.get_end())
                    )
                )
        )

        pert = DOWN
        ancora = np.array([5.,0.,0.])
        pert_flecha = Arrow(
                ancora,
                ancora + pert,
                buff    = 0.0,
                color   = YELLOW,
                z_index = -1,
        )
        self.play(
                linha1.animate.shift(pert),
                GrowArrow(pert_flecha),
        )

        erro = Arrow(
                stroke_width = 6.5,
                max_stroke_width_to_length_ratio = 7,
                color        = RED,
                z_index      = 3,
        )
        erro.add_updater(
                lambda line: line.put_start_and_end_on(ORIGIN,solucao.get_center())
        )
        self.play(
                FadeIn(erro),
        )
        self.wait()


        # --- MALEFICIAR SISTEMA ---
        self.play(Rotate(linha2,-PI/2 + 0.3), run_time=4)
        self.wait(2)
