class PipelineBaseException(Exception):
    """Exceção base para o pipeline de dados."""
    pass


class TransientNetworkError(PipelineBaseException):
    """Erro temporário de conexão/rede que deve acionar retry."""
    pass


class InvalidDataPayloadError(PipelineBaseException):
    """Erro de dados inválidos ou corrompidos que NÃO deve tentar novamente."""
    pass