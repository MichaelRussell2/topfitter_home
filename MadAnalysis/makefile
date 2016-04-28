F77   = gfortran
FFLAGS= -O -ffixed-line-length-132
PLOT    =  plot_events.o dbook.o rw_events.o kin_func.o set_cuts.o

.f.o: ; $(F77) $(FFLAGS) -c $*.f

plot_events: $(PLOT)
	$(F77) $(FFLAGS) -o plot_events $(PLOT)

clean:	
	rm -f *.o plot_events

kin_func.o: info.inc
plot_events.o: info.inc
set_cuts.o: info.inc
dbook.o: dbook.inc
