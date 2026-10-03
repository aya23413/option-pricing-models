# ============================================================
# MAIN.PY
# Projet : Pricing et analyse des options vanilles
# ============================================================

import time

from pricing.black_scholes import black_scholes_price
from pricing.binomial_crr import crr_price

from pricing.binomial_jarrow_rudd import (
    jarrow_rudd_price,
    jarrow_rudd_parameters
)

from pricing.binomial_tian import (
    tian_price,
    tian_parameters
)

from pricing.trinomial_boyle import (
    boyle_trinomial_price,
    boyle_parameters
)

from analysis.step_by_step import crr_step_by_step
from analysis.convergence import convergence_study
from analysis.scenarios import scenario_analysis

from analysis.plots import (
    display_table,
    plot_methods_price_comparison,
    plot_methods_error_comparison,
    plot_methods_time_comparison,
    plot_scenario_prices,
    plot_scenario_times,
    save_results_csv,
    save_scenario_results_csv
)


# ============================================================
# PARAMETRES DE L'OPTION
# ============================================================

S0 = 100
K = 100
T = 1
r = 0.05
sigma = 0.20

# "call" ou "put"
option_type = "put"

# "european" ou "american"
exercise_type = "american"

# Grand nombre de pas
N = 100

# Petit nombre de pas pour l'étude détaillée CRR
N_small = 2


# ============================================================
# VALIDATION
# ============================================================

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


# ============================================================
# AFFICHAGE DES PARAMETRES
# ============================================================

print("\n")
print("=" * 70)
print("         PRICING ET ANALYSE DES OPTIONS VANILLES")
print("=" * 70)

print("\nPARAMETRES DE L'OPTION")
print("-" * 70)

print(f"Prix initial S0       : {S0}")
print(f"Strike K              : {K}")
print(f"Maturité T            : {T} an(s)")
print(f"Taux sans risque r    : {r * 100:.2f}%")
print(f"Volatilité sigma      : {sigma * 100:.2f}%")
print(f"Type                  : {option_type.upper()}")
print(f"Style                 : {exercise_type.upper()}")
print(f"Grand N               : {N}")
print(f"Petit N détaillé      : {N_small}")


# ============================================================
# 1. BLACK-SCHOLES
# UNIQUEMENT POUR LES OPTIONS EUROPEENNES
# ============================================================

bs_price = None

if exercise_type == "european":

    print("\n")
    print("=" * 70)
    print("                    BLACK-SCHOLES")
    print("=" * 70)

    bs_price = black_scholes_price(
        S0,
        K,
        T,
        r,
        sigma,
        option_type
    )

    print(
        f"\nPrix Black-Scholes : {bs_price:.6f}"
    )


# ============================================================
# 2. CRR - GRAND N
# ============================================================

print("\n")
print("=" * 70)
print(f"                     CRR - N = {N}")
print("=" * 70)

start = time.perf_counter()

crr = crr_price(
    S0,
    K,
    T,
    r,
    sigma,
    N,
    option_type,
    exercise_type
)

end = time.perf_counter()

crr_time = end - start

print(f"\nPrix CRR          : {crr:.6f}")

print(
    f"Temps de calcul   : "
    f"{crr_time:.8f} seconde(s)"
)


# ============================================================
# 3. CRR - PETIT N : CALCUL DETAILLE
# ============================================================

print("\n")
print("=" * 70)
print(f"               CRR PAS A PAS - N = {N_small}")
print("=" * 70)

crr_details = crr_step_by_step(
    S0=S0,
    K=K,
    T=T,
    r=r,
    sigma=sigma,
    N_small=N_small,
    N_large=N,
    option_type=option_type,
    exercise_type=exercise_type
)


# ============================================================
# 4. JARROW-RUDD
# ============================================================

print("\n")
print("=" * 70)
print(f"                 JARROW-RUDD - N = {N}")
print("=" * 70)

jr_params = jarrow_rudd_parameters(
    T=T,
    r=r,
    sigma=sigma,
    N=N
)

