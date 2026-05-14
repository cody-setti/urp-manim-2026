# Make's purpose, as its name suggests, is to make a target file
# Here, in the 'Makefile', we tell it exactly what our target is and how to make it

# --- Target Artifacts ---
PROJECT   = cs-fapesp
BUILD_DIR = build
TARGET    = $(BUILD_DIR)/$(PROJECT).pdf


# --- File System Mapping ---
# Separate the files involved in the 'make' by their architectural purpose
CONFIGS   = cs-preamble.tex				# Environment setup, macros and styling
SRCS      = $(wildcard src/*.tex)			# The actual text/math payload (Note: Uses GNU Make wildcard)
ASSETS    = $(wildcard assets/*.bib assets/*.pdf)	# External assets queried during the build (Note: Uses GNU Make wildcard)

# Aggregate everything that should trigger a new build if modified
DEPS      = $(CONFIGS) $(SRCS) $(ASSETS)

# --- Toolchain Definition ---
# Map the compilation tools to standard systems-level variables
COMPILER  = lualatex
FLAGS     = -output-directory=$(BUILD_DIR) -interaction=nonstopmode -halt-on-error
LINKER    = biber


# --- Build Recipes ---

# The default rule executed when you just type `make`
# Here, we define it as a shorthand for make $(TARGET), the following rule
all: $(TARGET)

# The compilation seguence to make $(TARGET)
$(TARGET): $(PROJECT).tex $(DEPS)
# LaTeX requires multiple passes:
# 0. Make build directory
# 1. Generates aux. files and notes missing citations
# 2. Biber queries the .bib file to resolve those missing citations
# 3. Injects the formatted bibliography
# 4. Resolves all page numbers/references
	@mkdir -p $(BUILD_DIR)
	$(COMPILER) $(FLAGS) $(PROJECT).tex
	$(LINKER) $(BUILD_DIR)/$(PROJECT)
	$(COMPILER) $(FLAGS) $(PROJECT).tex  
	$(COMPILER) $(FLAGS) $(PROJECT).tex

# The `clean` rule deletes the build directory recursively
clean:
	rm -rf $(BUILD_DIR)

# Tell Make that 'all' and 'clean' are not actual files
.PHONY: all clean
