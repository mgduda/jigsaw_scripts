CC = mpicc
CFLAGS = -O3 -g
CPPFLAGS = -I$(PNETCDF)/include
LDFLAGS = -L$(PNETCDF)/lib -lpnetcdf -lm

CHECKS = mpi_check pnetcdf_check
.PHONY: $(CHECKS)

all: mkgrid

mkgrid: mkgrid.c | $(CHECKS)
	$(CC) -o $(@) $(CFLAGS) $(CPPFLAGS) $(LDFLAGS) mkgrid.c 

clean:
	rm -f mkgrid


#-----------------------------------------------------------------------------#
#------- Targets for checking various aspects of the build environment -------#
#-----------------------------------------------------------------------------#


# Check that the mpicc wrapper can compile a simple program
mpi_check:
	@ printf "Checking that the mpicc compiler works... "
	@ tmpname=$$(mktemp mpitestXXXX.c); \
	exename=$$(mktemp mpitestXXXX); \
	printf "#include \"mpi.h\"\n\
		&int main(int argc, char **argv)\n\
		&{\n\
		&	MPI_Init(&argc, &argv);\n\
		&	return 0;\n\
		&}\n" | sed 's/^[[:blank:]]*&//' > $$tmpname; \
	$(CC) -o $$exename $(CFLAGS) $$tmpname > /dev/null 2>&1; \
	if [ $$? -ne 0 ]; then \
		printf "\n\nError: Could not compile an MPI test program using mpicc.\n"; \
		printf "Failed compilation command was:\n\n"; \
		printf "$(CC) -o $$exename $(CFLAGS) $$tmpname\n\n"; \
		printf "where $$tmpname contained the following program:\n\n"; \
		cat $$tmpname; \
		printf "\n"; \
		printf "Compilation produced the following error:\n\n"; \
		$(CC) -o $$exename $(CFLAGS) $$tmpname 2>&1; \
		printf "\n"; \
		rm $$tmpname; \
		exit 1; \
	else \
		rm $$tmpname $$exename; \
	fi
	@ printf "OK\n"

# Check whether the Parallel-netCDF library is available
pnetcdf_check: mpi_check
	@ printf "Checking for Parallel-netCDF library... "
	@ tmpname=$$(mktemp pnetcdftestXXXX.c); \
	exename=$$(mktemp pnetcdftestXXXX); \
	printf "#include \"mpi.h\"\n\
		&#include \"pnetcdf.h\"\n\
		&int main(int argc, char **argv)\n\
		&{\n\
		&	int ncid;\n\
		&	MPI_Init(&argc, &argv);\n\
		&	ncmpi_create(MPI_COMM_WORLD, \"testfile.nc\", NC_64BIT_OFFSET, MPI_INFO_NULL, &ncid);\n\
		&	return 0;\n\
		&}\n" | sed 's/^[[:blank:]]*&//' > $$tmpname; \
	$(CC) -o $$exename $(CFLAGS) $(CPPFLAGS) $(LDFLAGS) $$tmpname > /dev/null 2>&1; \
	if [ $$? -ne 0 ]; then \
		printf "\n\nError: Could not compile a PnetCDF test program using mpicc.\n"; \
		printf "Failed compilation command was:\n\n"; \
		printf "$(CC) -o $$exename $(CFLAGS) $$(CPPFLAGS) $(LDFLAGS) $$tmpname\n\n"; \
		printf "where $$tmpname contained the following program:\n\n"; \
		cat $$tmpname; \
		printf "\n"; \
		printf "Compilation produced the following error:\n\n"; \
		$(CC) -o $$exename $(CFLAGS) $(CPPFLAGS) $(LDFLAGS) $$tmpname 2>&1; \
		printf "\n"; \
		rm $$tmpname; \
		exit 1; \
	else \
		rm $$tmpname $$exename; \
	fi
	@ printf "OK\n"
