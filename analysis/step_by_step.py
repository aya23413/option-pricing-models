import math
from pricing.binomial_crr import crr_price


def crr_step_by_step(
    S0,
    K,
    T,
    r,
    sigma,
    N_small=2,
    N_large=100,
    option_type="call",
    exercise_type="european"
):
    """
    Affiche les calculs détaillés du CRR pour un petit N,
    puis compare le résultat au prix CRR pour un grand N.
    """

    # ========================================================
    # VERIFICATION DES PARAMETRES
    # ========================================================

    if N_small < 1 or N_large < 1:
        raise ValueError(
            "Les deux valeurs de N doivent être >= 1."
        )

    if N_small > 10:
        raise ValueError(
            "N_small doit être <= 10 pour afficher l'arbre."
        )

    if S0 <= 0 or K <= 0:
        raise ValueError("S0 et K doivent être > 0.")

    if T <= 0:
        raise ValueError("T doit être > 0.")

    if sigma <= 0:
        raise ValueError("sigma doit être > 0.")

    option_type = option_type.lower()
    exercise_type = exercise_type.lower()

    if option_type not in ("call", "put"):
        raise ValueError(
            "option_type doit être 'call' ou 'put'."
        )

    if exercise_type not in ("european", "american"):
        raise ValueError(
            "exercise_type doit être 'european' ou 'american'."
        )

    # ========================================================
    # 1. PARAMETRES CRR
    # ========================================================

    dt = T / N_small

    u = math.exp(
        sigma * math.sqrt(dt)
    )

    d = math.exp(
        -sigma * math.sqrt(dt)
    )

    p = (
        math.exp(r * dt) - d
    ) / (
        u - d
    )

    q = 1 - p

    discount = math.exp(
        -r * dt
    )

    if not 0 <= p <= 1:
        raise ValueError(
            "Probabilité invalide. Vérifie les paramètres."
        )

    print("\n========== PARAMÈTRES CRR ==========")

    print(f"S0 = {S0}, K = {K}, T = {T}")
    print(f"r = {r}, sigma = {sigma}")
    print(
        f"Option : {option_type}, "
        f"exercice : {exercise_type}"
    )

    print(f"N_small = {N_small}")
    print(f"Delta t = {dt:.6f}")
    print(f"u = {u:.6f}, d = {d:.6f}")
    print(f"p = {p:.6f}, q = {q:.6f}")

    print(
        f"Facteur d'actualisation = "
        f"{discount:.6f}"
    )

    # ========================================================
    # 2. CONSTRUCTION DE L'ARBRE DU SOUS-JACENT
    # ========================================================

    stock_tree = []

    print(
        "\n========== ARBRE DU SOUS-JACENT =========="
    )

    for i in range(N_small + 1):

        level = []

        for j in range(i + 1):

            S = (
                S0
                * (u ** j)
                * (d ** (i - j))
            )

            level.append(S)

        stock_tree.append(level)

        print(
            f"Période {i}: "
            + " | ".join(
                f"{S:.4f}" for S in level
            )
        )

    # ========================================================
    # 3. PAYOFFS A MATURITE
    # ========================================================

    values = []

    print(
        "\n========== PAYOFFS À MATURITÉ =========="
    )

    for S in stock_tree[N_small]:

        if option_type == "call":
            payoff = max(S - K, 0)

        else:
            payoff = max(K - S, 0)

        values.append(payoff)

    print(
        "Payoffs :",
        [round(v, 6) for v in values]
    )

    # ========================================================
    # 4. BACKWARD INDUCTION
    # ========================================================

    print(
        "\n========== BACKWARD INDUCTION =========="
    )

    for i in range(
        N_small - 1,
        -1,
        -1
    ):

        new_values = []

        for j in range(i + 1):

            S = stock_tree[i][j]

            # Valeur de continuation
            continuation = discount * (
                p * values[j + 1]
                + q * values[j]
            )

            # =================================================
            # OPTION EUROPEENNE
            # =================================================

            if exercise_type == "european":

                value = continuation

                print(
                    f"Période {i}, nœud {j}: "
                    f"S={S:.4f}, "
                    f"continuation={continuation:.6f}, "
                    f"valeur={value:.6f}"
                )

            # =================================================
            # OPTION AMERICAINE
            # =================================================

            else:

                if option_type == "call":
                    exercise = max(S - K, 0)

                else:
                    exercise = max(K - S, 0)

                value = max(
                    exercise,
                    continuation
                )

                print(
                    f"Période {i}, nœud {j}: "
                    f"S={S:.4f}, "
                    f"continuation={continuation:.6f}, "
                    f"exercice={exercise:.6f}, "
                    f"valeur={value:.6f}"
                )

            new_values.append(value)

        values = new_values

    # ========================================================
    # 5. PRIX CRR PETIT N
    # ========================================================

    price_small = values[0]

    # ========================================================
    # 6. PRIX CRR GRAND N
    # ========================================================

    price_large = crr_price(
        S0,
        K,
        T,
        r,
        sigma,
        N_large,
        option_type,
        exercise_type
    )

    # ========================================================
    # 7. COMPARAISON
    # ========================================================

    difference = abs(
        price_small - price_large
    )

    print(
        "\n========== COMPARAISON =========="
    )

    print(
        f"Prix CRR, N={N_small} : "
        f"{price_small:.6f}"
    )

    print(
        f"Prix CRR, N={N_large} : "
        f"{price_large:.6f}"
    )

    print(
        f"Écart absolu          : "
        f"{difference:.6f}"
    )

    # ========================================================
    # RESULTATS
    # ========================================================

    return {
        "price_small": price_small,
        "price_large": price_large,
        "difference": difference,
        "stock_tree": stock_tree
    }