#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Counter-only teaching code. No buffer access is performed in the loops. */
static unsigned bad(uint8_t n) {
    volatile uint8_t i = 0;
    while (i <= n) {
        i = (uint8_t)(i + 1);
    }
    return i;
}

static unsigned repaired(uint8_t n) {
    volatile uint16_t i = 0;
    while (i <= n) {
        i = (uint16_t)(i + 1u);
    }
    return i;
}

int main(int argc, char **argv) {
    if (argc != 3) return 2;
    char *end = NULL;
    unsigned long value = strtoul(argv[2], &end, 10);
    if (!end || *end != '\0' || value > 255ul) return 2;
    uint8_t n = (uint8_t)value;
    if (strcmp(argv[1], "bad") == 0) {
        printf("%u\n", bad(n));
    } else if (strcmp(argv[1], "fixed") == 0) {
        printf("%u\n", repaired(n));
    } else {
        return 2;
    }
    return 0;
}