print("\nPARAMETRES JARROW-RUDD")
print("-" * 70)

print(
    f"Delta t                : "
    f"{jr_params['dt']:.6f}"
)

print(
    f"Facteur de hausse u    : "
    f"{jr_params['u']:.6f}"
)

print(
    f"Facteur de baisse d    : "
    f"{jr_params['d']:.6f}"
)

print(
    f"Probabilité hausse p   : "
    f"{jr_params['p']:.6f}"
)

print(
    f"Probabilité baisse q   : "
    f"{jr_params['q']:.6f}"
)

print(
    f"Facteur actualisation  : "
    f"{jr_params['discount']:.6f}"
)

start = time.perf_counter()

jr = jarrow_rudd_price(
    S0,
    K,
    T,
    r,
    sigma,
    N,
    option_type,
    exercise_type
)

end = time.perf_counter()

jr_time = end - start

print("\nRESULTAT JARROW-RUDD")
print("-" * 70)

print(
    f"Prix Jarrow-Rudd       : {jr:.6f}"
)

print(
    f"Temps de calcul        : "
    f"{jr_time:.8f} seconde(s)"
)


# ============================================================
# 5. TIAN
# ============================================================

print("\n")
print("=" * 70)
print(f"                      TIAN - N = {N}")
print("=" * 70)

tian_params = tian_parameters(
    T=T,
    r=r,
    sigma=sigma,
    N=N
)

print("\nPARAMETRES TIAN")
print("-" * 70)

print(
    f"Delta t                : "
    f"{tian_params['dt']:.6f}"
)

print(
    f"Facteur sans risque R  : "
    f"{tian_params['R']:.6f}"
)

print(
    f"Facteur variance V     : "
    f"{tian_params['V']:.6f}"
)

print(
    f"Facteur de hausse u    : "
    f"{tian_params['u']:.6f}"
)

print(
    f"Facteur de baisse d    : "
    f"{tian_params['d']:.6f}"
)

print(
    f"Probabilité hausse p   : "
    f"{tian_params['p']:.6f}"
)

print(
    f"Probabilité baisse q   : "
    f"{tian_params['q']:.6f}"
)

print(
    f"Facteur actualisation  : "
    f"{tian_params['discount']:.6f}"
)

start = time.perf_counter()

tian = tian_price(
    S0,
    K,
    T,
    r,
    sigma,
    N,
    option_type,
    exercise_type
)

end = time.perf_counter()

tian_time = end - start

print("\nRESULTAT TIAN")
print("-" * 70)

print(
    f"Prix Tian              : {tian:.6f}"
)

print(
    f"Temps de calcul        : "
    f"{tian_time:.8f} seconde(s)"
)


# ============================================================
# 6. TRINOMIAL BOYLE
# ============================================================

print("\n")
print("=" * 70)
print(f"                TRINOMIAL BOYLE - N = {N}")
print("=" * 70)

boyle_params = boyle_parameters(
    T=T,
    r=r,
    sigma=sigma,
    N=N
)

print("\nPARAMETRES BOYLE")
print("-" * 70)

print(
    f"Delta t                : "
    f"{boyle_params['dt']:.6f}"
)

print(
    f"Facteur de hausse u    : "
    f"{boyle_params['u']:.6f}"
)

print(
    f"Facteur médian m       : "
    f"{boyle_params['m']:.6f}"
)

print(
    f"Facteur de baisse d    : "
    f"{boyle_params['d']:.6f}"
)

print(
    f"Probabilité hausse pu  : "
    f"{boyle_params['pu']:.6f}"
)

print(
    f"Probabilité milieu pm  : "
    f"{boyle_params['pm']:.6f}"
)

print(
    f"Probabilité baisse pd  : "
    f"{boyle_params['pd']:.6f}"
)

print(
    f"Facteur actualisation  : "
    f"{boyle_params['discount']:.6f}"
)

start = time.perf_counter()

