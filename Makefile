NAME	= stockholm
KEY 	= 

$(NAME):
	python3 main.py

run: $(NAME)

version:
	python3  main.py --version

reverse:
	python3 main.py --reverse $(KEY)

key:
	@echo $(KEY)

PHONEY: reverse version key run