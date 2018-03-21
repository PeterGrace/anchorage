test: 
	docker-compose rm --force && docker-compose up

fulltest:
	docker build -t anchoragetest . && docker-compose rm --force && docker-compose up
