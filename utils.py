class ProgBar:
    """
    Simple CLI progress bar.

    :param niter: int, number of operations to complete progress.
    :param barsmax: size of progress bar.
    :param percprec: decimal precision of progress percentage value
    """

    def __init__(self, niter: int, barsmax: int = 50, percprec: int = 3):
        self.niter: int = niter
        self.barsmax: int = 50
        self.percprec: int = 3
        self.progress = [f"0{'.' if percprec > 0 else ''}{'0' * percprec}% [", f">{barsmax * ' '}", f"] 0/{self.niter}"]
        self.progperc, self.lastprogperc = 0.0, 0.0
        self.lastbars = 0
        self.numbars = 0
        self.curiter = 0
        print(''.join(self.progress), end='\r')

    def update_incr(self):
        """Progress progress bar by one discrete chunk of the total."""
        self.curiter += 1
        if self.progperc != self.lastprogperc:
            self.progress[0] = f"{self.progperc:.3f}% ["
            self.progress[-1] = f"] {self.curiter}/{self.niter}"
            print(''.join(self.progress), end='\r')
        self.progperc = round((self.curiter / self.niter) * 100, self.percprec)
        self.numbars = round((self.curiter / self.niter) * self.barsmax)
        if self.numbars != self.lastbars:
            self.progress[1] = f"{self.numbars * '='}>{(self.barsmax - self.numbars) * ' '}"
            self.lastbars = self.numbars

    def update(self, curiter: int):
        """Update the progress bar's progress with the value at the passed iteration/integer indicating progress"""
        if self.progperc != self.lastprogperc:
            self.progress[0] = f"{self.progperc:.3f}% ["
            self.progress[-1] = f"] {curiter}/{self.niter}"
            print(''.join(self.progress), end='\r')
        self.progperc = round((curiter / self.niter) * 100, self.percprec)
        self.numbars = round((curiter / self.niter) * self.barsmax)
        if self.numbars != self.lastbars:
            self.progress[1] = f"{self.numbars * '='}>{(self.barsmax - self.numbars) * ' '}"
            self.lastbars = self.numbars