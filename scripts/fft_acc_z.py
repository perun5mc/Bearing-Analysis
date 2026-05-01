import json
import numpy as np

from scipy.fft import fft, fftfreq

import scripts.colors as colors
import scripts.classes as bearingClass

# ------- Pobieranie danych o łożyskach wałach i przekładniach -------

# definiujemy położenie pliku z łożyskami
bearing_file_path = "data/bearings.json"

bearing_file = open(bearing_file_path)
bearings_file_data = json.load(bearing_file)
bearing_data = bearings_file_data["bearings"]  # przypisujemy wartości łożysk
gear_box_data = bearings_file_data["gear_boxes"]  # przypisujemy wartości przekładni

bearingss = []  # lista łożysk
bearings_initials = []  # lista inicjałów łożysk
gear_boxess = []  # lista przekładni
gear_boxes_initials = []  # lista inicjałów przekładni


# ------- Przypisujemy wartości do list -------

for bearing in bearing_data:
    bearingss.append(bearing_data[bearing])

for i in range(0, len(bearingss)):
    bearings_initials.append(f"B{i+1}")

for gear_box in gear_box_data:
    gear_boxess.append(gear_box_data[gear_box])

for i in range(0, len(gear_boxess)):
    gear_boxes_initials.append(f"G{i+1}")


bearing_option_list = []
for label in range(0, len(bearing_data)):
    bearing_option_list.append(
        {"label": f"Quantis148_{bearings_initials[label]}_geom", "value": label}
    )

def generate_fft_plot(speed, harmonics, bearingsDropdown, elementsDropdown, file_path):
    print(f"Bearings: {bearingsDropdown}")
    print(f"Elements: {elementsDropdown}")

    f = open(file_path)
    data = json.load(f)

    sample_rate = data["sample_rate"]
    N = data["number_of_samples"]  # pobieramy ilość próbek z pliku
    T = 1.0 / sample_rate

    #  -------------- MOZLIWOSC ZMIANY CZYTANEJ OSI --------------
    y1 = data["vibrationsZ"]
    y1 = y1 - np.mean(y1)

    xf = fftfreq(N, T)[: N // 2]
    yf1 = abs(fft(y1)) / N

    main_x_list = xf.tolist()
    main_y_list = yf1.tolist()
    main_plot = [main_x_list, main_y_list]
    # Generowanie głównego wykresu


    if harmonics is None or harmonics == "":
        harmonics = 0
    traces = []
    for i in range(0, len(bearingsDropdown)):
        for n in range(0, len(elementsDropdown)):
            match elementsDropdown[n]:
                case "inner":
                    for s in range(0, harmonics):
                        my_bearing = bearingClass.Bearing(
                            bearingss[bearingsDropdown[i]], speed
                        )
                        traces.append(
                            [
                                [
                                    my_bearing.inner() * (s + 1),
                                    my_bearing.inner() * (s + 1),
                                ],
                                [0, max(yf1)],
                                colors.inner_colors[0],
                                f"Inner {bearings_initials[bearingsDropdown[i]]}",
                            ]
                        )

                case "outer":
                    for s in range(0, harmonics):
                        my_bearing = bearingClass.Bearing(
                            bearingss[bearingsDropdown[i]], speed
                        )
                        traces.append(
                            [
                                [
                                    my_bearing.outer() * (s + 1),
                                    my_bearing.outer() * (s + 1),
                                ],
                                [0, max(yf1)],
                                colors.outer_colors[0],
                                f"Outer {bearings_initials[bearingsDropdown[i]]}",
                            ]
                        )

                case "cage":
                    for s in range(0, harmonics):
                        my_bearing = bearingClass.Bearing(
                            bearingss[bearingsDropdown[i]], speed
                        )
                        traces.append(
                            [
                                [
                                    my_bearing.cage() * (s + 1),
                                    my_bearing.cage() * (s + 1),
                                ],
                                [0, max(yf1)],
                                colors.cage_colors[0],
                                f"Cage {bearings_initials[bearingsDropdown[i]]}",
                            ]
                        )

                case "roll":
                    for s in range(0, harmonics):
                        my_bearing = bearingClass.Bearing(
                            bearingss[bearingsDropdown[i]], speed
                        )
                        traces.append(
                            [
                                [
                                    my_bearing.roller() * (s + 1),
                                    my_bearing.roller() * (s + 1),
                                ],
                                [0, max(yf1)],
                                colors.roll_colors[0],
                                f"Roller {bearings_initials[bearingsDropdown[i]]}",
                            ]
                        )
                case "shaft":
                    for s in range(0, harmonics):
                        my_bearing = bearingClass.Bearing(
                            bearingss[bearingsDropdown[i]], speed
                        )
                        traces.append(
                            [
                                [
                                    my_bearing.shaft() * (s + 1),
                                    my_bearing.shaft() * (s + 1),
                                ],
                                [0, max(yf1)],
                                colors.shaft_colors[0],
                                f"Shaft {bearings_initials[bearingsDropdown[i]]}",
                            ]
                        )
                case _:
                    # Should never happen
                    print("nothing")

    plot_data = [main_plot, traces]
    return plot_data
