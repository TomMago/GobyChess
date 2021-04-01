##
# GobyChess commands for development purposes
#
# @file
# @version 0.1

help:
	@echo " tests                  - Run unit tests."
	@echo " tests-cov     		   - Run unit tests."
	@echo " tests-make-cov         - Run unit tests and make coverage"
	@echo " benchmark              - Run benchmark tests."

test:
	python -m pytest --cov=gobychess tests

test-make-cov:
	python -m pytest --cov=gobychess tests
	python -m codecov

benchmark:
	python -m py.test --benchmark-columns=min,max,mean,stddev --benchmark-sort=mean benchmarks


# end
