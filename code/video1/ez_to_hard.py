from manim import *

for cls in (Text, MarkupText, Paragraph, Tex, MathTex, SingleStringMathTex):
    cls.set_default(color=BLACK)

class EzToHard(Scene):
    def construct(self):
        
        # --- EQUATIONS ---
        # Ax = b
        equation1 = MathTex(
            r"A\mathbf{x}",  # 0 (ANCHOR)
            r"="          ,  # 1
            r"\mathbf{b}" ,  # 2
        )
        
        # Ax - b = 0
        equation2 = MathTex(
            r"A\mathbf{x}",  # 0 (ANCHOR)
            r"-"          ,  # 1
            r"\mathbf{b}" ,  # 2
            r"="          ,  # 3
            r"\mathbf{0}" ,  # 4
        )
        
        # arg min ‖Ax - b‖² + γ‖x‖² + λ‖x‖₁
        equation3 = MathTex(
            r"\operatorname*{\arg\min}_{\mathbf{x} \in \mathbb{R}^{^n}}",  # 0
            r"\|"                                                       ,  # 1
            r"A\mathbf{x}"                                              ,  # 2 (ANCHOR)
            r"- \mathbf{b}"                                             ,  # 3
            r"\|_{_2}^{^2}"                                             ,  # 4
            r"+ \gamma\|\mathbf{x}\|_{_2}^{^2}"                         ,  # 5
            r"+ \lambda\|\mathbf{x}\|_{_1}"                             ,  # 6
        )
        
        # --- ALIGN EQUATIONS BY COMMON `Ax` TERM ---
        equation1.shift( equation3[2].get_center() - equation1[0].get_center() )
        equation2.shift( equation3[2].get_center() - equation2[0].get_center() )
        
        # --- ANIMATIONS ---
        # Ax = b
        self.play(Write(equation1))
        self.wait(1)
        
        # Ax - b = 0
        #                              ┌────── default path ──────┐ ┌─────────── hop ───────────┐
        def hop(start, end, t): return  interpolate(start, end, t) + 0.5 * (4 * t * (1 - t)) * UP
        self.play(
            ReplacementTransform(equation1[2], equation2[2], path_func=hop),  # `b` hops over (vertically) the shifting `=` sign.
            ReplacementTransform(equation1[1], equation2[3]),                 # `=` sign shifts to the right.
            FadeIn(equation2[1]),                                             # `-` symbol fades in.
            FadeIn(equation2[4], shift=0.3 * RIGHT),                          # `0` fades in from the left.
        )
        self.remove(equation1)
        self.add(equation2)
        self.wait(1)
        
        # LEAST SQUARES
        self.play(
            FadeOut(equation2[3:]),
            Write(equation3[0:2]) ,
            Write(equation3[4])   ,
        )
        self.wait(1)
        
        # TIKHONOV
        self.play(Write(equation3[5]))
        self.wait(1)
        
        # ELASTIC NET
        self.play(Write(equation3[6]))
        self.wait(1)
        
        #                 Ax - b        , arg min ‖     , ‖ + γ‖x‖² + λ‖x‖₁
        self.play(FadeOut(equation2[0:3], equation3[0:2], equation3[4:]))
        self.wait(1)
