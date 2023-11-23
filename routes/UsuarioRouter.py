from io import BytesIO
from babel.dates import format_datetime, get_month_names
from babel.numbers import format_currency
from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from models.Categoria import Categoria
from models.Conta import Conta
from models.Dependente import Dependente
from PIL import Image

from models.Usuario import Usuario
from repositories.CategoriaRepo import CategoriaRepo
from repositories.ContaRepo import ContaRepo
from repositories.DependenteRepo import DependenteRepo
from repositories.TransacaoRepo import TransacaoRepo
from repositories.UsuarioRepo import UsuarioRepo
from util.imageUtil import transformar_em_circulo
from util.seguranca import (
    gerar_token,
    obter_hash_senha,
    validar_usuario_logado,
    verificar_senha,
)
from util.templateFilters import capitalizar_nome_proprio, formatar_data
from util.validators import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatar_data


@router.post(
    "/novousuario",
    tags=["Usuário"],
    summary="Inserir um novo usuário ao sistema.",
    response_class=HTMLResponse,
)
async def postNovoUsuario(
    request: Request,
    nome: str = Form(""),
    email: str = Form(""),
    senha: str = Form(""),
    confirmarSenha: str = Form(""),
    termoUso: str = Form(""),
    usuario: Usuario = Depends(validar_usuario_logado),
):
    nome = capitalizar_nome_proprio(nome).strip()

    email = email.lower().strip()

    senha = senha.strip()

    confirmarSenha = confirmarSenha.strip()

    errosCad = {}

    is_not_empty(nome, "nome", errosCad)
    is_person_fullname(nome, "nome", errosCad)

    is_not_empty(email, "email", errosCad)
    if is_email(email, "email", errosCad):
        if UsuarioRepo.emailExiste(email):
            add_error(
                "email", "Já existe um usuário cadastrado com este e-mail.", errosCad
            )

    is_not_empty(senha, "senha", errosCad)
    is_password(senha, "senha", errosCad)

    is_not_empty(confirmarSenha, "confirmarSenha", errosCad)
    is_matching_fields(confirmarSenha, "confirmarSenha", senha, "Senha", errosCad)

    is_not_none(termoUso, "termoUso", errosCad)

    if len(errosCad) > 0:
        valoresCad = {}
        valoresCad["nome"] = nome
        valoresCad["email"] = email.lower()

        return templates.TemplateResponse(
            "usuario/entrar.html",
            {
                "request": request,
                "usuario": usuario,
                "errosCad": errosCad,
                "valoresCad": valoresCad,
            },
        )

    UsuarioRepo.inserir(
        Usuario(
            id=0,
            nome=nome,
            email=email,
            senha=obter_hash_senha(senha),
        )
    )
    token = gerar_token()
    UsuarioRepo.alterarToken(email, token)
    response = RedirectResponse("/dashboard", status.HTTP_302_FOUND)
    response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True)

    despesa = [
        "Aluguel",
        "Hipoteca",
        "Condomínio",
        "Energia elétrica",
        "Água",
        "Gás",
        "Internet",
        "Telefone fixo",
        "Plano de saúde",
        "Seguro do carro",
        "Mensalidade da academia",
        "Educação dos filhos",
        "Supermercado",
        "Transporte público",
        "Combustível",
        "Manutenção do carro",
        "Assinatura de streaming",
        "Refeições fora de casa",
        "Roupas",
        "Lazer",
        "Presentes",
        "Impostos",
        "Despesas médicas",
        "Despesas educacionais",
        "Despesas com animais de estimação",
    ]

    receita = [
        "Salário",
        "Freelancer",
        "Aluguel de propriedades",
        "Rendimentos de investimentos",
        "Vendas de produtos",
        "Consultoria",
        "Bônus",
        "Comissões",
        "Aluguel de quartos",
        "Trabalho temporário",
        "Dividendos",
        "Vendas online",
        "Renda passiva",
        "Pensão",
        "Prêmios",
    ]

    usuario = UsuarioRepo.obterUsuarioPorToken(token)

    for i in range(len(despesa)):
        CategoriaRepo.inserir(Categoria(0, usuario.id, despesa[i], "Despesa"))

    for i in range(len(receita)):
        CategoriaRepo.inserir(Categoria(0, usuario.id, receita[i], "Receita"))

    ContaRepo.inserir(
        Conta(0, usuario.id, "Carteira", 0, "Esta é a sua carteira física de dinheiro.")
    )

    DependenteRepo.inserir(Dependente(0, usuario.id, usuario.nome.split()[0]))

    return response


