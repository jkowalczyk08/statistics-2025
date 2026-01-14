import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
import os

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create directory for plots
output_dir = os.path.join(script_dir, "zad1")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load data
data_path = os.path.join(script_dir, 'CH01PR20.txt')
data = np.loadtxt(data_path)
y = data[:, 0]  # Time (hours)
x = data[:, 1]  # Number of copiers

n = len(x)
alpha = 0.05

# --- Part a) Plot and Regression ---
print("--- Część a ---")
# Theoretical
x_mean = np.mean(x)
y_mean = np.mean(y)

numerator = np.sum((x - x_mean) * (y - y_mean))
donominator = np.sum((x - x_mean)**2)

beta_1_teor = numerator / donominator
beta_0_teor = y_mean - beta_1_teor * x_mean

print(f"Teoretyczne beta_0: {beta_0_teor}")
print(f"Teoretyczne beta_1: {beta_1_teor}")

# Built-in
X = sm.add_constant(x)
model = sm.OLS(y, X).fit()
beta_0_lib, beta_1_lib = model.params

print(f"Biblioteczne beta_0: {beta_0_lib}")
print(f"Biblioteczne beta_1: {beta_1_lib}")

print("Sprawdzenie liniowości: Na podstawie wykresu zależność wydaje się być w przybliżeniu liniowa.")

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(x, y, label='Dane')
plt.xlabel('Liczba kopiarek')
plt.ylabel('Czas obsługi (godziny)')
plt.title('Czas obsługi vs Liczba kopiarek (Wykres punktowy)')
plt.legend()
plt.savefig(os.path.join(output_dir, 'plot_a_scatter.png'))

# Add regression line to the same plot or create a new one
plt.plot(x, beta_0_teor + beta_1_teor * x, color='red', label='Linia regresji')
plt.title('Czas obsługi vs Liczba kopiarek z linią regresji')
plt.legend()
plt.savefig(os.path.join(output_dir, 'plot_a.png'))
plt.close()

# --- Part b) 95% Confidence Intervals for Slope and Intercept ---
print("\n--- Część b ---")
# Theoretical
y_pred = beta_0_teor + beta_1_teor * x
sse = np.sum((y - y_pred)**2)
mse = sse / (n - 2)
se_beta_1 = np.sqrt(mse / np.sum((x - x_mean)**2))
se_beta_0 = np.sqrt(mse * (1/n + x_mean**2 / np.sum((x - x_mean)**2)))

t_crit = stats.t.ppf(1 - alpha/2, n - 2)

ci_beta_1_teor = (beta_1_teor - t_crit * se_beta_1, beta_1_teor + t_crit * se_beta_1)
ci_beta_0_teor = (beta_0_teor - t_crit * se_beta_0, beta_0_teor + t_crit * se_beta_0)

print(f"Teoretyczny przedział ufności beta_0: {ci_beta_0_teor}")
print(f"Teoretyczny przedział ufności beta_1: {ci_beta_1_teor}")

# Built-in
ci_lib = model.conf_int(alpha=alpha)
print(f"Biblioteczny przedział ufności beta_0: {ci_lib[0]}")
print(f"Biblioteczny przedział ufności beta_1: {ci_lib[1]}")

# Save table for a) and b)
table_a_b_data = [
    ["Intercept (Beta 0)", "Estymator", f"{beta_0_teor:.6f}", f"{beta_0_lib:.6f}"],
    ["Slope (Beta 1)", "Estymator", f"{beta_1_teor:.6f}", f"{beta_1_lib:.6f}"],
    ["Intercept (Beta 0)", "95% CI", f"({ci_beta_0_teor[0]:.6f}, {ci_beta_0_teor[1]:.6f})", f"[{ci_lib[0][0]:.6f}, {ci_lib[0][1]:.6f}]"],
    ["Slope (Beta 1)", "95% CI", f"({ci_beta_1_teor[0]:.6f}, {ci_beta_1_teor[1]:.6f})", f"[{ci_lib[1][0]:.6f}, {ci_lib[1][1]:.6f}]"]
]
df_a_b = pd.DataFrame(table_a_b_data, columns=["Parametr", "Metryka", "Teoretycznie", "Biblioteka"])
with open(os.path.join(output_dir, 'table_a_b.md'), 'w') as f:
    f.write(df_a_b.to_markdown(index=False))


