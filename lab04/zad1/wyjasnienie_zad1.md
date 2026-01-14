# Wyjaśnienie rozwiązania Zadania 1 (Regresja Liniowa Prosta)

Poniżej znajduje się szczegółowy opis matematyczny oraz implementacyjny każdego podpunktu z zadania 1.

## Wstęp: Model Regresji Liniowej
Rozważamy model regresji liniowej prostej:
$$ Y_i = \beta_0 + \beta_1 X_i + \epsilon_i $$
gdzie:
- $Y_i$ to zmienna zależna (czas obsługi),
- $X_i$ to zmienna niezależna (liczba maszyn),
- $\beta_0$ to wyraz wolny (intercept),
- $\beta_1$ to współczynnik kierunkowy (slope),
- $\epsilon_i$ to błąd losowy, zakładamy $\epsilon_i \sim N(0, \sigma^2)$.

---

## Podpunkt a) Estymacja parametrów i wykres

### Teoria (Wzory)
Metoda Najmniejszych Kwadratów (MNK) minimalizuje sumę kwadratów błędów ($SSE$). Estymatory wyrażają się wzorami:

1. **Współczynnik kierunkowy ($\\hat{\\beta}_1$):**
   $$ \\hat{\\beta}_1 = \frac{\\sum_{i=1}^n (X_i - \\bar{X})(Y_i - \\bar{Y})}{\\sum_{i=1}^n (X_i - \\bar{X})^2} $$
   
2. **Wyraz wolny ($\\hat{\\beta}_0$):**
   $$ \\hat{\\beta}_0 = \\bar{Y} - \\hat{\\beta}_1 \\bar{X} $$

### Implementacja w kodzie
- **Teoretycznie:** Obliczamy średnie `np.mean(x)` i `np.mean(y)`, a następnie ręcznie implementujemy powyższe sumy.
- **Bibliotecznie:** Używamy `statsmodels.api.OLS`. Funkcja ta wykonuje to samo pod spodem. Ważne jest dodanie stałej `sm.add_constant(x)`, ponieważ macierz $X$ w algebrze liniowej musi mieć kolumnę jedynek, aby uwzględnić $\\beta_0$.

---

## Podpunkt b) Przedziały ufności dla $\\beta_0$ i $\\beta_1$

### Teoria
Aby zbudować przedział ufności, musimy znać wariancję błędu. Estymujemy ją za pomocą **Błędu Średniokwadratowego (MSE)**:
$$ s^2 = MSE = \frac{SSE}{n-2} = \frac{\\sum (Y_i - \\hat{Y}_i)^2}{n-2} $$

Następnie obliczamy błędy standardowe estymatorów:
1. $$ s(\\hat{\\beta}_1) = \sqrt{\\frac{MSE}{\\sum (X_i - \\bar{X})^2}} $$
2. $$ s(\\hat{\\beta}_0) = \sqrt{MSE \\left( \\frac{1}{n} + \\frac{\\bar{X}^2}{\\sum (X_i - \\bar{X})^2} \\right)} $$

Przedział ufności na poziomie $(1-\\alpha)$ to:
$$ \\hat{\\beta}_k \\pm t_{(1-\\alpha/2, n-2)} \\cdot s(\\hat{\\beta}_k) $$
gdzie $t_{(1-\\alpha/2, n-2)}$ to kwantyl rozkładu t-Studenta z $n-2$ stopniami swobody.

### Implementacja
- Obliczamy `sse`, potem `mse`.
- Wyznaczamy `t_crit` używając `scipy.stats.t.ppf`.
- Biblioteka `statsmodels` robi to automatycznie metodą `model.conf_int()`.

---

## Podpunkt c) Testowanie hipotez

### Teoria
Testujemy hipotezy o istotności współczynników:
- $H_0: \\beta_i = 0$ (parametr nie jest istotny / brak zależności)
- $H_1: \\beta_i \\neq 0$ (parametr jest istotny)