boyle = boyle_trinomial_price(
    S0,
    K,
    T,
    r,
    sigma,
    N,
    option_type,
    exercise_type
)

end = time.perf_counter()

boyle_time = end - start

print("\nRESULTAT BOYLE")
print("-" * 70)

print(
    f"Prix Boyle             : {boyle:.6f}"
)

print(
    f"Temps de calcul        : "
    f"{boyle_time:.8f} seconde(s)"
)


# ============================================================
# 7. TABLEAU COMPARATIF POUR N FIXE
# ============================================================

print("\n")
print("=" * 70)
print(f"                 COMPARAISON - N = {N}")
print("=" * 70)


# ============================================================
# OPTION EUROPEENNE
# ============================================================

if exercise_type == "european":

    print(
        f"{'Méthode':<20}"
        f"{'Prix':<18}"
        f"{'Erreur BS':<18}"
        f"{'Temps (s)':<15}"
    )

    print("-" * 70)

    print(
        f"{'Black-Scholes':<20}"
        f"{bs_price:<18.6f}"
        f"{'-':<18}"
        f"{'-':<15}"
    )

    print(
        f"{'CRR':<20}"
        f"{crr:<18.6f}"
        f"{abs(crr - bs_price):<18.6f}"
        f"{crr_time:<15.8f}"
    )

    print(
        f"{'Jarrow-Rudd':<20}"
        f"{jr:<18.6f}"
        f"{abs(jr - bs_price):<18.6f}"
        f"{jr_time:<15.8f}"
    )

    print(
        f"{'Tian':<20}"
        f"{tian:<18.6f}"
        f"{abs(tian - bs_price):<18.6f}"
        f"{tian_time:<15.8f}"
    )

    print(
        f"{'Boyle':<20}"
        f"{boyle:<18.6f}"
        f"{abs(boyle - bs_price):<18.6f}"
        f"{boyle_time:<15.8f}"
    )


# ============================================================
# OPTION AMERICAINE
# ============================================================

else:

    print(
        f"{'Méthode':<20}"
        f"{'Prix':<18}"
        f"{'Temps (s)':<15}"
    )

    print("-" * 53)

    print(
        f"{'CRR':<20}"
        f"{crr:<18.6f}"
        f"{crr_time:<15.8f}"
    )

    print(
        f"{'Jarrow-Rudd':<20}"
        f"{jr:<18.6f}"
        f"{jr_time:<15.8f}"
    )

    print(
        f"{'Tian':<20}"
        f"{tian:<18.6f}"
        f"{tian_time:<15.8f}"
    )

    print(
        f"{'Boyle':<20}"
        f"{boyle:<18.6f}"
        f"{boyle_time:<15.8f}"
    )


# ============================================================
# 8. ETUDE COMPARATIVE DE CONVERGENCE
# ============================================================

print("\n")
print("=" * 70)
print("          ETUDE COMPARATIVE DE CONVERGENCE")
print("=" * 70)

n_values = [
    5,
    10,
    25,
    50,
    100,
    200,
    500
]


# ============================================================
# REFERENCE
# ============================================================

if exercise_type == "european":
    reference_price = bs_price
else:
    reference_price = None


# ============================================================
# CRR
# ============================================================

results_crr = convergence_study(
    pricing_function=crr_price,
    reference_price=reference_price,
    S0=S0,
    K=K,
    T=T,
    r=r,
    sigma=sigma,
    option_type=option_type,
    exercise_type=exercise_type,
    n_values=n_values
)


# ============================================================
# JARROW-RUDD
# ============================================================

results_jr = convergence_study(
    pricing_function=jarrow_rudd_price,
    reference_price=reference_price,
    S0=S0,
    K=K,
    T=T,
    r=r,
    sigma=sigma,
    option_type=option_type,
    exercise_type=exercise_type,
    n_values=n_values
)


# ============================================================
# TIAN
# ============================================================

