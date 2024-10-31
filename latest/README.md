# autochoice-app

# Test Local

# start customer-service
cd latest/customer-service
sh ./start.sh

#  start api-gateway
cd latest/api-gateway
sh ./start.sh

cd latest/customer-service
python test.py

cd latest/api-gateway/test
python customer-service-test.py


#minikube k8s testing
#Create images
cd latest/customer-service
sh ./build.sh
cd latest/api-gateway
sh ./build.sh

#Setup minikube
#Deploy the services
minikube image load customer-svc:latest
minikube image load gateway-svc:latest
cd latest/deployment
kubectl apply -f deployment.yaml

minikube ip

curl http://<minikube ip>:<port-defined-in-the-deployement-file>/customers


# Local Deployemnt - Docker Desktop

#Build the docker images for all the microservices
#e.g. 
cd latest
# gateway-svc
sh api-gateway/build.sh
# auth-svc
sh auth-service/build.sh
# customer-svc
sh customer-service/build.sh
# vehicle-svc
sh vehicle-catalouge-service/build.sh
# booking-svc
sh booking-service/build.sh
# support-svc
sh support-service/build.sh
# rsa-svc
sh rsa-service/build.sh
# feedback-svc
sh feedback-service/build.sh

# Deploy the images to local K8S cluster
# Move to deployment dir
* cd deployemnt
# Start the deployments 
* kubectl apply -f .
# Delete the deployments
* kubectl delete -f .
# check the status of the deployments and services 
* kubectl get pods
* kubectl get services
* kubectl get deployments