**Statystyka testowa T:**
$$ t^* = \frac{\\hat{\\beta}_i}{s(\\hat{\\beta}_i)} $$

Jeśli $H_0$ jest prawdziwa, statystyka ta ma rozkład t-Studenta z $n-2$ stopniami swobody.
**P-wartość (p-value):** Prawdopodobieństwo zaobserwowania wartości co najmniej tak skrajnej jak $t^*$, przy założeniu $H_0$. Dla testu dwustronnego:
$$ p = 2 \\cdot (1 - F_{t(n-2)}(|t^*|)) $$
gdzie $F$ to dystrybuanta.

### Wnioski z zadania
- Dla $\\beta_1$ (liczba maszyn) p-value wyszło bardzo małe ($\\approx 0$), więc **odrzucamy $H_0$**. Istnieje istotna statystycznie zależność liniowa.
- Dla $\\beta_0$ (intercept) p-value wyszło duże ($\\approx 0.84$), więc **nie mamy podstaw do odrzucenia $H_0$**. Oznacza to, że prosta regresji może przechodzić przez początek układu współrzędnych (teoretycznie 0 maszyn = 0 czasu pracy, co ma sens fizyczny).

---

## Podpunkt d) Przedział ufności dla wartości oczekiwanej ($E[Y_h]$)

### Teoria
Chcemy oszacować **średni** czas obsługi dla ustalonej liczby maszyn $X_h = k$.
Punktowa estymata: $\\hat{Y}_h = \\hat{\\beta}_0 + \\hat{\\beta}_1 X_h$.

Błąd standardowy tej estymaty zależy od tego, jak daleko $X_h$ jest od średniej $\\bar{X}$:
$$ s(\\hat{Y}_h) = \sqrt{MSE \\left( \\frac{1}{n} + \\frac{(X_h - \\bar{X})^2}{\\sum (X_i - \\bar{X})^2} \\right)} $$

Zauważ, że człon $(X_h - \\bar{X})^2$ sprawia, że przedział jest najwęższy gdy $X_h = \\bar{X}$ (w środku danych) i rozszerza się na brzegach (efekt "klepsydry" na wykresie).

---

## Podpunkt e) Przedział predykcyjny dla nowej obserwacji ($Y_{h(new)}$)

### Teoria
Tutaj chcemy przewidzieć czas obsługi dla **pojedynczego, konkretnego** przypadku (a nie średnią). Musimy uwzględnić nie tylko niepewność modelu (jak w punkcie d), ale też naturalną zmienność zjawiska (składnik losowy $\\epsilon$).

Błąd standardowy predykcji:
$$ s(pred) = \sqrt{MSE \\left( 1 + \\frac{1}{n} + \\frac{(X_h - \\bar{X})^2}{\\sum (X_i - \\bar{X})^2} \\right)} $$

Dodatkowa jedynka pod pierwiastkiem reprezentuje wariancję samej nowej obserwacji ($MSE \\approx \\sigma^2$). Dlatego przedziały predykcyjne są zawsze szersze od przedziałów ufności dla wartości oczekiwanej.

### Implementacja
W `statsmodels` różnica polega na ustawieniu flagi w `get_prediction(...)`:
- `obs=False` -> przedział ufności dla średniej (punkt d).
- `obs=True` -> przedział predykcyjny dla obserwacji (punkt e).

---

## Podpunkt f) Wizualizacja

Na wykresie (plik `plot_f.png`) naniesiono:
1. **Dane (niebieskie punkty)**.
2. **Linię regresji (czerwona linia)** - to nasze $\\hat{Y}$.
3. **Przedziały ufności dla średniej (zielone przerywane linie)** - węższe, "oplejają" linię regresji. Pokazują, gdzie z 95% pewnością leży prawdziwa linia regresji populacji.
4. **Przedziały predykcyjne (pomarańczowe kropkowane linie)** - szersze. Pokazują, gdzie z 95% pewnością spadnie *kolejny pomiar*. Muszą one objąć większość punktów danych.
