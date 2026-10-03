from analysis.performance import measure_runtime


def compare_methods(
    methods,
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
    Compare plusieurs méthodes de pricing.
    """

    results = []

    for name, function in methods.items():

        result = measure_runtime(
            function,
            S0,
            K,
            T,
            r,
            sigma,
            N,
            option_type,
            exercise_type
        )

        results.append({
            "method": name,
            "price": result["price"],
            "time": result["average_time"]
        })

    return results