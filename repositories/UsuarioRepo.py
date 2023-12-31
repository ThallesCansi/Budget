from typing import List

from models.Usuario import Usuario
from util.Database import Database



class UsuarioRepo:
    @classmethod
    def criarTabela(cls):
        sql = """CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                senha TEXT NOT NULL,
                token TEXT,
                UNIQUE (email)
            )"""
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tabela_criada = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tabela_criada

    @classmethod
    def inserir(cls, usuario: Usuario) -> Usuario:
        sql = """
                INSERT INTO usuario (nome, email, senha)
                VALUES (?, ?, ?)
              """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha))
        if resultado.rowcount > 0:
            usuario.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return usuario

    @classmethod
    def alterar(cls, usuario: Usuario) -> Usuario:
        sql = "UPDATE usuario SET nome=?, email=?, senha=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (usuario.nome, usuario.email, usuario.senha, usuario.id)
        )
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return usuario
        else:
            conexao.close()
            return None
    
    @classmethod
    def alterarSenha(cls, id: int, senha: str) -> bool:
        sql = "UPDATE usuario SET senha=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (senha, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
    
    @classmethod
    def alterarToken(cls, email: str, token: str) -> bool:
        sql = "UPDATE usuario SET token=? WHERE email=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token, email))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
    
    @classmethod
    def emailExiste(cls, email: str) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM usuario WHERE email=?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()        
        return bool(resultado[0])

    @classmethod
    def obterSenhaDeEmail(cls, email: str) -> str | None:
        sql = "SELECT senha FROM usuario WHERE email=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        if resultado:
            return str(resultado[0])
        else:
            return None

    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM usuario WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def limparTabela(cls) -> bool:
        sql = "DELETE FROM usuario"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultadoado = cursor.execute(sql)
        if resultadoado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def obterTodos(cls) -> List[Usuario]:
        sql = "SELECT usuario.id, usuario.nome, usuario.email FROM usuario"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Usuario(
                id=x[0],
                nome=x[1],
                email=x[2],
            )
            for x in resultado
        ]
        conexao.commit()
        conexao.close()
        return objetos

    @classmethod
    def obterPorId(cls, id: int) -> Usuario:
        sql = "SELECT usuario.id, usuario.nome, usuario.email FROM usuario WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchone()
        if (resultado):
            objeto = Usuario(
                id=resultado[0],
                nome=resultado[1],
                email=resultado[2]
            )
            return objeto
        else:
            return None

    @classmethod
    def obterPorEmail(cls, email: str) -> Usuario:
        sql = "SELECT * FROM usuario WHERE email=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        objeto = Usuario(*resultado) if resultado else False
        conexao.commit()
        conexao.close()
        return objeto

        
    @classmethod
    def obterUsuarioPorToken(cls, token: str) -> Usuario:
        sql = "SELECT id, nome, email FROM usuario WHERE token=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token,)).fetchone()
        if resultado:
            objeto = Usuario(*resultado)
            return objeto
        else:
            return None