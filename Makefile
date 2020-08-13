dev-up:
	 docker-compose -f local.yml up --build
dev-bash:
	docker-compose -f local.yml exec django bash
dev-down:
	docker-compose -f local.yml down
dev-restart-django:
	docker-compose -f local.yml restart django
