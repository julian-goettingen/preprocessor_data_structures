from PPDS.src.handle_file import handle_file

#
# es braucht eine kleine Bibliothek die dann reinkompiliert werden kann um das C-interface richtig zu testen
#
# dabei auch nachdenken über nötige features, was ist Teil von mvp?
# Einen Ordner importieren, der ein makefile enthält?
# Aus einem custom-command, was irgendwie einen Dateinamen zurückgibt, der auf ein .so verweist. -> am einfachsten.
# Einen String zu einem Modul erweitern (wäre cool)
#
# Wo kommt die config her? Aus code oder einem file wie bisher? -> erstmal file weil einfacher
#
# Ein generiertes (erstmal handgeschriebenes) Modul sollte einfach einen vielseitigen Konstruktor haben
# (Konstruktor oder static initializer für caching? Erstmal Konstruktor)
# Der Sinn vom Konstruktor ist aber eigentlich nur, die lib zu erzeugen, mit fest definiertem Namen, die dann in den
# generierten Funktionen benutzt werden kann. Das make_c_module enthält dann nur Hilfsmethoden, um diesen Konstruktor zu implementieren.
#
# Eine (mehrere) Funktion, die die verschiedenen input-arten (eg shell-command) nimmt und einen Dateinamen ausgibt, der dann das .so ist


def test_import():
    pass