results_tian = convergence_study(
    pricing_function=tian_price,
    reference_price=reference_price,
    S0=S0,
    K=K,
    T=T,
    r=r,
    sigma=sigma,
    option_type=option_type,
    exercise_type=exercise_type,
    n_values=n_values
)


# ============================================================
# BOYLE
# ============================================================

results_boyle = convergence_study(
    pricing_function=boyle_trinomial_price,
    reference_price=reference_price,
    S0=S0,
    K=K,
    T=T,
    r=r,
    sigma=sigma,
    option_type=option_type,
    exercise_type=exercise_type,
    n_values=n_values
)


# ============================================================
# 9. TABLEAUX DE CONVERGENCE
# ============================================================

display_table(
    results_crr,
    title="CONVERGENCE CRR"
)

display_table(
    results_jr,
    title="CONVERGENCE JARROW-RUDD"
)

display_table(
    results_tian,
    title="CONVERGENCE TIAN"
)

display_table(
    results_boyle,
    title="CONVERGENCE BOYLE"
)


# ============================================================
# 10. DICTIONNAIRE DES RESULTATS
# ============================================================

results_dict = {
    "CRR": results_crr,
    "Jarrow-Rudd": results_jr,
    "Tian": results_tian,
    "Boyle": results_boyle
}


# ============================================================
# 11. GRAPHIQUE COMPARATIF : PRIX VS N
# ============================================================

print(
    "\nGénération du graphique comparatif : "
    "Prix vs N..."
)

plot_methods_price_comparison(
    results_dict,
    reference_price=reference_price
)


# ============================================================
# 12. GRAPHIQUE COMPARATIF : ERREUR VS N
# UNIQUEMENT POUR LES OPTIONS EUROPEENNES
# ============================================================

if exercise_type == "european":

    print(
        "\nGénération du graphique comparatif : "
        "Erreur vs N..."
    )

    plot_methods_error_comparison(
        results_dict
    )


# ============================================================
# 13. GRAPHIQUE COMPARATIF : TEMPS VS N
# ============================================================

print(
    "\nGénération du graphique comparatif : "
    "Temps de calcul vs N..."
)

plot_methods_time_comparison(
    results_dict
)


# ============================================================
# 14. EXPORT DES RESULTATS DE CONVERGENCE
# ============================================================

save_results_csv(
    results_crr,
    "crr_convergence.csv"
)

save_results_csv(
    results_jr,
    "jarrow_rudd_convergence.csv"
)

save_results_csv(
    results_tian,
    "tian_convergence.csv"
)

save_results_csv(
    results_boyle,
    "boyle_convergence.csv"
)


# ============================================================
# 15. ANALYSE DES SCENARIOS DE MARCHE
# ============================================================

print("\n")
print("=" * 70)
print("             ANALYSE DES SCENARIOS DE MARCHE")
print("=" * 70)

scenario_results = scenario_analysis(
    option_type=option_type,
    exercise_type=exercise_type,
    N=N,
    repetitions=10
)


# ============================================================
# 16. GRAPHIQUE DES PRIX PAR SCENARIO
# ============================================================

print(
    "\nGénération du graphique : "
    "Prix selon les scénarios..."
)

plot_scenario_prices(
    scenario_results
)


# ============================================================
# 17. GRAPHIQUE DES TEMPS PAR SCENARIO
# ============================================================

print(
    "\nGénération du graphique : "
    "Temps de calcul selon les scénarios..."
)

plot_scenario_times(
    scenario_results
)

# ============================================================
# 18. EXPORT DES SCENARIOS EN CSV
# ============================================================

save_scenario_results_csv(
    scenario_results,
    "scenarios_results.csv"
)


# ============================================================
# FIN
# ============================================================

print("\n")
print("=" * 70)
print("                    ANALYSE TERMINEE")
print("=" * 70)

print("\nRésultats sauvegardés dans :")
print("- crr_convergence.csv")
print("- jarrow_rudd_convergence.csv")
print("- tian_convergence.csv")
print("- boyle_convergence.csv")
print("- scenarios_results.csv")

print("\nProgramme terminé.")

