from manim import *

class mal_posto(Scene):
    def construct(self):

       ## customizar a fonte do texto
       #Tex.set_default(    tex_template = TexFontTemplates.palatino)
       #MathTex.set_default(tex_template = TexFontTemplates.palatino)

    
        # --- DESENHAR SISTEMA BEM POSTO ---
        linha1 = FunctionGraph(
                lambda x: -3 * x,
                color        = BLUE,
                stroke_width = 6,
        ).set_z_index(1)
        self.play(Create(linha1))

        linha2 = FunctionGraph(
                lambda x: (1/3) * x,
                color        = GREEN,
                stroke_width = 6,
        ).set_z_index(1)
        self.play(Create(linha2))

        solucao = Dot(color=PURPLE, radius=0.17).set_z_index(2)
        self.play(Create(solucao))
        self.wait(0.5)


        # --- PERTURBAR SISTEMA ---
        linha1_ref = linha1.copy().set_opacity(0.3).set_z_index(1)
        solucao_ref = solucao.copy().set_opacity(0.5).set_z_index(2)
        self.add(linha1_ref, solucao_ref)

        solucao.add_updater(
                lambda mob: mob.move_to(
                    line_intersection(
                        (linha1.get_start(), linha1.get_end()),
                        (linha2.get_start(), linha2.get_end())
                    )
                )
        )

        pert = RIGHT
        ancora = np.array([-1.,3.,0.])  # ponto da linha1 no topo da tela
        pert_flecha = Arrow(
                ancora,
                ancora + pert,
                buff = 0.0,
                color = YELLOW,
        ).set_z_index(-1)
        self.play(
                linha1.animate.shift(pert),
                GrowArrow(pert_flecha),
        )

        erro = Arrow(
                stroke_width = 6.5,
                color        = RED,
        ).set_z_index(3)
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
