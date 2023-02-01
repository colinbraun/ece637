# LABS := lab1 lab2 lab3
# 
# all:
# 	for i in $(LABS); do \
# 		cd $$i; \
# 		make; \
# 		cd ..; \
# 	done
# clean:
# 	for
# 
TOPTARGETS := all clean

# SUBDIRS := $(wildcard lab*/.)
SUBDIRS := lab1 lab3

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: $(TOPTARGETS) $(SUBDIRS)
