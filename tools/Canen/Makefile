SRCDIR    = src
BUILDDIR  = build
TARGET    = mu-toksia

SRCEXT    = cpp
ALLSRCS   = $(wildcard $(SRCDIR)/*.$(SRCEXT))
SATSRCS   = $(wildcard $(SRCDIR)/*Solver.$(SRCEXT))
SOURCES   = $(filter-out $(SATSRCS),  $(ALLSRCS))
OBJECTS   = $(patsubst $(SRCDIR)/%,$(BUILDDIR)/%,$(SOURCES:.$(SRCEXT)=.o))

CXX       = g++
CFLAGS    = -Wall -Wno-parentheses -Wno-sign-compare -std=c++11
COPTIMIZE = -O3
LFLAGS    = -Wall
IFLAGS    = -I include

CFLAGS   += $(COPTIMIZE)
CFLAGS   += -D __STDC_LIMIT_MACROS -D __STDC_FORMAT_MACROS
CFLAGS   += -D CONE_OF_INFLUENCE
CFLAGS   += -D DCCO_VIA_DCAD
CFLAGS   += -D SECO_VIA_SEGR
CFLAGS   += -D DSCO_VIA_DCGR
CFLAGS   += -D GR_IN_ST
CFLAGS   += -D AD_IN_ST
#CFLAGS   += -D CO_IN_ST
CFLAGS   += -D ST_EXISTS_STG
#CFLAGS   += -D ST_EXISTS_SST

SAT_SOLVER = cryptominisat
CMSAT      = lib/cryptominisat-5.8.0

ifeq ($(SAT_SOLVER), cryptominisat)
	CFLAGS  += -D SAT_CMSAT
	IFLAGS  += -I $(CMSAT)/build/include
	LFLAGS  += -Wl,-rpath,'$$ORIGIN/lib/cryptominisat-5.8.0/build/lib' -L $(CMSAT)/build/lib -lcryptominisat5
	OBJECTS += $(BUILDDIR)/CryptoMiniSatSolver.o
	CMSAT_BUILD = $(CMSAT)/build
else
	$(error No SAT solver specified.)
endif

$(TARGET): $(OBJECTS)
	@echo "Linking..."
	@echo "$(CXX) $(OBJECTS) -o $(TARGET) $(LFLAGS)"; $(CXX) $(OBJECTS) -o $(TARGET) $(LFLAGS)

$(BUILDDIR)/%.o: $(SRCDIR)/%.$(SRCEXT)
	@echo "Compiling..."
	@mkdir -p $(BUILDDIR)
	@echo "$(CXX) $(CFLAGS) $(IFLAGS) -c -o $@ $<"; $(CXX) $(CFLAGS) $(IFLAGS) -c -o $@ $<

#.ONESHELL:
cmsat:
	@echo "Compiling CryptoMiniSat..."
	cd lib/cryptominisat-5.8.0 && \
	mkdir -p build && cd build && \
	cmake .. && \
	make

clean:
	@echo "Cleaning..."
	@echo "rm -rf $(BUILDDIR) $(TARGET)"; rm -rf $(BUILDDIR) $(TARGET) && if [ -d $(CMSAT) ]; then rm -rf $(CMSAT_BUILD); fi
