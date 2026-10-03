from analysis.performance import measure_runtime


def convergence_study(
    pricing_function,
    S0,
    K,
    T,
    r,
    sigma,
    option_type="call",
    exercise_type="european",
    n_values=None,
    reference_price=None,
    repetitions=10
):
    """
    Etudie la convergence et la performance
    d'une méthode de pricing.

    Pour chaque valeur de N :
    - calcule le prix de l'option
    - mesure le temps d'exécution sur plusieurs répétitions
    - utilise le temps médian comme mesure de performance

    Pour une option européenne :
        une référence peut être fournie afin de calculer
        l'erreur absolue.

    Pour une option américaine :
        aucune référence analytique n'est imposée.
        On étudie le prix, sa stabilisation et
        le temps de calcul.
    """

    if n_values is None:
        n_values = [
            5,
            10,
            25,
            50,
            100,
            200,
            500
        ]

    if repetitions <= 0:
        raise ValueError(
            "repetitions doit être > 0"
        )

    results = []

    for N in n_values:

        # --------------------------------------------
        # Mesure de la performance
        # --------------------------------------------

        runtime = measure_runtime(
            pricing_function=pricing_function,
            S0=S0,
            K=K,
            T=T,
            r=r,
            sigma=sigma,
            N=N,
            option_type=option_type,
            exercise_type=exercise_type,
            repetitions=repetitions
        )

        price = runtime["price"]
        median_time = runtime["median_time"]

        # --------------------------------------------
        # Résultat principal
        # --------------------------------------------

        result = {
            "N": N,
            "Prix": price,
            "Temps": median_time
        }

        # --------------------------------------------
        # Erreur
        # Seulement lorsqu'une référence existe
        # --------------------------------------------

        if reference_price is not None:

            result["Erreur"] = abs(
                price - reference_price
            )

        results.append(result)

    return results