NAME := main.py

all:
	python $(NAME)

play:
	python $(NAME) --play

run:
	python $(NAME) --run

replay:
	python $(NAME) --replay

clean:
	rm -rf data
