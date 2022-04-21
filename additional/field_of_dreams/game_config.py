PRIZE = -3
PLUS = -1
X2 = -2
BANK = -4

ALPHABET = list("йцукенгшщзхъфывапролджэячсмитьбюё".upper())

STATES_DESCRIPTIONS = {
    0: "Сектор ноль!",
    PRIZE: "Сектор приз на барабане!",
    PLUS: "Сектор плюс! Открыта случайная буква!",
    X2: "Ваши очки удвоены",
    BANK: "Теперь вы банкрот!",
}

DRUM_SCORES = [
    0,
    250,
    350,
    PRIZE,
    100,
    750,
    100,
    PLUS,
    250,
    300,
    100,
    500,
    250,
    BANK,
    100,
    350,
    100,
    0,
    100,
    500,
    350,
    PRIZE,
    100,
    X2,
    100,
    PLUS,
    100,
    750,
    250,
    750,
    100,
    BANK,
    300,
    500,
    100
]

EXTRA_DECISIONS = {
    0: "Сектор ноль!",
    BANK: "А вы всё равно банкрот!",
    PRIZE: "Сектор приз на барабане!",
    PLUS: "Сектор плюс на барабане!",

}
#
# DRUM_SCORES = [
#     100,
#     200,
#     300,
#     400,
#     500,
#     0,
#     -1,
#     -2,
#     -3,
#     -4
#
# ]
#
# DRUM_SCORES = [
#     0,
#     -3,
#     -2,
#     -1
#
# ]