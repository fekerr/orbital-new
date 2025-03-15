# Makefile
#
# This Makefile defines common build targets for this project.
#
# Targets:
#   gitup   - Automatically stages all changes, commits with an incrementing commit number,
#             and updates the commit count. The commit number is stored in the file $(GITUP_COUNT_FILE)
#             (default is commit_count.txt). You can override this with an environment variable.
#
#   clean   - Removes generated build files (YAML outputs); source code is preserved.
#
# Environment Variables (defined in setenv.sh):
#   FEKERR_YAML_CHECK  - If set to 1 (default), YAML lint checks will run.
#   GITUP_COUNT_FILE   - File where the gitup commit count is stored (default: commit_count.txt).

.PHONY: gitup clean

# Use environment variable GITUP_COUNT_FILE if set, or default to commit_count.txt.
GITUP_COUNT_FILE ?= commit_count.txt

gitup:
	@# Ensure the commit count file exists. If not, initialize it to 1.
	@if [ ! -f $(GITUP_COUNT_FILE) ]; then echo "1" > $(GITUP_COUNT_FILE); fi
	@commit_num=`cat $(GITUP_COUNT_FILE)`; \
	echo "Current gitup commit number: $$commit_num"; \
	git add .; \
	git commit -m "gitup $$commit_num" || echo "Nothing to commit"; \
	new_commit_num=`expr $$commit_num + 1`; \
	echo $$new_commit_num > $(GITUP_COUNT_FILE); \
	echo "Updated commit count to $$new_commit_num"

clean:
	@echo "Cleaning built files..."
	@rm -f output_2d_chunks.yaml output_3d_chunks.yaml
	@echo "Clean complete."
