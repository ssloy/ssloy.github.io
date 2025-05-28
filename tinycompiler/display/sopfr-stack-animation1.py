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
                div = div + 1      # ┌─ stack 1 ────────┐
                rec = sopfr_aux(n) # │val var  context  │
            return rec             # ├──────────────────┤
                                   # │ 42 n   sopfr     │
        div = 2                    # │                  │
        return sopfr_aux(n)        # │                  │
                                   # │                  │
    print(sopfr(42))               # └──────────────────┘

main()









