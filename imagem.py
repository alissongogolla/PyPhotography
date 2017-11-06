# coding=utf-8
import numpy as np, random, time, pprint
from PIL import Image


def criarImagem(nomeimagem):
    dX, dY = 5000, 5000

    """
	linspace(start, stop, num=50, endpoint=True, retstep=False)	
		A função linspace cria uma seqüência de números uniformemente espaçados entre os limites dados, opcionalmente incluindo o valor final (por default, esse é o comportamento). Esta função vai devolver um arranjo unidimensional que pode ser usado em qualquer operação que exija arranjos.
		start
		Este argumento indica o limite inicial do intervalo sobre o qual se deseja o arranjo.
		stop
		Este argumento indica o limite final do intervalo sobre o qual se deseja o arranjo.
		num
		Este argumento indica o número de pontos que o intervalo deve conter, ou seja, o comprimento do arranjo resultante. Esse número inclui os pontos que representam os limites do intervalo, exceto se o argumento endpoint for especificado como False (veja abaixo).
		endpoint
		Por default, o arranjo retornado contém o limite final do intervalo. Caso se deseje modificar esse comportamento, basta fazer este argumento igual a False. Neste caso, o limite final não é incluído.
		retstep
		Se este argumento for verdadeiro, o valor retornado é uma tupla em que o primeiro elemento é o arranjo construído, e o segundo elemento é o tamanho do intervalo, que, se endpoint for False, pode ser calculado pela fórmula:
	"""

    """
	reshape() para transformar o vetor de uma dimensão que contém as raízes em uma matriz-coluna com duas linhas. Fazemos isso para aproveitarmos a habilidade de broadcasting do NumPy. Note também que convertemos o resultado para uma matriz, para que possamos utilizar as operações de álgebra de matrizes que o NumPy tem disponíve
	"""

    xArray = np.linspace(0.0, 1.0, dX).reshape((1, dX, 1))
    yArray = np.linspace(0.0, 1.0, dY).reshape((dY, 1, 1))

    def randColor():
        return np.array([random.random(), random.random(), random.random()]).reshape((1, 1, 3))

    def getX(): return xArray

    def getY(): return yArray

    def safeDivide(a, b):
        return np.divide(a, np.maximum(b, 0.001))

    functions = [(0, randColor),
                 (0, getX),
                 (0, getY),
                 (1, np.sin),
                 (1, np.cos),
                 (2, np.add),
                 (2, np.subtract),
                 (2, np.multiply),
                 (2, safeDivide)]
    depthMin = 2
    depthMax = 10

    # Função recursiva para geração da imagem
    def buildImg(depth=0):
        funcs = [f for f in functions if
                 (f[0] > 0 and depth < depthMax) or
                 (f[0] == 0 and depth >= depthMin)]
        nArgs, func = random.choice(funcs)
        args = [buildImg(depth + 1) for n in range(nArgs)]
        return func(*args)

    img = buildImg()
    #pp = pprint.PrettyPrinter()
    #pp.pprint(img)

    # Verifica as dimensões da imagem estão corretas, dX por dY por 3
    img = np.tile(img, (dX / img.shape[0], dY / img.shape[1], 3 / img.shape[2]))

    # Converte para 8-bits e salva a imagem
    img8Bit = np.uint8(np.rint(img.clip(0.1, 1.0) * 255.0))
    Image.fromarray(img8Bit).save(nomeimagem)


ini = time.time()
for numero in range(0, 500, 1):
    criarImagem("ImagemSaida" + str(numero) + ".jpg")
fim = time.time()
print "Tempo execução: ", fim - ini
