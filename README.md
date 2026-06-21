# KSE-agentic-school-application-2026
Stage 2 of KSE AI Agentic Summer School Application - Time Series Analysis of air raid alerts in Ukraine

## Structure
- notes.md - thought process
- src/ - analysis pipeline
  - fetch_data.py - download & cache the dataset
  - preprocess.py - per-oblast daily alert-hours (overlap-merged) + national aggregate
  - analyze.py - ADF stationarity, weekly decomposition, ACF/PACF
  - forecast.py - SARIMA vs Exponential Smoothing, 14-day forecast
  - visualize.py - time series + per-oblast heatmap
  - main.py - runs the full pipeline
  - dashboard.py - Streamlit UI embedding the plots with commentary

## Data
Full history since 2022-03-15 from the [Vadimkin air-raid-sirens dataset](https://github.com/Vadimkin/ukrainian-air-raid-sirens-dataset)
(`official_data_en.csv`)

## Run
```
uv pip install -r requirements.txt
uv run python src/main.py          # build series, save plots/ + metrics.json
uv run streamlit run src/dashboard.py   # browse plots with commentary
```
`main.py` outputs PNG plots to `plots/` and prints ADF + forecast (MAE/RMSE)
metrics. The Streamlit dashboard embeds those plots with per-plot commentary.


```
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠰⡖⠤⣀⡀⡏⢦⠀⡠⠐⢡⠃⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣀⣀⣀⣀⣹⠀⠀⠙⠃⠈⠉⠀⠀⠘⠂⠉⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⢉⡠⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣠⠞⠉⠀⠀⢀⣴⡶⠟⠛⠻⣷⡀⢠⡐⡀⠈⠐⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣶⣶⣾⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣴⡋⠀⠀⠀⠀⣴⠟⠱⡀⠀⠀⢀⣸⡿⠦⣿⣾⣦⠰⡀⠁⠀⠀⠀⠀⡠⠢⣀⣠⣴⣾⣿⣿⣿⣿⡿⠿⠿⠿⠛⠛⠛⠷⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠉⡹⠂⠀⢠⠅⠀⠸⣀⠴⢊⠋⠀⣀⠀⠀⠈⠛⠗⡱⣤⣤⣤⣤⣴⡇⠀⠘⣿⡿⠟⠛⠉⠁⠀⠀⣠⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⡜⠁⡀⠀⢸⣆⣀⡜⠁⠀⠀⠀⠋⠀⢀⡴⠊⠉⣸⠃⠏⠛⠛⠛⠛⡇⠀⠀⢰⠀⠀⠀⠀⣠⣶⣿⣿⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣦⢸⣿⠃⡔⣥⡀⠀⠀⠀⠀⠀⢀⠰⠚⠈⠀⠄⠀⠀⠀⠀⠃⠀⠀⠘⢀⣠⣴⣿⣿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⠻⠻⢌⠉⠉⠀⠀⠀⢀⡴⣋⡤⣧⠀⠆⢋⠰⣦⣤⣤⣤⡄⠀⠀⠀⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠰⠲⡴⠃⠀⣴⣫⣶⡴⠋⠁⠀⠀⢨⣿⡏⠉⢙⢫⢽⠀⠀⠀⢷⣶⣄⣀⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠡⡞⡁⣉⠉⠑⠉⠀⠀⣠⣴⣿⣿⣷⣎⡡⠒⣳⠀⠀⠀⠸⠛⠉⠉⢻⠟⠃⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢓⡀⢀⣀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠘⠀⠀⠀⠘⡄⠀⠀⢃⠉⠢⢄⣀⣠⣤⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⡶⠶⠚⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠑⢇⠀⠀⠀⠐⡀⠀⠈⠆⠀⠀⣸⣿⠿⠛⠛⠛⠉⠉⣉⡤⠖⠊⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣏⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣀⣀⣀⣈⡆⠀⠀⠀⡅⠀⠀⡸⠀⢰⣿⣿⣧⣀⣤⠴⠚⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⡀⠀⠉⠉⣙⠫⠭⠭⠭⢤⠒⣴⢒⢾⠉⠈⡈⡇⠀⠀⢀⠁⠀⣰⡁⣰⠁⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⡤⠒⠉⠐⠆⠀⣠⠄⠀⡏⡠⠿⠜⠒⠃⠹⡀⢀⡠⠆⡀⠔⠁⣨⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⢁⡀⠈⠉⠉⣉⣀⡤⠒⢍⡁⠀⠀⠀⠀⠀⠁⢈⣨⣥⣤⣤⣾⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⡿⣾⣿⣿⣿⣿⣿⠟⣠⠊⠀⠹⣶⣦⣤⣤⣤⣶⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⠿⣿⣿⣿⣿⡇⣿⣿⣿⡿⠋⠀⡔⠁⠀⠀⠀⠈⠙⠻⠿⠿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠉⢹⣿⣷⣿⣿⣿⡇⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠉⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⠀⣸⣿⢧⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠏⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠀⠀⠀⣿⡏⣾⣿⣿⡇⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⢀⡞⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⣿⢷⣿⣿⣿⡇⠀⠀⠀⣠⡴⠃⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠀⠀⠀⢠⣿⢸⣿⣿⣿⣇⣠⣴⡾⠋⠀⠀⠀⠀⠀⠀⠀⠌⠀⠀⠀⢸⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⡆⠀⠛⠶⣾⣿⢸⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠠⠾⠿⠿⠸⠿⠿⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
```