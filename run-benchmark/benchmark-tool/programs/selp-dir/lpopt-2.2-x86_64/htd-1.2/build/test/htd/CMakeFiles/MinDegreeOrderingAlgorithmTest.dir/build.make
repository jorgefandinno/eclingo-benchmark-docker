# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /gpfs1/sw/x86_64/rh7/pkgs/cmake/3.28.3/bin/cmake

# The command to remove a file.
RM = /gpfs1/sw/x86_64/rh7/pkgs/cmake/3.28.3/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build

# Include any dependencies generated for this target.
include test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/compiler_depend.make

# Include the progress variables for this target.
include test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/progress.make

# Include the compile flags for this target's objects.
include test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/flags.make

test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.o: test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/flags.make
test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.o: /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/test/htd/MinDegreeOrderingAlgorithmTest.cpp
test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.o: test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.o"
	cd /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build/test/htd && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.o -MF CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.o.d -o CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.o -c /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/test/htd/MinDegreeOrderingAlgorithmTest.cpp

test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.i"
	cd /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build/test/htd && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/test/htd/MinDegreeOrderingAlgorithmTest.cpp > CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.i

test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.s"
	cd /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build/test/htd && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/test/htd/MinDegreeOrderingAlgorithmTest.cpp -o CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.s

# Object files for target MinDegreeOrderingAlgorithmTest
MinDegreeOrderingAlgorithmTest_OBJECTS = \
"CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.o"

# External object files for target MinDegreeOrderingAlgorithmTest
MinDegreeOrderingAlgorithmTest_EXTERNAL_OBJECTS =

test/htd/MinDegreeOrderingAlgorithmTest: test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/MinDegreeOrderingAlgorithmTest.cpp.o
test/htd/MinDegreeOrderingAlgorithmTest: test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/build.make
test/htd/MinDegreeOrderingAlgorithmTest: lib/libhtd.so.0.0.0
test/htd/MinDegreeOrderingAlgorithmTest: test/googletest/googletest-release-1.8.0/googlemock/gtest/libgtest_main.so
test/htd/MinDegreeOrderingAlgorithmTest: test/googletest/googletest-release-1.8.0/googlemock/gtest/libgtest.so
test/htd/MinDegreeOrderingAlgorithmTest: test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable MinDegreeOrderingAlgorithmTest"
	cd /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build/test/htd && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/build: test/htd/MinDegreeOrderingAlgorithmTest
.PHONY : test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/build

test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/clean:
	cd /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build/test/htd && $(CMAKE_COMMAND) -P CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/cmake_clean.cmake
.PHONY : test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/clean

test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/depend:
	cd /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2 /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/test/htd /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build/test/htd /gpfs1/home/e/l/elillopo/eclingo-benchmark/selp/lpopt-2.2-x86_64/htd-1.2/build/test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : test/htd/CMakeFiles/MinDegreeOrderingAlgorithmTest.dir/depend

