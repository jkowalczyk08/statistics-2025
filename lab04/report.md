# Raport z listy 4

Jakub Kowalczyk

## Zadanie 1

W tym zadaniu analizujemy zależność czasu obsługi (*y*) od liczby obsługiwanych maszyn (*x*). Dane pochodzą z pliku `ch01pr20.txt`.

### a) Wykres i Regresja Liniowa

Na podstawie wykresu punktowego (poniżej) można stwierdzić, że zależność między czasem obsługi a liczbą kopiarek jest w przybliżeniu liniowa. Punkty układają się wzdłuż prostej, co sugeruje zasadność zastosowania modelu regresji liniowej prostej:
$$ y = \beta_0 + \beta_1 x + \epsilon $$

![](zad1/plot_a.png)

Obliczone parametry regresji:
- **Teoretyczne:**
  - $\beta_0 = -0.580157$
  - $\beta_1 = 15.035248$
- **Biblioteczne (`statsmodels`):**
  - $\beta_0 = -0.580157$
  - $\beta_1 = 15.035248$

Równanie regresji:
$$ y = -0.58 + 15.04 x $$

### b) 95% Przedziały Ufności dla Slope'a i Intersepta

Poniższa tabela przedstawia punktowe estymatory oraz 95% przedziały ufności dla wyrazu wolnego ($\beta_0$) i współczynnika kierunkowego ($\beta_1$). Wyniki obliczone ręcznie są zgodne z wynikami z biblioteki.

| Parametr           | Metryka   | Teoretycznie           | Biblioteka             |
|:-------------------|:----------|:-----------------------|:-----------------------|
| Intercept (Beta 0) | Estymator | -0.580157              | -0.580157              |
| Slope (Beta 1)     | Estymator | 15.035248              | 15.035248              |
| Intercept (Beta 0) | 95% CI    | (-6.234843, 5.074529)  | [-6.234843, 5.074529]  |
| Slope (Beta 1)     | 95% CI    | (14.061010, 16.009486) | [14.061010, 16.009486] |

### c) Test Istotności Parametrów

Przeprowadzono testy istotności dla obu parametrów.
Hipotezy:
- $H_0: \beta_i = 0$
- $H_1: \beta_i \neq 0$

| Parametr           | Metryka      |   Teoretycznie |   Biblioteka |
|:-------------------|:-------------|---------------:|-------------:|
| Intercept (Beta 0) | Statystyka T |      -0.206908 | -0.206908    |
| Intercept (Beta 0) | p-wartość    |       0.837059 |  0.837059    |
| Slope (Beta 1)     | Statystyka T |      31.1233   | 31.1233      |
| Slope (Beta 1)     | p-wartość    |       0        |  4.00903e-31 |

**Wnioski:**
- **Slope ($\\beta_1$):** p-wartość $\approx 0 < 0.05$. Odrzucamy $H_0$. Istnieje istotna statystycznie zależność liniowa między liczbą kopiarek a czasem obsługi. Każda dodatkowa kopiarka zwiększa oczekiwany czas obsługi o około 15 godzin.
- **Intercept ($\\beta_0$):** p-wartość $\approx 0.84 > 0.05$. Nie ma podstaw do odrzucenia $H_0$. Wyraz wolny nie różni się istotnie od zera. W kontekście zadania oznacza to, że przy zerowej liczbie maszyn czas obsługi jest bliski zeru, co jest logiczne.

### d) Przedział Ufności dla Wartości Oczekiwanej

Estymujemy średni czas obsługi dla $k$ maszyn.

