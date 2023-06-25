
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "module.h"

#include "PPDS_SOURCE_ARR1D.h"

#include "PPDS_DEF_1.h"
int main() {

    const int n = 1000;
    int *x = (int*)malloc(n*sizeof(int));
    if (x==NULL) exit(1);
    PPDS_DECLARE_ARR1D(X, x, n)

    for (int i=0; i<n; i++) {
        X(i) = i;
    }

//    definiere Funktionen in module.c und rufe sie von hier aus auf
//    füge dabei nach und nach die checker hinzu


//    erste Mission: scoping der Funktionen.
//
//PERFEKT WÄRE JA: Die Datenstruktur kann in einem .c-Implementationsfile genauso gescoped werden wie bisher, aber der nötige compatibility-check wird irgendwie rausgetragen. Ans header-file. Das klingt gut.
//
//Also: DEF und UNDEF bleiben, aber es gibt ein zusätzliches target-file, was dann im header inkludiert werden muss/sollte (linter?)
//Das ist auch ein sinnvolles target für die Funktionsdefinition selber.
//
//und wie soll die Funktionsdeklaration im header überhaupt aussehen?
//Mglk 1: genauso wie in der Implementation --> wäre konsistent, aber es wäre auch schlecht, weil dann würde wieder die Definition von den Datenstrukturen rausleaken würde
//Mglk 2: Ein Makro aus dem DEFS_FOR_HEADER, was einfach zu einer Deklaration expanded -> ja das würde doch gehen, oder? Ausprobieren, wie die code-navigation dann aussieht.
//Mglk 3: das defs_for_header deklariert die Funktionen auch direkt -> ja, das wäre einfacher, kann man trotzdem noch module-private-funktionen machen? später - da reicht ja ein keyword für.
//
//MGLK 3 soll es sein
//
//
//
//Name: file.<ending> -> file_PPDS_DEFS_FOR_HEADER.h
//
//damit es auch mit templates vernünftig geht sollte noch ein DEF_LEAK_NAMES dazukommen. -> eigentlich ein unabhängiges Ding.
//
//dabei todo: Könnten die ganzen source-header-felder optional werden, oder in eigene files gesteckt werden?
//
//
//Schritte:
//    SOURCE_FUNCTION_NEW hat die Definitionen schon unter der neuen Rubrik
//    Das muss verarbeitet werden um den neuen header zu erzeugen.
//
//
//
//    free(x); x=NULL;
}
#include "PPDS_UNDEF_1.h"