@router.get(
    "/dashboard",
    tags=["Usuário"],
    summary="Visualizar o dashboard do sistema.",
    response_class=HTMLResponse,
)
async def getDashboard(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        pagina = "/dashboard"
        hora = datetime.now().hour
        if 6 <= hora < 12:
            mensagem = "Bom dia, "
        elif hora < 18:
            mensagem = "Boa tarde, "
        else:
            mensagem = "Boa noite, "

        transacoes = TransacaoRepo.obterTransacaoPorUsuario(usuario.id)
        receita = TransacaoRepo.obterReceita(usuario.id)
        despesa = TransacaoRepo.obterDespesa(usuario.id)
        saldo = TransacaoRepo.obterSaldo(usuario.id)

        categorias = CategoriaRepo.obterCategoriaPorUsuario(usuario.id)
        lista_categoria_despesa = []
        for t in transacoes:
            if t.tipo == "Despesa":
                lista_categoria_despesa.append(t.nomeCategoria)

        receita = format_currency(receita, "BRL", locale="pt_BR")
        saldo = format_currency(saldo, "BRL", locale="pt_BR")
        despesa = format_currency(despesa, "BRL", locale="pt_BR")

        contas = ContaRepo.obterContaPorUsuario(usuario.id)

        dependentes = DependenteRepo.obterDependentePorUsuario(usuario.id)

        data_hora = format_datetime(
            datetime.now(), format="short", locale="pt_BR"
        ).title()
        meses = get_month_names("wide", locale="pt_BR")
        return templates.TemplateResponse(
            "usuario/dashboard.html",
            {
                "request": request,
                "usuario": usuario,
                "transacoes": transacoes,
                "receita": receita,
                "despesa": despesa,
                "categorias": categorias,
                "contas": contas,
                "dependentes": dependentes,
                "saldo": saldo,
                "mensagem": mensagem,
                "pagina": pagina,
                "data_hora": data_hora,
                "meses": meses,
                "lista_despesa": lista_categoria_despesa,
            },
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/recuperarSenha")
async def getRecuperar(request: Request):
    return templates.TemplateResponse(
        "usuario/recuperarSenha.html",
        {
            "request": request,
        },
    )


@router.get("/usuario/perfil")
async def getPerfil(
    request: Request,
    mensagem="Perfil",
    pagina="/configuracoes",
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        return templates.TemplateResponse(
            "usuario/perfil.html",
            {
                "request": request,
                "usuario": usuario,
                "mensagem": mensagem,
                "pagina": pagina,
                "usuario": usuario,
            },
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/alterarSenha", response_class=HTMLResponse)
async def getAlterarSenha(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    mensagem="Alterar senha",
    pagina="/configuracoes",
):
    if usuario:
        return templates.TemplateResponse(
            "usuario/alterarSenha.html",
            {
                "request": request,
                "usuario": usuario,
                "mensagem": mensagem,
                "pagina": pagina,
            },
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/alterarSenha", response_class=HTMLResponse)
async def postAlterarSenha(
    request: Request,
    mensagem="Senha alterada",
    pagina="/configuracoes",
    usuario: Usuario = Depends(validar_usuario_logado),
    senhaAtual: str = Form(""),
    novaSenha: str = Form(""),
    confNovaSenha: str = Form(""),
):
    # normalização dos dados
    senhaAtual = senhaAtual.strip()
    novaSenha = novaSenha.strip()
    confNovaSenha = confNovaSenha.strip()

    # verificação de erros
    erros = {}
    # validação do campo senhaAtual
    is_not_empty(senhaAtual, "senhaAtual", erros)
    is_password(senhaAtual, "senhaAtual", erros)
    # validação do campo novaSenha
    is_not_empty(novaSenha, "novaSenha", erros)
    is_password(novaSenha, "novaSenha", erros)
    # validação do campo confNovaSenha
    is_not_empty(confNovaSenha, "confNovaSenha", erros)
    is_matching_fields(confNovaSenha, "confNovaSenha", novaSenha, "Nova Senha", erros)

    # só verifica a senha no banco de dados se não houverem erros de validação
    if len(erros) == 0:
        hash_senha_bd = UsuarioRepo.obterSenhaDeEmail(usuario.email)
        if hash_senha_bd:
            if not verificar_senha(senhaAtual, hash_senha_bd):
                add_error("senhaAtual", "Senha atual está incorreta.", erros)

    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}
        valores["senhaAtual"] = senhaAtual
        valores["novaSenha"] = novaSenha
        valores["confNovaSenha"] = confNovaSenha
        return templates.TemplateResponse(
            "usuario/alterarSenha.html",
            {
                "request": request,
                "usuario": usuario,
                "erros": erros,
                "valores": valores,
                "mensagem": mensagem,
                "pagina": pagina,
            },
        )

    # se passou pelas validações, altera a senha no banco de dados
    hash_nova_senha = obter_hash_senha(novaSenha)
    UsuarioRepo.alterarSenha(usuario.id, hash_nova_senha)

    # mostra página de sucesso
    return templates.TemplateResponse(
        "usuario/alterouSenha.html",
        {
            "request": request,
            "usuario": usuario,
            "mensagem": mensagem,
            "pagina": pagina,
        },
    )


@router.post("/usuario/imagem")
async def postImagem(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    arquivoImagem: UploadFile = File(...),
):
    erros = {}

    conteudo_arquivo = await arquivoImagem.read()
    imagem = Image.open(BytesIO(conteudo_arquivo))
    if not imagem:
        add_error("arquivoImagem", "Nenhuma imagem foi enviada.", erros)

    if len(erros) > 0:
        return templates.TemplateResponse(
            "usuario/perfil.html",
            {
                "request": request,
                "usuario": usuario,
                "erros": erros,
            },
        )

    imagem_quadrada = transformar_em_circulo(imagem)
    imagem_quadrada.save(f"static/img/usuario/{usuario.id:04d}.jpg", "JPEG")

    return templates.TemplateResponse(
        "usuario/perfil.html",
        {"request": request, "usuario": usuario},
    )
