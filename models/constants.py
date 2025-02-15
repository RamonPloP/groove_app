from enum import IntEnum


PAGINATE_DEFAULT_RESULS = 10
class Role(IntEnum):
    ADMIN = 0
    USER = 1

class SocialMediaType(IntEnum):
    FB = 0
    WP = 1
    IG = 2

class DanceReasons(IntEnum):
    EJERCICIO = 0
    EJERCICIO_PASION_HOBBY = 1
    ME_ENCANTA = 2
    ME_HACE_FELIZ = 3
    ME_QUIERO_DEDICAR_A_ESTO = 4
    TERAPIA = 5
    TODAS = 6

    def __str__(self):
        return {
            DanceReasons.EJERCICIO: "Ejercicio",
            DanceReasons.EJERCICIO_PASION_HOBBY: "Ejercicio, pasión y hobby",
            DanceReasons.ME_ENCANTA: "Me encanta",
            DanceReasons.ME_HACE_FELIZ: "Me hace feliz",
            DanceReasons.ME_QUIERO_DEDICAR_A_ESTO: "Me quiero dedicar a esto",
            DanceReasons.TERAPIA: "Terapia",
            DanceReasons.TODAS: "Todas",
        }[self]


class LeadsObservations(IntEnum):
    ASISTIO = 0
    NO_ASISTIO = 1
    DAR_RECORDATORIO = 2
    SE_INSCRIBIO = 3
    REAGENDA = 4
    OTRO = 5

class BloodType(IntEnum):
    A_POSITIVE = 0
    A_NEGATIVE = 1
    B_POSITIVE = 2
    B_NEGATIVE = 3
    AB_POSITIVE = 4
    AB_NEGATIVE = 5
    O_POSITIVE = 6
    O_NEGATIVE = 7

    def __str__(self):
        return {
            BloodType.A_POSITIVE: "A+",
            BloodType.A_NEGATIVE: "A-",
            BloodType.B_POSITIVE: "B+",
            BloodType.B_NEGATIVE: "B-",
            BloodType.AB_POSITIVE: "AB+",
            BloodType.AB_NEGATIVE: "AB-",
            BloodType.O_POSITIVE: "O+",
            BloodType.O_NEGATIVE: "O-",
        }[self]