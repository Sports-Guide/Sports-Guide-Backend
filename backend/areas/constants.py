from enum import Enum


class ModerationStatus(Enum):
    """
    Константы для статусов модерации площадок.
    """
    REJECTED = 'rejected'
    PENDING = 'pending'
    APPROVED = 'approved'