# --- Part c) Hypothesis Testing ---
print("\n--- Część c ---")
# H0: beta_i = 0, H1: beta_i != 0
# Theoretical
t_stat_beta_0 = beta_0_teor / se_beta_0
t_stat_beta_1 = beta_1_teor / se_beta_1

p_val_beta_0 = 2 * (1 - stats.t.cdf(np.abs(t_stat_beta_0), n - 2))
p_val_beta_1 = 2 * (1 - stats.t.cdf(np.abs(t_stat_beta_1), n - 2))

print(f"Teoretyczna statystyka t dla beta_0: {t_stat_beta_0}, p-wartość: {p_val_beta_0}")
print(f"Teoretyczna statystyka t dla beta_1: {t_stat_beta_1}, p-wartość: {p_val_beta_1}")

# Built-in
print(f"Biblioteczna statystyka t dla beta_0: {model.tvalues[0]}, p-wartość: {model.pvalues[0]}")
print(f"Biblioteczna statystyka t dla beta_1: {model.tvalues[1]}, p-wartość: {model.pvalues[1]}")

# Save table for c)
table_c_data = [
    ["Intercept (Beta 0)", "Statystyka T", f"{t_stat_beta_0:.6f}", f"{model.tvalues[0]:.6f}"],
    ["Intercept (Beta 0)", "p-wartość", f"{p_val_beta_0:.6f}", f"{model.pvalues[0]:.6f}"],
    ["Slope (Beta 1)", "Statystyka T", f"{t_stat_beta_1:.6f}", f"{model.tvalues[1]:.6f}"],
    ["Slope (Beta 1)", "p-wartość", f"{p_val_beta_1:.6e}", f"{model.pvalues[1]:.6e}"]
]
df_c = pd.DataFrame(table_c_data, columns=["Parametr", "Metryka", "Teoretycznie", "Biblioteka"])
with open(os.path.join(output_dir, 'table_c.md'), 'w') as f:
    f.write(df_c.to_markdown(index=False))

# Decisions
print("\nDecyzje:")
if p_val_beta_1 < alpha:
    print(f"Beta 1: p-wartość ({p_val_beta_1:.4e}) < {alpha}. Odrzucamy H0. Istnieje istotna statystycznie zależność liniowa między liczbą kopiarek a czasem obsługi.")
else:
    print(f"Beta 1: p-wartość ({p_val_beta_1:.4e}) >= {alpha}. Brak podstaw do odrzucenia H0.")

if p_val_beta_0 < alpha:
    print(f"Beta 0: p-wartość ({p_val_beta_0:.4f}) < {alpha}. Odrzucamy H0.")
else:
    print(f"Beta 0: p-wartość ({p_val_beta_0:.4f}) >= {alpha}. Brak podstaw do odrzucenia H0. Wyraz wolny nie jest istotnie różny od 0.")


# --- Part d) Expected Value CI for k machines ---
print("\n--- Część d ---")
k_values = [1, 5, 8, 11, 25, 100]
results_d = []

for k in k_values:
    # Theoretical
    y_hat_k = beta_0_teor + beta_1_teor * k
    se_mean_k = np.sqrt(mse * (1/n + (k - x_mean)**2 / np.sum((x - x_mean)**2)))
    ci_mean_lower = y_hat_k - t_crit * se_mean_k
    ci_mean_upper = y_hat_k + t_crit * se_mean_k
    
    # Built-in
    pred = model.get_prediction([1, k])
    ci_mean_lib = pred.conf_int(obs=False, alpha=alpha) # obs=False for mean response CI
    
    results_d.append({
        'k': k,
        'Oczekiwana (Teor)': y_hat_k,
        'CI Średnia Dolna (Teor)': ci_mean_lower,
        'CI Średnia Górna (Teor)': ci_mean_upper,
        'Długość CI': ci_mean_upper - ci_mean_lower,
        'Oczekiwana (Bibl)': pred.predicted_mean[0],
        'CI Średnia Dolna (Bibl)': ci_mean_lib[0][0],
        'CI Średnia Górna (Bibl)': ci_mean_lib[0][1]
    })

