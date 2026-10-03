import math


def crr_price(
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
    Modèle binomial CRR
    Cox-Ross-Rubinstein.

    Permet de valoriser :
    - Call européen
    - Put européen
    - Call américain
    - Put américain
    """

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

    if option_type not in ["call", "put"]:
        raise ValueError("option_type doit être 'call' ou 'put'")

    if exercise_type not in ["european", "american"]:
        raise ValueError(
            "exercise_type doit être 'european' ou 'american'"
        )

    # 1. Durée d'un pas
    dt = T / N

    # 2. Facteurs up et down
    u = math.exp(sigma * math.sqrt(dt))
    d = math.exp(-sigma * math.sqrt(dt))

    # 3. Probabilité risque-neutre
    p = (
        math.exp(r * dt) - d
    ) / (u - d)

    q = 1 - p

    # Vérification
    if not 0 <= p <= 1:
        raise ValueError(
            "Probabilité risque-neutre invalide. "
            "Essayez un N plus grand."
        )

    # 4. Facteur d'actualisation
    discount = math.exp(-r * dt)

    # ------------------------------------------------
    # Valeurs de l'action à maturité
    # ------------------------------------------------

    stock_prices = []

    for j in range(N + 1):

        S = (
            S0
            * (u ** j)
            * (d ** (N - j))
        )

        stock_prices.append(S)

    # ------------------------------------------------
    # Payoff à maturité
    # ------------------------------------------------

    option_values = []

    for S in stock_prices:

        if option_type == "call":
            payoff = max(S - K, 0)

        else:
            payoff = max(K - S, 0)

        option_values.append(payoff)

    # ------------------------------------------------
    # Backward induction
    # ------------------------------------------------

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

            # Valeur d'exercice immédiat
            if option_type == "call":

                exercise = max(S - K, 0)

            else:

                exercise = max(K - S, 0)

            # European
            if exercise_type == "european":

                value = continuation

            # American
            else:

                value = max(
                    exercise,
                    continuation
                )

            new_values.append(value)

        option_values = new_values

    return option_values[0]