# VÍDEO 1 - SISTEMAS MAL CONDICIONADOS
## INSTALANDO-SE UMA CERCA
A primeira etapa de se construir uma cerca é definir onde os dois mourões mestres serão instalados e correr uma linha entre esses dois pontos. Ela servirá de guia para a instalação dos mourões intermediários.

Se afobadamente instalarmos os mourões em série, sem antes configurar nossa guia, um pequeno desalinhamento entre os dois primeiros mourões pode impedir a instalação da travessa.

Crucialmente, o primeiro modo de se construir uma cerca, fixando os dois extremos primeiro, é robusto contra pequenas imprecisões de instalação, ao passo que o segundo, em que começamos por fixar os dois primeiros mourões, é muito sensível.

Nos problemas enfrentados nas exatas, esses dois comportamentos emergem. Um problema matemático cuja solução é pouco perturbada por imprecisões é dito **bem condicionado**, ao passo que um cuja solução muda completamente, mesmo quando os erros são pequenos, é dito **mal condicionado**.


## INEVITABILIDADE DOS ERROS
É importante frisar que em qualquer problema **real**, medições errôneas são inescapáveis.

A começar, todo instrumento de medição físico possui um grau de incerteza em suas leituras.

Mas, mesmo se tivéssemos um maquinário perfeito, que fizesse medições exatas, os computadores - os aparelhos que fazem nossas contas no contexto profissional - **sempre** cometem pequenos erros.

O motivo por trás disso é simples: um número real pode ter infinitos dígitos - como $\pi$, por exemplo -, mas a memória (a quantidade de bits) que um computador aloca para guardar cada número é, obviamente, finita. Portanto, mais cedo ou tarde, o computador terá que truncá-lo.

Da geometria, por exemplo, sabemos que a área de um círculo de raio de 4 cm é

$$
    \pi \cdot 4^2\;\text{cm}^2.
$$

Logo, por menor que seja, sempre cometeremos um erro calculando essa área no computador.

Com isso em mente, fica claro que, quando resolvendo um problema, seu condicionamento **sempre** será um ponto importante de consideração. Se ele for **mal** condicionado - dada a inevitabilidade dos erros - mesmo se fizermos todos os cálculos devidos, ainda é inteiramente possível que nossos resultados não sejam confiáveis!


## SISTEMAS LINEARES
Um problema clássico da matemática, com muitas aplicações úteis, é a resolução de sistemas lineares.

### ALGUMAS APLICAÇÕES
Serve

1. na produção de exames de imagem no contexto médico,
2. na determinação do carregamento de estruturas da construção civil,
3. na animação de artefatos 3D em videogames.

Dentre várias outras coisas...

Em seu caso mais simples, resolver um sistema linear é nada mais do que determinar o ponto de interseção entre duas retas no plano, de forma sistemática.

### PLANO CARTESIANO
A começar, note que qualquer ponto no plano pode ser identificado por um par de números reais
$[ x \quad y ]^\top$
Onde $x$ representa sua distância horizontal de um ponto de referência e $y$ a vertical.

Vale frisar que usamos aqui a distância **com sinal**, ou seja, se $x$ for negativo, significa que o ponto está **à esquerda** da origem, ao passo que, se $y$ for negativo, significa que o ponto está **abaixo** da origem.

### 1 EQUAÇÃO LINEAR
O emprego desses dois números $x$ e $y$ agora permite-nos estabelecer relações entre figuras geométricas e equações algébricas - a chamada *Geometria Analítica*.

Por exemplo, o conjunto de todos pares $(x,y)$ tais que $x=3$ nada mais é do que uma reta vertical 3 unidades à direita de nossa origem.

Que figura nos fornece a equação $y=4$? ...a reta vertical 4 unidades acima de nossa origem.

Uma **equação linear**, por sua vez, é uma da forma
$$
    a\cdot x + b\cdot y = c.
$$
Por exemplo,
$$
    2\cdot x - 1\cdot y = 3.
$$
Os pares $(x,y)$ da reta que satisfazem essa equação formam uma **reta**.

Se mudarmos os valores de $a$ e $b$, mudamos a angulação da reta. Se mudamos o valor de $c$, transladamo-na.


### 2 EQUAÇÕES LINEARES
Por conseguinte, determinar o ponto de interseção destas duas retas significa encontrar o par (ou pares)
$[ x \quad y ]^\top$
que satisfaz(em) simultaneamente as equações

$$
    \begin{cases}
        a_{11}x + a_{12}y = b_1 \\
        a_{21}x + a_{22}y = b_2
    \end{cases}.
$$

Ou, expresso em notação matricial,

$$
    \begin{bmatrix}
        a_{11} & a_{12} \\
        a_{21} & a_{22}
    \end{bmatrix}
    \begin{bmatrix}
        x \\
        y
    \end{bmatrix}
    =
    \begin{bmatrix}
        b_1 \\
        b_2
    \end{bmatrix}.
