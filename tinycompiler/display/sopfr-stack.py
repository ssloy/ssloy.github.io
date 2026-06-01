def main():
    def sopfr(n):
        def sopfr_aux(n):
            nonlocal div
            rec = 0
            if n % div == 0:
                rec = div # breakpoint here
                if n != div:
                    rec = rec + sopfr_aux(n // div)
            else:
                div = div + 1
                rec = sopfr_aux(n)
            return rec

        div = 2
        return sopfr_aux(n)

    print(sopfr(42))

main() # current instruction

┌─ stack 1 ────────┐┌─ stack 2 ────────┐┌─ stack 3 ────────┐
│val var  context  ││val var  context  ││val var  context  │
├──────────────────┤├──────────────────┤├──────────────────┤
│ 42 n   sopfr     ││ 42 n   sopfr     ││ 42 n   sopfr     │
│  2 div sopfr     ││  3 div sopfr     ││  7 div sopfr     │
│ 42 n   sopfr_aux ││ 42 n   sopfr_aux ││ 42 n   sopfr_aux │
│  0 rec sopfr_aux ││  2 rec sopfr_aux ││  2 rec sopfr_aux │
└──────────────────┘│ 21 n   sopfr_aux ││ 21 n   sopfr_aux │
                    │  0 rec sopfr_aux ││  0 rec sopfr_aux │
                    │ 21 n   sopfr_aux ││ 21 n   sopfr_aux │
                    │  0 rec sopfr_aux ││  3 rec sopfr_aux │
                    └──────────────────┘│  7 n   sopfr_aux │
                                        │  0 rec sopfr_aux │
                                        │  7 n   sopfr_aux │
                                        │  0 rec sopfr_aux │
                                        │  7 n   sopfr_aux │
                                        │  0 rec sopfr_aux │
                                        │  7 n   sopfr_aux │
                                        │  0 rec sopfr_aux │
                                        │  7 n   sopfr_aux │
                                        │  0 rec sopfr_aux │
                                        └──────────────────┘