df_d = pd.DataFrame(results_d)
print(df_d[['k', 'Oczekiwana (Teor)', 'CI Średnia Dolna (Teor)', 'CI Średnia Górna (Teor)', 'Długość CI']])
print("Uwaga: Długość przedziału ufności rośnie w miarę oddalania się k od średniej x.")

# Save table to markdown
with open(os.path.join(output_dir, 'table_d.md'), 'w') as f:
    f.write(df_d.to_markdown(index=False))

# --- Part e) Prediction Interval for k machines ---
print("\n--- Część e ---")
results_e = []

for k in k_values:
    # Theoretical
    y_hat_k = beta_0_teor + beta_1_teor * k
    se_pred_k = np.sqrt(mse * (1 + 1/n + (k - x_mean)**2 / np.sum((x - x_mean)**2)))
    pi_lower = y_hat_k - t_crit * se_pred_k
    pi_upper = y_hat_k + t_crit * se_pred_k
    
    # Built-in
    pred = model.get_prediction([1, k])
    pi_lib = pred.conf_int(obs=True, alpha=alpha) # obs=True for prediction interval
    
    results_e.append({
        'k': k,
        'Przewidywana (Teor)': y_hat_k,
        'PI Dolna (Teor)': pi_lower,
        'PI Górna (Teor)': pi_upper,
        'Długość PI': pi_upper - pi_lower,
        'Przewidywana (Bibl)': pred.predicted_mean[0],
        'PI Dolna (Bibl)': pi_lib[0][0],
        'PI Górna (Bibl)': pi_lib[0][1]
    })

df_e = pd.DataFrame(results_e)
print(df_e[['k', 'Przewidywana (Teor)', 'PI Dolna (Teor)', 'PI Górna (Teor)', 'Długość PI']])
print("Uwaga: Długość przedziału predykcyjnego jest zawsze większa niż przedziału ufności i również rośnie w miarę oddalania się k od średniej x.")

# Save table to markdown
with open(os.path.join(output_dir, 'table_e.md'), 'w') as f:
    f.write(df_e.to_markdown(index=False))

# --- Part f) Plot with intervals ---
print("\n--- Część f ---")
# Sort x for plotting lines
sort_idx = np.argsort(x)
x_sorted = x[sort_idx]

x_grid = np.linspace(min(x), max(x), 100)
X_grid = sm.add_constant(x_grid)
predictions = model.get_prediction(X_grid)
pred_summary = predictions.summary_frame(alpha=alpha)

plt.figure(figsize=(10, 6))
plt.scatter(x, y, label='Dane', color='blue')
plt.plot(x_grid, pred_summary['mean'], color='red', label='Linia regresji')

# Mean response CI
plt.plot(x_grid, pred_summary['mean_ci_lower'], color='green', linestyle='--', label='95% CI (Średnia)')
plt.plot(x_grid, pred_summary['mean_ci_upper'], color='green', linestyle='--')

# Prediction Interval
plt.plot(x_grid, pred_summary['obs_ci_lower'], color='orange', linestyle=':', label='95% PI (Obs)')
plt.plot(x_grid, pred_summary['obs_ci_upper'], color='orange', linestyle=':')

plt.xlabel('Liczba kopiarek')
plt.ylabel('Czas obsługi (godziny)')
plt.title('Regresja z 95% przedziałami ufności i predykcji')
plt.legend()
plt.savefig(os.path.join(output_dir, 'plot_f.png'))
plt.close()

print("Wykres zapisano w zad1/plot_f.png")