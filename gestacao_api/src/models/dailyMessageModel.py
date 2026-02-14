from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class MessageType(str, Enum):
    """
    Estilos visuais/temas do widget
    - afetam cores, backgrounds, decoração
    """

    # TIPOS GRATUITOS
    padrao = 'padrão'  # Rosa suave padrão do app

    # TIPOS PREMIUM
    floral = 'floral'  # Tons florais, pétalas, rosa/lavanda
    oceano = 'oceano'  # Azul/verde água, ondas, conchas
    transformacao = 'transformação'  # Roxo/dourado, borboletas, metamorfose
    noite = 'noite'  # Azul escuro/roxo, estrelas, lua
    natureza = 'natureza'  # Verde/marrom, folhas, terra
    seu_corpo = 'seu corpo'  # Tons pele, anatomia suave, empoderamento
    sol = 'sol'  # Amarelo/laranja, raios, energia
    serenidade = 'serenidade'  # Branco/bege, minimalista, zen
    forca = 'força'  # Vermelho/laranja, empoderamento, energia
    ternura = 'ternura'  # Rosa bebê/lilás, delicado, suave


class MessageCategory(str, Enum):
    """
    Categorias de conteúdo
    - definem o tipo de mensagem
    """

    # CATEGORIAS DE BEM-ESTAR
    motivacional = 'motivacional'  # Encorajamento, força, superação
    saude = 'saúde'  # Dicas de saúde física
    emocional = 'emocional'  # Saúde mental, sentimentos
    autocuidado = 'autocuidado'  # Tempo para si, mimos
    mindfulness = 'mindfulness'  # Meditação, presença, gratidão

    # CATEGORIAS SOBRE O BEBÊ
    desenvolvimento = 'desenvolvimento'  # Crescimento semanal do bebê
    bebe = 'bebê'  # Informações gerais sobre o bebê
    conexao = 'conexão'  # Vínculo mãe-bebê
    mensagem_do_bebe = 'mensagem do bebê'  # Como se o bebê falasse (PREMIUM)

    # CATEGORIAS PRÁTICAS
    nutricao = 'nutrição'  # Alimentação, receitas
    pratica = 'prática'  # Dicas práticas, organização
    parto = 'parto'  # Preparação para o parto
    relacionamento = 'relacionamento'  # Parceiro, família, apoio

    # CATEGORIAS ESPECIAIS (PREMIUM)
    diversao = 'diversão'  # Curiosidades, humor, leveza
    curiosidade = 'curiosidade'  # Fatos interessantes
    celebracao = 'celebração'  # Marcos, conquistas
    inspiracao = 'inspiração'  # Frases inspiradoras, citações


# ============================================
# DAILY MESSAGE MODEL
# ============================================


class DailyMessage(SQLModel, table=True):
    __tablename__ = 'daily_messages'

    id: Optional[int] = Field(default=None, primary_key=True)

    message: str = Field()
    emoji: str = Field()

    category: MessageCategory
    type: MessageType = Field(default=MessageType.padrao)

    onlyPremium: bool = Field(default=False)

    week_min: Optional[int] = Field(
        default=None, description='Semana gestacional mínima (1-40)'
    )
    week_max: Optional[int] = Field(
        default=None, description='Semana gestacional máxima (1-40)'
    )
    trimester: Optional[int] = Field(
        default=None, description='Trimestre específico (1, 2 ou 3)'
    )
    tags: Optional[str] = Field(
        default=None, description='Tags separadas por vírgula'
    )
