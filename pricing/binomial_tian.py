import math


# ============================================================
# PARAMETRES TIAN
# ============================================================

def tian_parameters(T, r, sigma, N):
    """
    Calcule les paramètres du modèle binomial de Tian.
    """

    if N <= 0:
        raise ValueError("N doit être > 0")

    if T <= 0:
        raise ValueError("T doit être > 0")

    if sigma <= 0:
        raise ValueError("sigma doit être > 0")

    dt = T / N

    R = math.exp(r * dt)
    V = math.exp(sigma**2 * dt)

    discriminant = V**2 + 2 * V - 3

    if discriminant < 0:
        raise ValueError(
            "Discriminant négatif pour le modèle de Tian."
        )

    sqrt_term = math.sqrt(discriminant)

    u = (
        0.5
        * R
        * V
        * (V + 1 + sqrt_term)
    )

    d = (
        0.5
        * R
        * V
        * (V + 1 - sqrt_term)
    )

    p = (R - d) / (u - d)

    q = 1 - p

    if not 0 <= p <= 1:
        raise ValueError(
            "Probabilité invalide pour Tian."
        )

    discount = math.exp(-r * dt)

    return {
        "dt": dt,
        "R": R,
        "V": V,
        "u": u,
        "d": d,
        "p": p,
        "q": q,
        "discount": discount
    }


# ============================================================
# PRICING TIAN
# ============================================================

def tian_price(
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
    Modèle binomial de Tian.
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
        raise ValueError(
            "option_type doit être 'call' ou 'put'"
        )

    if exercise_type not in ["european", "american"]:
        raise ValueError(
            "exercise_type doit être 'european' ou 'american'"
        )

    # ========================================================
    # PARAMETRES TIAN
    # ========================================================

    params = tian_parameters(
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
    # PRIX DU SOUS-JACENT A MATURITE
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
    # PAYOFF A MATURITE
    # ========================================================

    option_values = []

    for S in stock_prices:

        if option_type == "call":
            payoff = max(S - K, 0)

        else:
            payoff = max(K - S, 0)

        option_values.append(payoff)

    # ========================================================
    # BACKWARD INDUCTION
    # ========================================================

    for i in range(N - 1, -1, -1):

        new_values = []

        for j in range(i + 1):

            continuation = discount * (
                p * option_values[j + 1]
                + q * option_values[j]
            )

            # Option européenne
            if exercise_type == "european":

                value = continuation

            # Option américaine
            else:

                S = (
                    S0
                    * (u ** j)
                    * (d ** (i - j))
                )

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

    return option_values[0]