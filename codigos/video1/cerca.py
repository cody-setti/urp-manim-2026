from manim import *
from manim.opengl import *

class Cerca(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # --- POSTES ---
        # Cilindros apontam ao eixo z por padrão (OUT nas coordenadas do Manim).
        poste_altura    = 3.0
        poste_raio      = 0.2
        cor_poste       = "#EB9A6B"
        cor_bases       = "#D08050"
        
        poste1 = Cylinder(
            radius              = poste_raio           ,
            height              = poste_altura         ,
            checkerboard_colors = [cor_poste,cor_poste],
            stroke_width        = 0                    ,
            show_ends           = True                 ,
        )
        poste1[-1].set_style(fill_color=cor_bases, fill_opacity=1, stroke_width = 0,)
        poste1[-2].set_style(fill_color=cor_bases, fill_opacity=1, stroke_width = 0,)
        poste1.shift(LEFT * 2)
        
        poste2 = Cylinder(
            radius              = poste_raio,
            height              = poste_altura,
            checkerboard_colors = [cor_poste,cor_poste],
            stroke_width        = 0,
            show_ends           = True,
        )
        poste2[-1].set_style(fill_color=cor_bases, fill_opacity=1, stroke_width = 0,)
        poste2[-2].set_style(fill_color=cor_bases, fill_opacity=1, stroke_width = 0,)
        poste2.shift(RIGHT * 2)
        
        # --- BARROTES ---
        cor_barrote       = "#A0522D"
        barrote_espessura = 0.1
        desvio            = poste_raio + (barrote_espessura / 2)# = 0.25
        
        # Começamos com um cubo 1x1x1, que deformamos.
        # Fatores de escala: [X (comprimento), Y (largura), Z (altura)]
        barrote_sup = Cube(side_length=1, fill_color=cor_barrote, fill_opacity=1)
        barrote_sup.scale([4.4, 0.1, 0.3])
        barrote_sup.shift(OUT  * 0.8   )
        barrote_sup.shift(DOWN * desvio)
        
        barrote_inf = Cube(side_length=1, fill_color=cor_barrote, fill_opacity=1)
        barrote_inf.scale([4.4, 0.1, 0.3])
        barrote_inf.shift(IN   * 0.8   )
        barrote_inf.shift(DOWN * desvio)
        
        # --- CERCA ---
        cerca = VGroup(poste1, poste2, barrote_sup, barrote_inf)

        ## --- SOLO ---
        #nivel_chao = IN * (poste_altura / 2)# = -1.5*e3
        #solo = Square(
        #    side_length  = 10       ,
        #    fill_color   = "#5E8C6A",
        #    fill_opacity = 1        ,
        #    stroke_width = 0        ,
        #)
        
        # --- ANIMAÇÕES ---
        self.play(
            #FadeIn(solo,   shift=UP ),
            FadeIn(poste1, shift=OUT),
            FadeIn(poste2, shift=OUT),
            run_time=0.5
        )
        self.play(
            FadeIn(barrote_sup, shift=LEFT ),
            FadeIn(barrote_inf, shift=RIGHT),
            run_time=1
        )
        
        self.move_camera(theta=45 * DEGREES, run_time=4)
        self.wait()