|   k |   Oczekiwana (Teor) |   CI Średnia Dolna (Teor) |   CI Średnia Górna (Teor) |   Długość CI |   Oczekiwana (Bibl) |   CI Średnia Dolna (Bibl) |   CI Średnia Górna (Bibl) |
|----:|--------------------:|--------------------------:|--------------------------:|-------------:|--------------------:|--------------------------:|--------------------------:|
|   1 |             14.4551 |                   9.63614 |                   19.274  |      9.6379  |             14.4551 |                   9.63614 |                   19.274  |
|   5 |             74.5961 |                  71.9142  |                   77.2779 |      5.36372 |             74.5961 |                  71.9142  |                   77.2779 |
|   8 |            119.702  |                 115.816   |                  123.588  |      7.77223 |            119.702  |                 115.816   |                  123.588  |
|  11 |            164.808  |                 158.475   |                  171.14   |     12.6643  |            164.808  |                 158.475   |                  171.14   |
|  25 |            375.301  |                 355.74    |                  394.862  |     39.1219  |            375.301  |                 355.74    |                  394.862  |
| 100 |           1502.94   |                1410.46    |                 1595.43   |    184.966   |           1502.94   |                1410.46    |                 1595.43   |

**Wniosek:** Długość przedziału ufności zależy od odległości $k$ od średniej liczby maszyn w próbie ($\\bar{x} \approx 5.11$). Im dalej punkt $k$ znajduje się od $\\bar{x}$, tym przedział jest szerszy (większa niepewność estymacji średniej). Najwęższy przedział obserwujemy dla $k=5$, które jest najbliżej średniej.

### e) Przedział Predykcyjny dla Nowej Obserwacji

Przewidujemy czas obsługi dla konkretnego przypadku serwisowania $k$ maszyn.

|   k |   Przewidywana (Teor) |   PI Dolna (Teor) |   PI Górna (Teor) |   Długość PI |   Przewidywana (Bibl) |   PI Dolna (Bibl) |   PI Górna (Bibl) |
|----:|----------------------:|------------------:|------------------:|-------------:|----------------------:|------------------:|------------------:|
|   1 |               14.4551 |          -4.15544 |           33.0656 |      37.2211 |               14.4551 |          -4.15544 |           33.0656 |
|   5 |               74.5961 |          56.4213  |           92.7708 |      36.3495 |               74.5961 |          56.4213  |           92.7708 |
|   8 |              119.702  |         101.311   |          138.093  |      36.7821 |              119.702  |         101.311   |          138.093  |
|  11 |              164.808  |         145.749   |          183.866  |      38.1169 |              164.808  |         145.749   |          183.866  |
|  25 |              375.301  |         348.735   |          401.867  |      53.1323 |              375.301  |         348.735   |          401.867  |
| 100 |             1502.94   |        1408.73    |         1597.16   |     188.428  |             1502.94   |        1408.73    |         1597.16   |

**Wniosek:** Podobnie jak w punkcie d), długość przedziału predykcyjnego rośnie wraz z oddalaniem się od średniej. Przedziały te są jednak znacznie szersze niż przedziały ufności dla wartości oczekiwanej.

### f) Wizualizacja Przedziałów

Na poniższym wykresie przedstawiono dane, linię regresji oraz 95% pasma ufności (zielone) i predykcji (pomarańczowe).

![](zad1/plot_f.png)

**Wyjaśnienie różnicy w szerokości przedziałów:**
Przedziały ufności (CI) dotyczą estymacji **średniej** wartości oczekiwanej ($E[Y|X]$), podczas gdy przedziały predykcyjne (PI) dotyczą **pojedynczej przyszłej obserwacji** ($Y_{new}$).
Wzór na błąd standardowy predykcji zawiera dodatkowy składnik wariancji błędu losowego ($\\sigma^2$), którego nie ma we wzorze na błąd estymacji średniej:
$$ s^2_{pred} = MSE \left( 1 + \frac{1}{n} + \frac{(X_h - \bar{X})^2}{\\sum(X_i - \bar{X})^2} \right) $$
Jedynka w nawiasie odpowiada za zmienność samej nowej obserwacji wokół średniej. Dlatego przedziały predykcyjne muszą uwzględniać zarówno niepewność co do położenia linii regresji (jak CI), jak i naturalny rozrzut danych wokół tej linii, przez co są zawsze szersze.
