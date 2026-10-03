import math


# ============================================================
# PARAMETRES JARROW-RUDD
# ============================================================

def jarrow_rudd_parameters(T, r, sigma, N):
    """
    Calcule les paramètres du modèle binomial Jarrow-Rudd.

    Retourne :
    - dt : durée d'une période
    - u  : facteur de hausse
    - d  : facteur de baisse
    - p  : probabilité de hausse
    - q  : probabilité de baisse
    - discount : facteur d'actualisation
    """

    if N <= 0:
        raise ValueError("N doit être > 0")

    if T <= 0:
        raise ValueError("T doit être > 0")

    if sigma <= 0:
        raise ValueError("sigma doit être > 0")

    # Durée d'une période
    dt = T / N

    # Facteur de hausse Jarrow-Rudd
    u = math.exp(
        (r - 0.5 * sigma**2) * dt
        + sigma * math.sqrt(dt)
    )

    # Facteur de baisse Jarrow-Rudd
    d = math.exp(
        (r - 0.5 * sigma**2) * dt
        - sigma * math.sqrt(dt)
    )

    # Probabilités symétriques de Jarrow-Rudd
    p = 0.5
    q = 0.5

    # Facteur d'actualisation
    discount = math.exp(-r * dt)

    return {
        "dt": dt,
        "u": u,
        "d": d,
        "p": p,
        "q": q,
        "discount": discount
    }


# ============================================================
# PRICING JARROW-RUDD
# ============================================================

def jarrow_rudd_price(
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
    Valorisation d'une option vanille avec le modèle
    binomial de Jarrow-Rudd.

    Permet de valoriser :
    - Call européen
    - Put européen
    - Call américain
    - Put américain
    """

    # ========================================================
    # 1. VERIFICATION DES PARAMETRES
    # ========================================================

    if N <= 0:
        raise ValueError("N doit être > 0")

    if S0 <= 0 or K <= 0:
        raise ValueError("S0 et K doivent être > 0")

    if T <= 0:
        raise ValueError("T doit être > 0")

    if sigma <= 0:
        raise ValueError("sigma doit être > 0")

    option_type = option_type.lower()
    exercise_type = exercise_type.lower()

    if option_type not in ("call", "put"):
        raise ValueError(
            "option_type doit être 'call' ou 'put'"
        )

    if exercise_type not in ("european", "american"):
        raise ValueError(
            "exercise_type doit être 'european' ou 'american'"
        )

    # ========================================================
    # 2. PARAMETRES JARROW-RUDD
    # ========================================================

    params = jarrow_rudd_parameters(
        T=T,
        r=r,
        sigma=sigma,
        N=N
    )

    u = params["u"]
    d = params["d"]
    p = params["p"]
    q = params["q"]
    discount = params["discount"]

    # ========================================================
    # 3. PRIX DU SOUS-JACENT A MATURITE
    # ========================================================

    stock_prices = []

    for j in range(N + 1):

        S = (
            S0
            * (u ** j)
            * (d ** (N - j))
        )

        stock_prices.append(S)

    # ========================================================
    # 4. PAYOFF A MATURITE
    # ========================================================

    option_values = []

    for S in stock_prices:

        if option_type == "call":
            payoff = max(S - K, 0)

        else:
            payoff = max(K - S, 0)

        option_values.append(payoff)

    # ========================================================
    # 5. BACKWARD INDUCTION
    # ========================================================

    for i in range(N - 1, -1, -1):

        new_values = []

        for j in range(i + 1):

            # Prix du sous-jacent au noeud
            S = (
                S0
                * (u ** j)
                * (d ** (i - j))
            )

            # Valeur de continuation
            continuation = discount * (
                p * option_values[j + 1]
                + q * option_values[j]
            )

            # OPTION EUROPEENNE
            # Pas d'exercice anticipé
            if exercise_type == "european":

                value = continuation

            # OPTION AMERICAINE
            # Comparaison exercice immédiat / continuation
            else:

                if option_type == "call":
                    exercise = max(S - K, 0)

                else:
                    exercise = max(K - S, 0)

                value = max(
                    exercise,
                    continuation
                )

            new_values.append(value)

        option_values = new_values

    # ========================================================
    # 6. PRIX DE L'OPTION A t = 0
    # ========================================================

    return option_values[0]