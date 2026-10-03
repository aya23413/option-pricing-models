from pricing.binomial_crr import crr_price
from pricing.binomial_jarrow_rudd import jarrow_rudd_price
from pricing.binomial_tian import tian_price
from pricing.trinomial_boyle import boyle_trinomial_price

from analysis.performance import measure_runtime


# ============================================================
# DEFINITION DES SCENARIOS DE MARCHE
# ============================================================

def get_market_scenarios(option_type="call"):
    """
    Retourne les différents scénarios de marché.

    Les scénarios ITM et OTM sont adaptés automatiquement
    selon qu'il s'agit d'un call ou d'un put.
    """

    option_type = option_type.lower()

    # --------------------------------------------------------
    # Définition de ITM / OTM selon le type d'option
    # --------------------------------------------------------

    if option_type == "call":

        # Call ITM : S0 > K
        S0_itm = 120

        # Call OTM : S0 < K
        S0_otm = 80

    elif option_type == "put":

        # Put ITM : S0 < K
        S0_itm = 80

        # Put OTM : S0 > K
        S0_otm = 120

    else:
        raise ValueError(
            "option_type doit être 'call' ou 'put'"
        )

    # --------------------------------------------------------
    # Scénarios
    # --------------------------------------------------------

    scenarios = {

        "Standard": {
            "S0": 100,
            "K": 100,
            "T": 1,
            "r": 0.05,
            "sigma": 0.20
        },

        "Faible volatilite": {
            "S0": 100,
            "K": 100,
            "T": 1,
            "r": 0.05,
            "sigma": 0.10
        },

        "Forte volatilite": {
            "S0": 100,
            "K": 100,
            "T": 1,
            "r": 0.05,
            "sigma": 0.40
        },

        "ITM": {
            "S0": S0_itm,
            "K": 100,
            "T": 1,
            "r": 0.05,
            "sigma": 0.20
        },

        "OTM": {
            "S0": S0_otm,
            "K": 100,
            "T": 1,
            "r": 0.05,
            "sigma": 0.20
        },

        "Maturite courte": {
            "S0": 100,
            "K": 100,
            "T": 0.25,
            "r": 0.05,
            "sigma": 0.20
        },

        "Maturite longue": {
            "S0": 100,
            "K": 100,
            "T": 2,
            "r": 0.05,
            "sigma": 0.20
        }
    }

    return scenarios


# ============================================================
# ANALYSE DES SCENARIOS
# ============================================================

def scenario_analysis(
    option_type="call",
    exercise_type="european",
    N=100,
    repetitions=10
):
    """
    Analyse les modèles CRR, Jarrow-Rudd, Tian et Boyle
    sur différents scénarios de marché.

    Pour chaque scénario :
    - calcul du prix
    - mesure du temps médian d'exécution
    """

    option_type = option_type.lower()
    exercise_type = exercise_type.lower()

    # --------------------------------------------------------
    # Vérifications
    # --------------------------------------------------------

    if option_type not in ["call", "put"]:
        raise ValueError(
            "option_type doit être 'call' ou 'put'"
        )

    if exercise_type not in ["european", "american"]:
        raise ValueError(
            "exercise_type doit être 'european' ou 'american'"
        )

    if N <= 0:
        raise ValueError(
            "N doit être > 0"
        )

    if repetitions <= 0:
        raise ValueError(
            "repetitions doit être > 0"
        )

    # --------------------------------------------------------
    # Récupération des scénarios
    # IMPORTANT : on transmet option_type
    # --------------------------------------------------------

    scenarios = get_market_scenarios(option_type)

    # --------------------------------------------------------
    # Méthodes de pricing
    # --------------------------------------------------------

    methods = {
        "CRR": crr_price,
        "Jarrow-Rudd": jarrow_rudd_price,
        "Tian": tian_price,
        "Boyle": boyle_trinomial_price
    }

    all_results = {}

    # ========================================================
    # BOUCLE SUR LES SCENARIOS
    # ========================================================

    for scenario_name, params in scenarios.items():

        print("\n")
        print("=" * 70)
        print(f"SCENARIO : {scenario_name.upper()}")
        print("=" * 70)

        print(
            f"S0={params['S0']} | "
            f"K={params['K']} | "
            f"T={params['T']} | "
            f"r={params['r'] * 100:.2f}% | "
            f"sigma={params['sigma'] * 100:.2f}%"
        )

        print("-" * 70)

        print(
            f"{'Méthode':<20}"
            f"{'Prix':<20}"
            f"{'Temps médian (s)':<20}"
        )

        print("-" * 70)

        scenario_results = []

        # ====================================================
        # BOUCLE SUR LES METHODES
        # ====================================================

        for method_name, pricing_function in methods.items():

            runtime = measure_runtime(
                pricing_function=pricing_function,
                S0=params["S0"],
                K=params["K"],
                T=params["T"],
                r=params["r"],
                sigma=params["sigma"],
                N=N,
                option_type=option_type,
                exercise_type=exercise_type,
                repetitions=repetitions
            )

            result = {
                "Méthode": method_name,
                "Prix": runtime["price"],
                "Temps": runtime["median_time"]
            }

            scenario_results.append(result)

            print(
                f"{method_name:<20}"
                f"{runtime['price']:<20.6f}"
                f"{runtime['median_time']:<20.8f}"
            )

        all_results[scenario_name] = scenario_results

    return all_results