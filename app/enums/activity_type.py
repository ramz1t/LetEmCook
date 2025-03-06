from enum import Enum


class ActivityType(Enum):
    Sedentary = 1.2
    Lightly_active = 1.375
    Moderately_active = 1.55
    Very_active = 1.725
    Super_active = 1.9