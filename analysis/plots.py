import matplotlib.pyplot as plt
import pandas as pd


# ============================================================
# CONVERSION EN DATAFRAME
# ============================================================

def results_to_dataframe(results):
    """
    Transforme les résultats en DataFrame.
    """
    return pd.DataFrame(results)


# ============================================================
# AFFICHAGE TABLEAU
# ============================================================

def display_table(results, title="Résultats"):

    df = results_to_dataframe(results)

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    formatters = {
        "Prix": "{:.6f}".format,
        "Temps": "{:.8f}".format
    }

    # La colonne Erreur existe seulement lorsqu'une
    # référence a été utilisée.
    if "Erreur" in df.columns:
        formatters["Erreur"] = "{:.6f}".format

    print(
        df.to_string(
            index=False,
            formatters=formatters
        )
    )

    return df


# ============================================================
# UNE SEULE METHODE : PRIX
# ============================================================

def plot_price_convergence(
    results,
    method_name="CRR",
    reference_price=None
):

    df = results_to_dataframe(results)

    plt.figure(figsize=(9, 5))

    plt.plot(
        df["N"],
        df["Prix"],
        marker="o",
        label=method_name
    )

    if reference_price is not None:

        plt.axhline(
            reference_price,
            linestyle="--",
            label="Black-Scholes"
        )

        plt.title(
            f"Convergence du prix {method_name} "
            "vers Black-Scholes"
        )

    else:

        plt.title(
            f"Evolution du prix {method_name} "
            "en fonction de N"
        )

    plt.xlabel("Nombre de pas N")
    plt.ylabel("Prix de l'option")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ============================================================
# UNE SEULE METHODE : ERREUR
# ============================================================

def plot_error_convergence(
    results,
    method_name="CRR"
):

    df = results_to_dataframe(results)

    if "Erreur" not in df.columns:
        raise ValueError(
            "Aucune erreur de référence disponible."
        )

    plt.figure(figsize=(9, 5))

    plt.plot(
        df["N"],
        df["Erreur"],
        marker="o",
        label=method_name
    )

    plt.xlabel("Nombre de pas N")
    plt.ylabel("Erreur absolue")

    plt.title(
        f"Erreur de {method_name} "
        "par rapport à Black-Scholes"
    )

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ============================================================
# UNE SEULE METHODE : TEMPS
# ============================================================

def plot_computation_time(
    results,
    method_name="CRR"
):

    df = results_to_dataframe(results)

    plt.figure(figsize=(9, 5))

    plt.plot(
        df["N"],
        df["Temps"],
        marker="o",
        label=method_name
    )

    plt.xlabel("Nombre de pas N")
    plt.ylabel("Temps médian de calcul (secondes)")

    plt.title(
        f"Temps de calcul de {method_name}"
    )

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ============================================================
# COMPARAISON DES METHODES : PRIX
# ============================================================

def plot_methods_price_comparison(
    results_dict,
    reference_price=None
):

    plt.figure(figsize=(10, 6))

    for method_name, results in results_dict.items():

        df = results_to_dataframe(results)

        plt.plot(
            df["N"],
            df["Prix"],
            marker="o",
            label=method_name
        )

    # Référence analytique seulement lorsqu'elle existe
    if reference_price is not None:

        plt.axhline(
            reference_price,
            linestyle="--",
            label="Black-Scholes"
        )

        plt.title(
            "Convergence des méthodes vers Black-Scholes"
        )

    else:

        plt.title(
            "Evolution des prix en fonction du nombre de pas N"
        )

    plt.xlabel("Nombre de pas N")
    plt.ylabel("Prix de l'option")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ============================================================
# COMPARAISON DES METHODES : ERREUR
# ============================================================

