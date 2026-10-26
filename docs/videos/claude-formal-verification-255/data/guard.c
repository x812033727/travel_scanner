#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

_Static_assert(CHAR_BIT == 8, "This example uses 8-bit bytes");
_Static_assert(UINT8_MAX == 255, "This example uses uint8_t values 0..255");

enum { CAPACITY = 8 };

/* n is the payload length in bytes; one extra byte is needed for a terminator. */
static bool guard_bad(uint8_t n) {
    uint8_t total = (uint8_t)(n + 1);
    return total <= CAPACITY;
}

/* Preserve the complete value before comparing it with the capacity. */
static bool guard_widened(uint8_t n) {
    uint16_t total = (uint16_t)((uint16_t)n + 1u);
    return total <= CAPACITY;
}

/* Equivalent bound, derived from the mathematical specification. */
static bool guard_bound(uint8_t n) {
    return n < CAPACITY;
}

int main(void) {
    puts("n,bad,widened,bound,mathematical_fits,promoted_total,narrowed_total");
    for (unsigned n = 0; n <= UINT8_MAX; ++n) {
        unsigned fits = (n + 1u) <= (unsigned)CAPACITY;
        int promoted_total = (uint8_t)n + 1;
        uint8_t narrowed_total = (uint8_t)promoted_total;
        printf("%u,%u,%u,%u,%u,%d,%u\n", n,
               (unsigned)guard_bad((uint8_t)n),
               (unsigned)guard_widened((uint8_t)n),
               (unsigned)guard_bound((uint8_t)n), fits,
               promoted_total, (unsigned)narrowed_total);
    }
    return 0;
}
