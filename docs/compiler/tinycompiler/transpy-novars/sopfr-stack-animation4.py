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
                div = div + 1      # ┌─ stack ──────────┐
                rec = sopfr_aux(n) # │val var  context  │
            return rec             # ├──────────────────┤
                                   # │ 42 n   sopfr     │
        div = 2                    # │  2 div sopfr     │
        return sopfr_aux(n)        # │ 42 n   sopfr_aux │
                                   # │  0 rec sopfr_aux │
    print(sopfr(42))               # └──────────────────┘

main()









