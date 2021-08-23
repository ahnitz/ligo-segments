PYTHON ?= python3

check : \
	segments_verify \
	segments_utils_verify
	@echo "All Tests Passed"

define printpassfail
	{ echo "Pass" ; true ; } || { echo "Fail" ; false ; }
endef

segments_verify segments_utils_verify :
	@echo "=== start $@ ===>"
	$(PYTHON) $@.py && $(printpassfail)
	@echo "<=== end $@ ==="
