from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class MessageType(str, Enum):
    """Estilos visuais/temas do widget - afetam cores, backgrounds, decoração"""
    
    # TIPOS GRATUITOS
    padrao = 'padrão'              # Rosa suave padrão do app
    
    # TIPOS PREMIUM
    floral = 'floral'              # Tons florais, pétalas, rosa/lavanda
    oceano = 'oceano'              # Azul/verde água, ondas, conchas
    transformacao = 'transformação' # Roxo/dourado, borboletas, metamorfose
    noite = 'noite'                # Azul escuro/roxo, estrelas, lua
    natureza = 'natureza'          # Verde/marrom, folhas, terra
    seu_corpo = 'seu corpo'        # Tons pele, anatomia suave, empoderamento
    sol = 'sol'                    # Amarelo/laranja, raios, energia
    serenidade = 'serenidade'      # Branco/bege, minimalista, zen
    forca = 'força'                # Vermelho/laranja, empoderamento, energia
    ternura = 'ternura'            # Rosa bebê/lilás, delicado, suave


class MessageCategory(str, Enum):
    """Categorias de conteúdo - definem o tipo de mensagem"""
    
    # CATEGORIAS DE BEM-ESTAR
    motivacional = 'motivacional'           # Encorajamento, força, superação
    saude = 'saúde'                         # Dicas de saúde física
    emocional = 'emocional'                 # Saúde mental, sentimentos
    autocuidado = 'autocuidado'             # Tempo para si, mimos
    mindfulness = 'mindfulness'             # Meditação, presença, gratidão
    
    # CATEGORIAS SOBRE O BEBÊ
    desenvolvimento = 'desenvolvimento'      # Crescimento semanal do bebê
    bebe = 'bebê'                           # Informações gerais sobre o bebê
    conexao = 'conexão'                     # Vínculo mãe-bebê
    mensagem_do_bebe = 'mensagem do bebê'   # Como se o bebê falasse (PREMIUM)
    
    # CATEGORIAS PRÁTICAS
    nutricao = 'nutrição'                   # Alimentação, receitas
    pratica = 'prática'                     # Dicas práticas, organização
    parto = 'parto'                         # Preparação para o parto
    relacionamento = 'relacionamento'       # Parceiro, família, apoio
    
    # CATEGORIAS ESPECIAIS (PREMIUM)
    diversao = 'diversão'                   # Curiosidades, humor, leveza
    curiosidade = 'curiosidade'             # Fatos interessantes
    celebracao = 'celebração'               # Marcos, conquistas
    inspiracao = 'inspiração'               # Frases inspiradoras, citações

# ============================================
#DAILY MESSAGE MODEL
# ============================================

class DailyMessage(SQLModel, table=True):
    __tablename__ = "daily_messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    message: str = Field()
    emoji: str = Field()
    
    category: MessageCategory
    type: MessageType = Field(default=MessageType.padrao)
    

    onlyPremium: bool = Field(default=False)
    
    week_min: Optional[int] = Field(default=None, description="Semana gestacional mínima (1-40)")
    week_max: Optional[int] = Field(default=None, description="Semana gestacional máxima (1-40)")
    trimester: Optional[int] = Field(default=None, description="Trimestre específico (1, 2 ou 3)")
    tags: Optional[str] = Field(default=None, description="Tags separadas por vírgula")


# TYPE_STYLES = {
#     MessageType.padrao: {
#         'color_primary': '#E8849C',      # Rosa padrão
#         'color_secondary': '#F5C6D3',    # Rosa claro
#         'color_background': '#FFF8F9',   # Off-white quente
#         'decoration': 'blobs',            # Círculos decorativos
#         'icon': '🌸',
#     },
#     MessageType.floral: {
#         'color_primary': '#D4A5C4',      # Lavanda
#         'color_secondary': '#F3D7E3',    # Rosa pétala
#         'color_background': '#FFF5FB',   # Branco floral
#         'decoration': 'petals',           # Pétalas flutuantes
#         'icon': '🌺',
#     },
#     MessageType.oceano: {
#         'color_primary': '#5BA3C9',      # Azul oceano
#         'color_secondary': '#A8D5E2',    # Azul claro
#         'color_background': '#F0F9FC',   # Azul muito claro
#         'decoration': 'waves',            # Ondas
#         'icon': '🌊',
#     },
#     MessageType.transformacao: {
#         'color_primary': '#9B6FB0',      # Roxo
#         'color_secondary': '#D4A853',    # Dourado
#         'color_background': '#F8F5FC',   # Lavanda claro
#         'decoration': 'butterflies',      # Borboletas
#         'icon': '🦋',
#     },
#     MessageType.noite: {
#         'color_primary': '#4A5F7F',      # Azul noturno
#         'color_secondary': '#8B9DC3',    # Azul acinzentado
#         'color_background': '#F5F7FA',   # Cinza azulado claro
#         'decoration': 'stars',            # Estrelas
#         'icon': '🌙',
#     },
#     MessageType.natureza: {
#         'color_primary': '#6B8E6B',      # Verde folha
#         'color_secondary': '#B8D4A8',    # Verde claro
#         'color_background': '#F7FBF5',   # Verde mu