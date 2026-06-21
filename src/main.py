"""Time Series Analysis of air raid alerts in Ukraine — pipeline entry point.

fetch -> preprocess -> visualize -> analyze -> forecast
Outputs PNGs into ../plots and prints metrics to stdout.
"""

import analyze
import fetch_data
import forecast
import preprocess
import visualize


def main() -> None:
    csv_path = fetch_data.load_or_fetch()
    aggregate, by_region = preprocess.build_series(csv_path)

    visualize.timeseries(aggregate)
    visualize.heatmap(by_region)

    analyze.run(aggregate)
    forecast.run(aggregate)


if __name__ == "__main__":
    main()
