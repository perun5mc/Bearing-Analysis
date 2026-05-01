Jest to program, który ma tworzyć wykresy na podstawie danych z plików JSON.
Pliki te muszą zostać wybrane przez użytkownika.

Pozostałe dane zawarte są w folderze data.
bearings.json - pozwala zdefiniować bearingi (dropdown lista w oknie Options)
                lista ta jest aktualizowana także w trakcie działania programu, po ponownym otworzeniu okna Opcji
filepaths.json - lista ścieżek plików wskazanych przez użytkownika
state.json - przechowuje zapisany stan układu docków

W folderze files znajdują się przykładowe pliki z danymi
W folderze img znajdują się pliki obrazów, które wykorzystywane są w wyglądzie ui (ikonka i dropdown arrow)
W folderze scripts znajdują się skrypty, które wykorzystywane są przez main.py
W folderze ui znajdują się pliki ui z których utworzyłem plik main.py.

Uwagi, problemy i rzeczy do dodania:
 -  skrypt colors jest w zasadzie niepotrzebny. Moja metoda generowania kolorów jest niezależna od niego.
    Jest on używany w skryptach fft i spec w folderze Scripts
 -  lista bearingów w dropdown liście jest w istocie pobierana z pliku bearings.json, natomiast na wykresie labele są niezależne od tego
    przykładowo: jeśli zmienię nazwę pierwsze bearinga z B1 na B15, w liście pojawi się B15, a w labelu nadal będzie B1.
 -  kolory wykresów zmieniają się dynamicznie, to znaczy:
    przykładowo jak zaznaczę 500 rpm, wykres jest żółty. Potem, jak zaznaczę jakiś plik 1000 rpm, to 500 rpm zmienia kolor na inny.
    Jak dodam kolejny plik, to te wykresy przyjmują jeszcze inny kolor. Pasuje zrobić tak, aby kolejność była stała.
 -  Nie wiem co się dzieje, kiedy pierwsza harmoniczna jednego łożyska jest równa drugiej (lub jakiejkolwiek innej, innej niż pierwsza)
    Najprawdopodobniej któraś z tych harmonicznych się nie pokaże
 -  Heatmapa jest tworzona tylko i wyłącznie z ostatniego pliku, nie ze wszystkich zaznaczonych  


Pliki fft i spec z folderu scripts pochodzą z aplikacji webowej i nie mam pojęcia co się tam dzieje. Nieznacznie je zmodyfikowałem.
Dokumentacja tych skryptów powinna znajdować się w plikach aplikacji webowej (jest gdzieś na teamsie).