#include <stdio.h>

int sopfr_aux(int n, int *div) {
    int recursion = 0;
    if (n % *div == 0) {
        recursion = *div;
        if (n!=*div) {
            recursion = recursion + sopfr_aux(n / *div, div);
        }
    } else {
        *div = *div + 1;
        recursion = sopfr_aux(n, div);
    }
    return recursion;
}

int sopfr(int n) {
    int div = 2;
    return sopfr_aux(n, &div);
}

void main() {
    printf("%d\n", sopfr(42));
}
