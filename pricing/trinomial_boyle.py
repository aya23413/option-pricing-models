import math


# ============================================================
# PARAMETRES BOYLE
# ============================================================

def boyle_parameters(T, r, sigma, N):
    """
    Calcule les paramètres de l'arbre trinomial de Boyle.
    """

    if N <= 0:
        raise ValueError("N doit être > 0")

    if T <= 0:
        raise ValueError("T doit être > 0")

    if sigma <= 0:
        raise ValueError("sigma doit être > 0")

    # Pas de temps
    dt = T / N

    # Facteurs de mouvement
    u = math.exp(
        sigma * math.sqrt(2 * dt)
    )

    m = 1.0
    d = 1 / u

    # Probabilités de Boyle
    numerator_up = (
        math.exp(r * dt / 2)
        - math.exp(-sigma * math.sqrt(dt / 2))
    )

    denominator = (
        math.exp(sigma * math.sqrt(dt / 2))
        - math.exp(-sigma * math.sqrt(dt / 2))
    )

    numerator_down = (
        math.exp(sigma * math.sqrt(dt / 2))
        - math.exp(r * dt / 2)
    )

    pu = (numerator_up / denominator) ** 2
    pd = (numerator_down / denominator) ** 2
    pm = 1 - pu - pd

    # Vérification des probabilités
    if pu < 0 or pm < 0 or pd < 0:
        raise ValueError(
            "Probabilités trinomiales invalides. "
            "Essayez un N plus grand."
        )

    # Facteur d'actualisation
    discount = math.exp(-r * dt)

    return {
        "dt": dt,
        "u": u,
        "m": m,
        "d": d,
        "pu": pu,
        "pm": pm,
        "pd": pd,
        "discount": discount
    }


# ============================================================
# PRICING BOYLE
# ============================================================

def boyle_trinomial_price(
    S0,
    K,
    T,
    r,
    sigma,
    N,
    option_type="call",
    exercise_type="european"
):
    """
    Arbre trinomial de Boyle.

    Supporte :
    - Call européen
    - Put européen
    - Call américain
    - Put américain
    """

    # ========================================================
    # VERIFICATION DES PARAMETRES
    # ========================================================

    if N <= 0:
        raise ValueError("N doit être > 0")

    if S0 <= 0:
        raise ValueError("S0 doit être > 0")

    if K <= 0:
        raise ValueError("K doit être > 0")

    if T <= 0:
        raise ValueError("T doit être > 0")

    if sigma <= 0:
        raise ValueError("sigma doit être > 0")

    option_type = option_type.lower()
    exercise_type = exercise_type.lower()

    if option_type not in ["call", "put"]:
        raise ValueError(
            "option_type doit être 'call' ou 'put'"
        )

    if exercise_type not in ["european", "american"]:
        raise ValueError(
            "exercise_type doit être 'european' ou 'american'"
        )

    # ========================================================
    # PARAMETRES BOYLE
    # ========================================================

    params = boyle_parameters(
        T=T,
        r=r,
        sigma=sigma,
        N=N
    )

    u = params["u"]
    pu = params["pu"]
    pm = params["pm"]
    pd = params["pd"]
    discount = params["discount"]

    # ========================================================
    # PRIX DU SOUS-JACENT A MATURITE
    # ========================================================

    stock_prices = {}

    for j in range(-N, N + 1):

        S = S0 * (u ** j)

        stock_prices[j] = S

    # ========================================================
    # PAYOFF A MATURITE
    # ========================================================

    option_values = {}

    for j, S in stock_prices.items():

        if option_type == "call":
            payoff = max(S - K, 0)

        else:
            payoff = max(K - S, 0)

        option_values[j] = payoff

    # ========================================================
    # BACKWARD INDUCTION
    # ========================================================

    for i in range(N - 1, -1, -1):

        new_values = {}

        for j in range(-i, i + 1):

            continuation = discount * (
                pu * option_values[j + 1]
                + pm * option_values[j]
                + pd * option_values[j - 1]
            )

            # Option européenne
            if exercise_type == "european":

                value = continuation

            # Option américaine
            else:

                S = S0 * (u ** j)

                if option_type == "call":
                    exercise = max(S - K, 0)

                else:
                    exercise = max(K - S, 0)

                value = max(
                    exercise,
                    continuation
                )

            new_values[j] = value

        option_values = new_values

    # ========================================================
    # PRIX INITIAL
    # ========================================================

    return option_values[0]