def plot_methods_error_comparison(results_dict):

    plt.figure(figsize=(10, 6))

    for method_name, results in results_dict.items():

        df = results_to_dataframe(results)

        if "Erreur" not in df.columns:
            raise ValueError(
                "Les résultats ne contiennent pas "
                "d'erreur de référence."
            )

        plt.plot(
            df["N"],
            df["Erreur"],
            marker="o",
            label=method_name
        )

    plt.xlabel("Nombre de pas N")
    plt.ylabel("Erreur absolue")

    plt.title(
        "Comparaison des erreurs par rapport à Black-Scholes"
    )

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ============================================================
# COMPARAISON DES METHODES : TEMPS
# ============================================================

def plot_methods_time_comparison(results_dict):

    plt.figure(figsize=(10, 6))

    for method_name, results in results_dict.items():

        df = results_to_dataframe(results)

        plt.plot(
            df["N"],
            df["Temps"],
            marker="o",
            label=method_name
        )

    plt.xlabel("Nombre de pas N")
    plt.ylabel("Temps médian de calcul (secondes)")

    plt.title(
        "Comparaison des temps médians de calcul"
    )

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ============================================================
# SCENARIOS DE MARCHE : PRIX
# ============================================================

def plot_scenario_prices(scenario_results):
    """
    Compare les prix obtenus par les différentes méthodes
    pour chaque scénario de marché.
    """

    scenario_names = list(
        scenario_results.keys()
    )

    methods = [
        "CRR",
        "Jarrow-Rudd",
        "Tian",
        "Boyle"
    ]

    plt.figure(figsize=(12, 6))

    for method in methods:

        prices = []

        for scenario_name in scenario_names:

            results = scenario_results[
                scenario_name
            ]

            price = next(
                result["Prix"]
                for result in results
                if result["Méthode"] == method
            )

            prices.append(price)

        plt.plot(
            scenario_names,
            prices,
            marker="o",
            label=method
        )

    plt.xlabel(
        "Scénarios de marché"
    )

    plt.ylabel(
        "Prix de l'option"
    )

    plt.title(
        "Comparaison des prix selon "
        "les scénarios de marché"
    )

    plt.xticks(
        rotation=25
    )

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ============================================================
# SCENARIOS DE MARCHE : TEMPS
# ============================================================

def plot_scenario_times(scenario_results):
    """
    Compare les temps médians de calcul des différentes
    méthodes pour chaque scénario de marché.
    """

    scenario_names = list(
        scenario_results.keys()
    )

    methods = [
        "CRR",
        "Jarrow-Rudd",
        "Tian",
        "Boyle"
    ]

    plt.figure(figsize=(12, 6))

    for method in methods:

        times = []

        for scenario_name in scenario_names:

            results = scenario_results[
                scenario_name
            ]

            computation_time = next(
                result["Temps"]
                for result in results
                if result["Méthode"] == method
            )

            times.append(
                computation_time
            )

        plt.plot(
            scenario_names,
            times,
            marker="o",
            label=method
        )

    plt.xlabel(
        "Scénarios de marché"
    )

    plt.ylabel(
        "Temps médian de calcul (secondes)"
    )

    plt.title(
        "Comparaison des performances selon "
        "les scénarios de marché"
    )

    plt.xticks(
        rotation=25
    )

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ============================================================
# SAUVEGARDE CSV
# ============================================================

def save_results_csv(results, filename):

    df = results_to_dataframe(results)

    df.to_csv(
        filename,
        index=False
    )

    print(
        f"\nRésultats sauvegardés dans : {filename}"
    )

# ============================================================
# SAUVEGARDE DES SCENARIOS EN CSV
# ============================================================

def save_scenario_results_csv(
    scenario_results,
    filename="scenarios_results.csv"
):
    """
    Sauvegarde les résultats de tous les scénarios
    dans un seul fichier CSV.
    """

    rows = []

    for scenario_name, results in scenario_results.items():

        for result in results:

            rows.append({
                "Scenario": scenario_name,
                "Methode": result["Méthode"],
                "Prix": result["Prix"],
                "Temps": result["Temps"]
            })

    df = pd.DataFrame(rows)

    df.to_csv(
        filename,
        index=False
    )

    print(
        f"\nRésultats des scénarios sauvegardés dans : "
        f"{filename}"
    )

    return df