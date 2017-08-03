IMAGE_NAME ?= kjagiello/thunderpush
TAG_FINAL ?= $(IMAGE_NAME):latest

.PHONY: docker-image
docker-image:
	docker build -t $(IMAGE_NAME) .

.PHONY: docker-push
docker-push:
	docker push $(TAG_FINAL)

.PHONY: travis-docker-login
travis-docker-login:
	@docker login -e="$(DOCKER_EMAIL)" -u="$(DOCKER_USER)" -p="$(DOCKER_PASS)"

.PHONY: travis-docker-push
travis-docker-push:
	docker tag $(IMAGE_NAME):latest $(IMAGE_NAME); \
	if [ -nz $$TRAVIS_TAG ]; then \
		docker tag $(IMAGE_NAME):$(TRAVIS_TAG) $(IMAGE_NAME);\
	fi
	docker tag \
		$(TAG_FINAL) \
		$(IMAGE_NAME):$(COMMIT)
	docker tag \
		$(TAG_FINAL) \
		$(IMAGE_NAME):travis-$(TRAVIS_BUILD_NUMBER)
	docker images
	docker push $(IMAGE_NAME)
