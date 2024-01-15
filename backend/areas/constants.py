from enum import Enum


class ModerationStatus(Enum):
    REJECTED = 'rejected'
    PENDING = 'pending'
    APPROVED = 'approved'
