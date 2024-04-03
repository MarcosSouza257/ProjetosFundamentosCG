/* Hello Triangle - c�digo adaptado de https://learnopengl.com/#!Getting-started/Hello-Triangle 
 *
 * Adaptado por Rossana Baptista Queiroz
 * para a disciplina de Processamento Gr�fico - Unisinos
 * Vers�o inicial: 7/4/2017
 * �ltima atualiza��o em 14/08/2023
 *
 */

#include <iostream>
#include <string>
#include <assert.h>

using namespace std;

// Titulo do Exercicio
char title_window[] = "Ex. 9. Desenhando uma casa";

//Classe para manipula��o dos shaders
#include "Shader.h"

// Prot�tipo da fun��o de callback de teclado
void key_callback(GLFWwindow* window, int key, int scancode, int action, int mode);

// Prot�tipos das fun��es
int setupGeometry();

// Dimens�es da janela (pode ser alterado em tempo de execu��o)
const GLuint WIDTH = 800, HEIGHT = 600;

// Fun��o MAIN
int main()
{
	// Inicializa��o da GLFW
	glfwInit();

	// Cria��o da janela GLFW
	GLFWwindow* window = glfwCreateWindow(WIDTH, HEIGHT, title_window, nullptr, nullptr);
	glfwMakeContextCurrent(window);

	// Fazendo o registro da fun��o de callback para a janela GLFW
	glfwSetKeyCallback(window, key_callback);

	// GLAD: carrega todos os ponteiros d fun��es da OpenGL
	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
	{
		std::cout << "Failed to initialize GLAD" << std::endl;

	}

	// Obtendo as informa��es de vers�o
	const GLubyte* renderer = glGetString(GL_RENDERER); /* get renderer string */
	const GLubyte* version = glGetString(GL_VERSION); /* version as a string */
	cout << "Renderer: " << renderer << endl;
	cout << "OpenGL version supported " << version << endl;

	// Definindo as dimens�es da viewport com as mesmas dimens�es da janela da aplica��o
	int width, height;
	glfwGetFramebufferSize(window, &width, &height);
	glViewport(0, 0, width, height);


	// Compilando e buildando o programa de shader
	Shader shader("../shaders/helloTriangle.vs", "../shaders/helloTriangle.fs");

	// Gerando um buffer simples, com a geometria de um tri�ngulo
	GLuint VAO = setupGeometry();
	
	// Enviando a cor desejada (vec4) para o fragment shader
	// Utilizamos a vari�veis do tipo uniform em GLSL para armazenar esse tipo de info
	// que n�o est� nos buffers
	GLint colorLoc = glGetUniformLocation(shader.ID, "inputColor");
	
	shader.Use();
	
	// Loop da aplica��o - "game loop"
	while (!glfwWindowShouldClose(window))
	{
		// Checa se houveram eventos de input (key pressed, mouse moved etc.) e chama as fun��es de callback correspondentes
		glfwPollEvents();

		// Limpa o buffer de cor
		glClearColor(1.0f, 1.0f, 1.0f, 1.0f); //cor de fundo
		glClear(GL_COLOR_BUFFER_BIT);

		glLineWidth(10);
		glPointSize(20);

		glBindVertexArray(VAO); //Conectando ao buffer de geometria


		glUniform4f(colorLoc, 1.0f, 0.5f, 0.0f, 1.0f); // Linha Ch�o
		glDrawArrays(GL_LINES, 0, 2);

		glUniform4f(colorLoc, 0.0f, 0.0f, 0.0f, 1.0f); // Casa
		glDrawArrays(GL_LINE_STRIP, 2, 4);

		glUniform4f(colorLoc, 1.0f, 0.0f, 0.0f, 1.0f); // Telhado
		glDrawArrays(GL_TRIANGLES, 6, 3);
		
		glUniform4f(colorLoc, 0.0f, 0.0f, 0.0f, 1.0f); // Telhado linha
		glDrawArrays(GL_LINE_LOOP, 6, 3);

		glUniform4f(colorLoc, 0.7f, 0.16f, 0.16f, 1.0f); // Porta
		glDrawArrays(GL_TRIANGLE_FAN, 9, 4);

		glUniform4f(colorLoc, 0.0f, 0.0f, 0.0f, 1.0f); // Porta Linha
		glDrawArrays(GL_LINE_STRIP, 9, 4);

		glUniform4f(colorLoc, 1.0f, 1.0f, 0.0f, 1.0f); // Janela
		glDrawArrays(GL_TRIANGLE_FAN, 13, 4);

		glUniform4f(colorLoc, 0.0f, 0.0f, 0.0f, 1.0f); // Janela Linha
		glDrawArrays(GL_LINE_LOOP, 13, 11);

		glBindVertexArray(0); //Desconectando o buffer de geometria

		// Troca os buffers da tela
		glfwSwapBuffers(window);
	}
	// Pede pra OpenGL desalocar os buffers
	glDeleteVertexArrays(1, &VAO);
	// Finaliza a execu��o da GLFW, limpando os recursos alocados por ela
	glfwTerminate();
	return 0;
}

// Fun��o de callback de teclado - s� pode ter uma inst�ncia (deve ser est�tica se
// estiver dentro de uma classe) - � chamada sempre que uma tecla for pressionada
// ou solta via GLFW
void key_callback(GLFWwindow* window, int key, int scancode, int action, int mode)
{
	if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
		glfwSetWindowShouldClose(window, GL_TRUE);
}

// Esta fun��o est� bastante harcoded - objetivo � criar os buffers que armazenam a 
// geometria de um tri�ngulo
// Apenas atributo coordenada nos v�rtices
// 1 VBO com as coordenadas, VAO com apenas 1 ponteiro para atributo
// A fun��o retorna o identificador do VAO
int setupGeometry()
{
	GLfloat vertices[] = {
		// Ch�o
		-0.60, -0.6, 0.0,
		0.60, -0.6, 0.0,
		// Casa
		-0.35, -0.6, 0.0,
		-0.35, 0.3, 0.0,
		0.35, 0.3, 0.0,
		0.35, -0.6, 0.0,
		//Triangulo Telhado
		-0.35, 0.3, 0.0,
		0.0, 0.7, 0.0, 
		0.35, 0.3, 0.0, 
		// Porta
		-0.12, -0.6, 0.0,
		-0.12, -0.2, 0.0,
		0.12, -0.2, 0.0, 
		0.12, -0.6, 0.0,
		// Janela
		0.0, -0.1, 0.0,
		0.0, 0.1, 0.0,
		-0.2, 0.1, 0.0,
		-0.2, -0.1, 0.0,
		0.0, -0.1, 0.0,
		0.0, 0.0, 0.0,
		-0.2, 0.0, 0.0,
		-0.2, -0.1, 0.0,
		-0.1, -0.1, 0.0,
		-0.1, 0.1, 0.0,
		0.0, 0.1, 0.0,

};

	GLuint VAO, VBO;
	glGenVertexArrays(1, &VAO);
	glGenBuffers(1, &VBO);

	glBindVertexArray(VAO);

	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), (GLvoid*)0);
	glEnableVertexAttribArray(0);

	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindVertexArray(0);

	return VAO;
}

