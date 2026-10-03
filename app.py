from flask import Flask, render_template, request

import time


from pricing.binomial_crr import crr_price

from pricing.binomial_jarrow_rudd import jarrow_rudd_price

from pricing.binomial_tian import tian_price

from pricing.trinomial_boyle import boyle_trinomial_price

from analysis.step_by_step import crr_step_by_step

from analysis.convergence import convergence_study

from analysis.scenarios import scenario_analysis


app = Flask(__name__)


# ============================================================

# FONCTIONS UTILITAIRES

# ============================================================


def get_default_form():

    return {

        "S0": 100,

        "K": 100,

        "T": 1,

        "r": 5,

        "sigma": 20,

        "N": 100,

        "option_type": "call",

        "exercise_type": "european"

    }


def validate_parameters(

    S0,

    K,

    T,

    sigma,

    N,

    option_type,

    exercise_type

):

    if S0 <= 0:

        raise ValueError(

            "Le prix du sous-jacent doit être strictement positif."

        )


    if K <= 0:

        raise ValueError(

            "Le prix d'exercice doit être strictement positif."

        )


    if T <= 0:

        raise ValueError(

            "La maturité doit être strictement positive."

        )


    if sigma <= 0:

        raise ValueError(

            "La volatilité doit être strictement positive."

        )


    if N <= 0:

        raise ValueError(

            "Le nombre de pas doit être supérieur à 0."

        )


    if option_type not in ["call", "put"]:

        raise ValueError(

            "Le type d'option est invalide."

        )


    if exercise_type not in ["european", "american"]:

        raise ValueError(

            "Le style d'exercice est invalide."

        )


# ============================================================

# 1. VALORISATION

# ============================================================


@app.route("/", methods=["GET", "POST"])

def index():


    form_data = get_default_form()


    results = None

    crr_tree = None

    error_message = None


    if request.method == "POST":


        try:


            S0 = float(request.form["S0"])

            K = float(request.form["K"])

            T = float(request.form["T"])


            r_percent = float(request.form["r"])

            sigma_percent = float(request.form["sigma"])


            N = int(request.form["N"])


            option_type = request.form[

                "option_type"

            ].lower()


            exercise_type = request.form[

                "exercise_type"

            ].lower()


            form_data = {

                "S0": S0,

                "K": K,

                "T": T,

                "r": r_percent,

                "sigma": sigma_percent,

                "N": N,

                "option_type": option_type,

                "exercise_type": exercise_type

            }


            r = r_percent / 100

            sigma = sigma_percent / 100


            validate_parameters(

                S0,

                K,

                T,

                sigma,

                N,

                option_type,

                exercise_type

            )


            # ------------------------------------------------

            # CRR

            # ------------------------------------------------


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


            crr_time = time.perf_counter() - start


            # ------------------------------------------------
            # ARBRE CRR PEDAGOGIQUE - N = 2
            # ------------------------------------------------

            crr_tree = crr_step_by_step(

                    S0=S0,

                    K=K,

                    T=T,

                    r=r,

                    sigma=sigma,

                    N_small=2,

                    N_large=N,

                    option_type=option_type,

                    exercise_type=exercise_type

            )


            # ------------------------------------------------

            # JARROW-RUDD

            # ------------------------------------------------


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


            jr_time = time.perf_counter() - start


            # ------------------------------------------------

            # TIAN

            # ------------------------------------------------


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


            tian_time = time.perf_counter() - start


            # ------------------------------------------------

            # BOYLE

            # ------------------------------------------------


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


            boyle_time = time.perf_counter() - start


            results = {

                "crr": {

                    "name": "CRR",

                    "price": crr,

                    "time": crr_time

                },

                "jr": {

                    "name": "Jarrow-Rudd",

                    "price": jr,

                    "time": jr_time

                },

                "tian": {

                    "name": "Tian",

                    "price": tian,

                    "time": tian_time

                },

                "boyle": {

                    "name": "Boyle",

                    "price": boyle,

                    "time": boyle_time

                }

            }


            # ------------------------------------------------

            # BLACK-SCHOLES

            # SEULEMENT POUR UNE EUROPEENNE

            # ------------------------------------------------


            if exercise_type == "european":


                from pricing.black_scholes import (

                    black_scholes_price

                )


                bs_price = black_scholes_price(

                    S0,

                    K,

                    T,

                    r,

                    sigma,

                    option_type

                )


                results["black_scholes"] = {

                    "name": "Black-Scholes",

                    "price": bs_price

                }


                results["crr"]["error"] = abs(

                    crr - bs_price

                )


                results["jr"]["error"] = abs(

                    jr - bs_price

                )


                results["tian"]["error"] = abs(

                    tian - bs_price

                )


                results["boyle"]["error"] = abs(

                    boyle - bs_price

                )


        except Exception as error:

            error_message = str(error)


    return render_template(

        "index.html",

        form_data=form_data,

        results=results,

        crr_tree=crr_tree,

        error_message=error_message

    )


