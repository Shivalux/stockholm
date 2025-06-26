NAME	= main.py
VERSION	= --version
HELP	= --help
SILENT	= --silent
REVERSE = --reverse
ARGS	= $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

$(NAME):
	@python3 $(NAME)
%:
	@:

silent:
	@python3 $(NAME) $(SILENT) $(ARGS)

activate:
	@python3 $(NAME) $(ARGS)

version:
	@python3  $(NAME) $(VERSION)

help:
	@python3 $(NAME) $(HELP)

reverse:
	@python3 $(NAME) $(REVERSE) $(ARGS)

qreverse:
	@python3 $(NAME) $(SILENT) $(REVERSE) $(ARGS)

.PHONY: reverse version activate silent qreverse help