$$

Ou finalmente, de forma ainda mais enxuta, $A\mathbf{x} = \mathbf{b}$.

Para de fato resolver o sistema linear, há uma gama ampla de estratégias que poderíamos adotar.
* Poderíamos isolar uma das incógnitas na equação de cima e substituir na de baixo, por exemplo;
* aplicar _eliminação de Gauss_;
* a regra de Cramer...

enfim, nos preocuparemos aqui muito mais em estudar o **condicionamento** dos sistemas lineares do que encontrar soluções particulares.


## CONDICIONAMENTO DE SISTEMAS LINEARES
Alguns sistemas lineares são bem condicionados, ao passo que outros são mal condicionados...

> TOCAR ANIMAÇÃO CHAVE (CASO 2D)

...para esse sistema em particular, em que as retas são perpendiculares, se errarmos um pouco no desenho de uma, vemos que a diferença entre a solução real e a alterada é bem proporcional ao tamanho do erro.

Já se considerarmos retas bem mais paralelas, vemos que para um mesmo erro, a variação na solução é muito violenta.

Recapitulando: o condicionamento é uma propriedade intrínseca de cada _sistema_ e, portanto, a acurácia de nossas respostas não depende apenas do quão refinado é o sistema de pontos flutuantes que temos a disposição. O problema _em si_ que nos propomos a resolver também afeta a acurácia de nossa resposta. Alguns problemas são mais difíceis de se responder do que outros!

## SISTEMAS TRIDIMENSIONAIS
Naturalmente, sistemas lineares se estendem para o caso tridimensional também. Agora, ao invés de buscarmos o ponto de interseção de duas retas, buscamos o ponto de interseção de **três planos**.

> EXPLICAR EQUIVALÊNCIA ENTRE EQUAÇÃO ALGÉBRICA $a_1x + a_2y + a_3z = b$ E PLANO GEOMÉTRICO

...o que nos leva ao equacionamento

$$
    \begin{cases}
        a_{11}x + a_{12}y + a_{13}z = b_1 \\
        a_{21}x + a_{22}y + a_{23}z = b_2 \\
        a_{31}x + a_{32}y + a_{33}z = b_3
    \end{cases}.
$$

Ou, expresso em notação matricial,

$$
    \begin{bmatrix}
        a_{11} & a_{12} & a_{13} \\
        a_{21} & a_{22} & a_{23} \\
        a_{31} & a_{32} & a_{33}
    \end{bmatrix}
    \begin{bmatrix}
        x \\
        y \\
        z
    \end{bmatrix}
    =
    \begin{bmatrix}
        b_1 \\
        b_2 \\
        b_3
    \end{bmatrix}.
$$

Ou finalmente, a forma mais enxuta coincide com a bidimensional, $A\mathbf{x} = \mathbf{b}$.

## CONDICIONAMENTO DE SISTEMAS TRIDIMENSIONAIS
Agora, da perspectiva geométrica, observamos que o sistema é bem condicionado se os planos são próximos de ortogonais, ao passo que, quanto mais próximos de paralelos, pior fica.

> TOCAR ANIMAÇÃO CHAVE (CASO 3D)

## SISTEMAS ARBITRÁRIOS - NÚMERO DE CONDICIONAMENTO
Em muitos contextos, tratamos de sistemas lineares muito maiores, envolvendo 4, 5, 10, 100 ou até milhares de incógnitas ao invés de apenas 2 ou 3. Mas claro, não possuímos visão quadridimensional, quinquedimensional e muito menos visão em 1.000 dimensões.

Como avaliamos o condicionamento de sistemas lineares nesses casos?

Agora, com a geometria fora de jogo, voltamo-nos à álgebra. Recorremos a seu **número de condicionamento** $\kappa$ da matriz. Um único valor que resumo o condicionamento do (possivelmente) massivo sistema linear.

Se $\kappa$ for pequeno, indica bom condicionamento e, se grande, mau condicionamento.

Mas, como tomamos posse desse número, exatamente? Que conta fazemos para computá-lo?

Formalmente, temos que

$$
    \kappa
    \coloneqq
    \lVert A \rVert \cdot \lVert A^{-1}\rVert
$$

Aqui, os delimitadores de duplo traço indicam as **normas** das matrizes $A$ e $A^{-1}$. Para vetores de $\mathbb{R}^n$, a definição de norma é direta. Temos que (assumindo-se a métrica euclidiana)

$$
    \lVert \mathbf{x} \rVert_2
    \coloneqq
    \sqrt{x_1^2 + x_2^2 + \ldots + x_n^2}
$$

Para matrizes, a definição é um pouco mais sutil...
> EXPLICAR NORMA EUCLIDIANA DE MATRIZ ALIADO AS ANIMAÇÕES:

* > ELIPSE DOS VALORES SINGULARES (2D)
* > ELIPSÓIDE DOS VALORES SINGULARES (3D)