# ============================================================

# 2. CONVERGENCE

# ============================================================


@app.route(

    "/convergence",

    methods=["GET", "POST"]

)

def convergence():


    form_data = get_default_form()


    results_dict = None

    reference_price = None

    error_message = None


    n_values = [

        5,

        10,

        25,

        50,

        100,

        200,

        500

    ]


    if request.method == "POST":


        try:


            S0 = float(request.form["S0"])

            K = float(request.form["K"])

            T = float(request.form["T"])


            r_percent = float(request.form["r"])

            sigma_percent = float(

                request.form["sigma"]

            )


            option_type = request.form[

                "option_type"

            ].lower()


            exercise_type = request.form[

                "exercise_type"

            ].lower()


            form_data = {

                "S0": S0,

                "K": K,

                "T": T,

                "r": r_percent,

                "sigma": sigma_percent,

                "N": 100,

                "option_type": option_type,

                "exercise_type": exercise_type

            }


            r = r_percent / 100

            sigma = sigma_percent / 100


            validate_parameters(

                S0,

                K,

                T,

                sigma,

                100,

                option_type,

                exercise_type

            )


            # ------------------------------------------------

            # REFERENCE

            # ------------------------------------------------


            if exercise_type == "european":


                from pricing.black_scholes import (

                    black_scholes_price

                )


                reference_price = black_scholes_price(

                    S0,

                    K,

                    T,

                    r,

                    sigma,

                    option_type

                )


            # ------------------------------------------------

            # CONVERGENCE DES 4 METHODES

            # ------------------------------------------------


            results_crr = convergence_study(

                pricing_function=crr_price,

                S0=S0,

                K=K,

                T=T,

                r=r,

                sigma=sigma,

                option_type=option_type,

                exercise_type=exercise_type,

                n_values=n_values,

                reference_price=reference_price

            )


            results_jr = convergence_study(

                pricing_function=jarrow_rudd_price,

                S0=S0,

                K=K,

                T=T,

                r=r,

                sigma=sigma,

                option_type=option_type,

                exercise_type=exercise_type,

                n_values=n_values,

                reference_price=reference_price

            )


            results_tian = convergence_study(

                pricing_function=tian_price,

                S0=S0,

                K=K,

                T=T,

                r=r,

                sigma=sigma,

                option_type=option_type,

                exercise_type=exercise_type,

                n_values=n_values,

                reference_price=reference_price

            )


            results_boyle = convergence_study(

                pricing_function=boyle_trinomial_price,

                S0=S0,

                K=K,

                T=T,

                r=r,

                sigma=sigma,

                option_type=option_type,

                exercise_type=exercise_type,

                n_values=n_values,

                reference_price=reference_price

            )


            results_dict = {

                "CRR": results_crr,

                "Jarrow-Rudd": results_jr,

                "Tian": results_tian,

                "Boyle": results_boyle

            }


        except Exception as error:

            error_message = str(error)


    return render_template(

        "convergence.html",

        form_data=form_data,

        results_dict=results_dict,

        reference_price=reference_price,

        error_message=error_message

    )


# ============================================================

# 3. SCENARIOS DE MARCHE

# ============================================================


@app.route(

    "/scenarios",

    methods=["GET", "POST"]

)

def scenarios():


    form_data = {

        "N": 100,

        "option_type": "call",

        "exercise_type": "european"

    }


    results = None

    error_message = None


    if request.method == "POST":


        try:


            N = int(request.form["N"])


            option_type = request.form[

                "option_type"

            ].lower()


            exercise_type = request.form[

                "exercise_type"

            ].lower()


            form_data = {

                "N": N,

                "option_type": option_type,

                "exercise_type": exercise_type

            }


            if N <= 0:

                raise ValueError(

                    "Le nombre de pas doit être "

                    "supérieur à 0."

                )


            if option_type not in [

                "call",

                "put"

            ]:

                raise ValueError(

                    "Le type d'option est invalide."

                )


            if exercise_type not in [

                "european",

                "american"

            ]:

                raise ValueError(

                    "Le style d'exercice est invalide."

                )


            results = scenario_analysis(

                option_type=option_type,

                exercise_type=exercise_type,

                N=N,

                repetitions=10

            )


        except Exception as error:

            error_message = str(error)


    return render_template(

        "scenarios.html",

        form_data=form_data,

        results=results,

        error_message=error_message

    )


# ============================================================

# LANCEMENT

# ============================================================


if __name__ == "__main__":


    app.run(

        debug=True

    )