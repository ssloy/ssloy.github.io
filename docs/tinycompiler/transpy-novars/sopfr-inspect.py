import inspect

def main():
    def sopfr(n):
        def sopfr_aux(n):
            nonlocal div
            rec = 0
            if n % div == 0:
                # breakpoint, print stack
                var = {"main":[], "sopfr":["n","div"], "sopfr_aux":["n","rec"]}
                print([frame[0].f_locals[name] for frame in reversed(inspect.stack()[:-1]) for name in var[frame[3]]])
                rec = div
                if n != div:
                    rec = rec + sopfr_aux(n // div)
            else:
                div = div + 1
                rec = sopfr_aux(n)
            return rec

        div = 2
        return sopfr_aux(n)

    print(sopfr(42))

main()

