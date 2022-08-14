from tkinter import *
import pymysql
from tkinter import messagebox, ttk


class AdminJanela():

    def CadastrarProduto(self):  #agora foi criado uma janela com a cor de fundo cinza
        self.cadastrar = Tk()
        self.cadastrar.title('Cadastro de Produtos')
        self.cadastrar['bg'] ='#524f4f'
        Label(self.cadastrar,text='Cadastrar os produtos',bg='#524f4f',fg='white').grid(row=0, column=0, columnspan=5, padx=5,pady=5) #bg muda cor do fundo e fg muda cor da letra


        Label(self.cadastrar, text='Nome',bg='#524f4f', fg='white').grid(row=1,column=0,columnspan=1,pady=5,padx=5)
        self.nome = Entry(self.cadastrar)
        self.nome.grid(row=1,column=1,columnspan=2,padx=5,pady=5)

        Label(self.cadastrar, text='Ingredientes',bg='#524f4f', fg='white').grid(row=2,column=0,columnspan=1,pady=5,padx=5)
        self.ingredientes = Entry(self.cadastrar)
        self.ingredientes.grid(row=2,column=1,columnspan=2,padx=5,pady=5)

        Label(self.cadastrar, text='Grupo',bg='#524f4f', fg='white').grid(row=3,column=0,columnspan=1,pady=5,padx=5)
        self.grupo = Entry(self.cadastrar)
        self.grupo.grid(row=3,column=1,columnspan=2,padx=5,pady=5)

        Label(self.cadastrar, text='Preço', bg='#524f4f', fg='white').grid(row=4, column=0, columnspan=1, pady=5,padx=5)
        self.preco = Entry(self.cadastrar)   #colocando os campos da janela cadastros
        self.preco.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        Button(self.cadastrar, text='Cadastrar', width=15, bg='gray', relief='flat', highlightbackground='#524f4f', command=self.CadastrarProdutoBackEnd).grid(row=5,column=0,padx=5,pady=5)
        Button(self.cadastrar, text='Excluir', width=15, bg='gray', relief='flat', highlightbackground='#524f4f', command=self.RemoverCadastrosBackEnd).grid(row=5,column=1,padx=5,pady=5)
        Button(self.cadastrar, text='Atualizar', width=15, bg='gray', relief='flat', highlightbackground='#524f4f', command=self.CadastrarProdutoBackEnd).grid(row=6,column=0,padx=5,pady=5)
        Button(self.cadastrar, text='Limpar Produtos', width=15, bg='gray', relief='flat', highlightbackground='#524f4f', command=self.LimparCadastrosBackEnd).grid(row=6,column=1,padx=5,pady=5)


        self.tree = ttk.Treeview(self.cadastrar,selectmode= 'browse', columns=("column1","column2","column3","column4"),show='headings')
        self.tree.column("column1",width=200, minwidth=500, stretch=NO)
        self.tree.heading('#1',text='Nome')
        self.tree.column("column2", width=400, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Ingredientes')
        self.tree.column("column3", width=200, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Grupo')
        self.tree.column("column4", width=60, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Preço')
        self.tree.grid(row=0, column=4, padx=10, pady=10,columnspan=3, rowspan=6) #columnspan 3 significa ocupar tres colunas e rowspan é para ocupar 6 linhas da janela
        self.MostrarProdutosBeckEnd()

        self.cadastrar.mainloop()



    def __init__(self):
        self.root = Tk()
        self.root.title('Admin')
        Button(self.root,text='Pedidos',width=20, bg='blue1').grid(row=0, column=0, pady=10, padx=10)
        Button(self.root,text='Cadastros', width=20, bg='blue1', command=self.CadastrarProduto).grid(row=1, column=0,pady=10, padx=10) #ao clicar no botao cadastro sera redirencionado para a def acima

        self.root.mainloop()


    @staticmethod
    def conectar():
        conexao = pymysql.connect(
            host='localhost',
            user='root',
            password='1234',
            db='erp',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )



    def MostrarProdutosBeckEnd(self):
        try:
            AdminJanela.conectar()
        except:
            print('Erro ao se conectar ao banco de dados')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from produtos')
                resultados = cursor.fetchall()
        except:
            print('Erro ao fazer a consulta')
        self.tree.delete(*self.tree.get_children())

        linhaV = []
        for linha in resultados:
            linhaV.append(linha['nome'])
            linhaV.append(linha['ingredientes'])
            linhaV.append(linha['grupo'])
            linhaV.append(linha['preco'])
            self.tree.insert("", END, values=linhaV, iid=linha['id'], tags='1')#passando o iid no momento da inserçao dos dados facilitara na hora de excluir, porque quando clicarmos no elemento dentro da treview ele tera um id
            linhaV.clear()


    def CadastrarProdutoBackEnd(self):
        nome = self.nome.get()
        ingredientes = self.ingredientes.get()
        grupo = self.grupo.get()
        preco = self.preco.get()

        try:  #muito interessante criar uma função para conexão para ficar mais facil ao inves de ficar copiando e colando a conexao
            AdminJanela.conectar()
        except:
            print('Erro ao se conectar ao banco de dados')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('insert into produtos(nome,ingredientes,grupo,preco) values(%s,%s,%s,%s)',(nome,ingredientes,grupo,preco)) #inserindo dados digitados dentro do banco de dados
                conexao.commit() #conectando com o banco de dados
        except:
            print('Erro ao fazer a consulta 1')

        messagebox.showinfo('Aviso','Produto cadastrado com sucesso!')
        self.MostrarProdutosBeckEnd()



    def RemoverCadastrosBackEnd(self):
        idDeletar = int(self.tree.selection()[0]) #vai pegar o valor do id do elemento do meu banco de dados para excluir
        try:
           AdminJanela.conectar()
        except:
            print('Erro ao se conectar ao banco de dados')
        try:
            with conexao.cursor() as cursor:
                cursor.execute(f'delete from produtos where id ={idDeletar}')
                conexao.commit()
        except:
            print('Erro ao fazer a consulta')
        messagebox.showinfo('', 'Produto excluido com sucesso!')
        self.MostrarProdutosBeckEnd()


    def LimparCadastrosBackEnd(self):
        if messagebox.askokcancel('Limpar dados Cuidado!', 'DESEJA ESCLUIR TODOS OS DADOS DA TABELA?'):
            #com este if eu crio uma janela para confirmar se eu quero exclui ou não os dados. posso fazer em todo casa tanto no momento de excluir como no momento de cadastrar ou posso usar os ifs feitos no curso em video
            try:
                AdminJanela.conectar()
            except:
                print('Erro ao se conectar ao banco de dados')
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('truncadte table produtos:') #só escluiu os dados de dentro da tabela
                    conexao.commit()
            except:
                print('Erro ao fazer a consulta')

            self.MostrarProdutosBeckEnd()


class JanelaLogin():#class vai ser uma janela do nosso programa
    def verificaLogin(self):

        autenticado = False
        usuarioMaster = False
        try:
            AdminJanela.conectar()
        except:
            print('Erro ao se conectar ao banco de dados')
        usuario = self.login.get()  #o que o usuario digitar dentro do Entry abaixo ira para dentro desta variavel
        senha = self.senha.get()
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from cadastros')
                resultados = cursor.fetchall()
        except:
            print('Erro ao fazer a consulta')
        for linha in resultados:
            if usuario == linha['nome'] and senha == linha['senha']:
                autenticado = True
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                break
            else:
                autenticado = False
        if not autenticado:
            messagebox.showinfo('login', 'Email ou senha invalido')
        if autenticado:
            messagebox.showinfo('Autenticado',f'Bem vindo ao programa {linha["nome"]}')
            self.root.destroy()
            if usuarioMaster:
                AdminJanela()


    def CadastrosBackEnd(self):
        codigoPadrao = '1234'
        if self.codigoSeguranca.get() == codigoPadrao:
            if len(self.login.get()) <=20:
                if len(self.senha.get()) <=50:
                    nome = self.login.get()
                    senha = self.senha.get()
                    try:
                        AdminJanela.conectar()
                    except:
                        print('Erro ao se conectar ao banco de dados')
                    try:
                        with conexao.cursor() as cursor:
                            cursor.execute('insert into cadastros (nome, senha, nivel) values (%s,%s,%s)',(nome,senha, 1))
                            conexao.commit()

                        messagebox.showinfo('Cadastro', 'Usuario cadastrado com sucesso!')
                        self.root.destroy()
                    except:
                        print('Erro ao inserir os dados')
                else:
                    messagebox.showinfo('Erro', 'Por favor insira uma senha com 50 ou menos caracteres')
            else:
                messagebox.showinfo('Erro', 'Por favor, insira um nome com 20 ou menos caracteres')
        else:
            messagebox.showinfo('Erro', 'Erro no codigo de segurança')


    def Cadastros(self):
        Label(self.root, text='Chave de Segurança').grid(row=3,column=0, pady=5, padx=5)
        self.codigoSeguranca = Entry(self.root, show='*')
        self.codigoSeguranca.grid(row=3,column=1,pady=5,padx=10)
        Button(self.root,text='Confirmar cadastro', width=15, bg='blue1',command=self.CadastrosBackEnd).grid(row=4,column=0, columnspan=3, pady=5,padx=10)


    def UpdateBeckEnd(self): #interligando com MYSQL, onde os arquivos serão armazenados.
        try:
           AdminJanela.conectar()
        except:
            print('Erro ao se conectar ao banco de dados')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from cadastros')
                resultados = cursor.fetchall()
        except:
            print('Erro ao fazer a consulta')
        self.tree.delete(*self.tree.get_children())
        linhaV = []
        for linha in resultados:
            linhaV.append(linha['id'])
            linhaV.append(linha['nome'])
            linhaV.append(linha['senha'])
            linhaV.append(linha['nivel'])
            self.tree.insert("", END, values=linhaV, iid=linha['id'], tags='1')


            linhaV.clear()


    def VisualizarCadastros(self):
        self.vc = Toplevel()
        self.vc.resizable(False,False)
        self.vc.title('Visualizar Cadastros')
        self.tree = ttk.Treeview(self.vc,selectmode= 'browse', columns=("column1","column2","column3","column4"),show='headings')
        self.tree.column("column1",width=40, minwidth=500, stretch=NO)
        self.tree.heading('#1',text='id')
        self.tree.column("column2", width=100, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='usuario')
        self.tree.column("column3", width=100, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='senha')
        self.tree.column("column4", width=40, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='nivel')
        self.tree.grid(row=0, column=0, padx=10, pady=10)
        self.UpdateBeckEnd()
        self.vc.mainloop()


    def __init__(self): # o init será sempre mostrado
        self.root = Tk()
        self.root.title('Login')
        Label(self.root, text='Faça seu login').grid(row=0, column=0, columnspan=2)
        Label(self.root, text='Usuario').grid(row=1, column=0)
        self.login = Entry(self.root)

        self.login.grid(row=1, column=1, padx=5,pady=5)
        Label(self.root, text='Senha').grid(row=2, column=0)
        self.senha = Entry(self.root, show='*')
        self.senha.grid(row=2, column=1, padx=5,pady=5)
        Button(self.root,text='login',bg='green3',width=10, command=self.verificaLogin).grid(row=5,column=0, padx=5,pady=5)
        Button(self.root, text='cadastrar', bg='orange3', width=10, command=self.Cadastros).grid(row=5, column=1, padx=5, pady=5)
        Button(self.root, text='Visualizar Cadastros', bg='white', command=self.VisualizarCadastros).grid(row=6, columnspan=2, column=0, padx=5, pady=5)
        self.root.mainloop()

JanelaLogin() #sempre que eu chamar esta janela ele mostrara tudo que estiver dentro desta funçao e executara