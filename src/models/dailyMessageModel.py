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
    floral = 'floral'
    oceano = 'oceano'
    transformacao = 'transformação'
    noite = 'noite'
    natureza = 'natureza'
    seu_corpo = 'seu corpo'
    sol = 'sol'
    serenidade = 'serenidade'
    forca = 'força'
    ternura = 'ternura'


class MessageCategory(str, Enum):
    """
    Categorias de conteúdo
    - definem o tipo de mensagem
    """

    # CATEGORIAS DE BEM-ESTAR
    motivacional = 'motivacional'
    saude = 'saúde'
    emocional = 'emocional'
    autocuidado = 'autocuidado'
    mindfulness = 'mindfulness'

    # CATEGORIAS SOBRE O BEBÊ
    desenvolvimento = 'desenvolvimento'
    bebe = 'bebê'
    conexao = 'conexão'
    mensagem_do_bebe = 'mensagem do bebê'

    # CATEGORIAS PRÁTICAS
    nutricao = 'nutrição'
    pratica = 'prática'
    parto = 'parto'
    relacionamento = 'relacionamento'

    # CATEGORIAS ESPECIAIS (PREMIUM)
    diversao = 'diversão'
    curiosidade = 'curiosidade'
    celebracao = 'celebração'
    inspiracao = 'inspiração'


class DailyMessage(SQLModel, table=True):
    __tablename__ = 'daily_messages'

    id: Optional[int] = Field(default=None, primary_key=True)

    message: str = Field()
    emoji: str = Field()

    category: MessageCategory
    type: MessageType = Field(default=MessageType.padrao)

    only_premium: bool = Field(default=False)

    week_min: Optional[int] = Field(
        default=None, description='Semana gestacional mínima (1-40)'
    )
    week_max: Optional[int] = Field(
        default=None, description='Semana gestacional máxima (1-40)'
    )
    trimester: Optional[int] = Field(
        default=None, description='Trimestre específico (1, 2 ou 3)'
    )
