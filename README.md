
## Pilot_project_2nd


---
### Command line

* input : 영상이 담겨 있는 폴더
* output : 영상 Top5 분류 결과 및 비영상 정보 .csv 파일

---
### Web page

* input : 단일 영상 파일 또는 url
* output : 영상 Top5 분류 결과

---
### Transfer learning

* dataset : 대회용과 겹치지 않는 새로운 1000개의 ImageNet class
* -ing

---
### Requirements

* freezing graph : inception_resnet_v2 , inception_v3(for retrain)
* en and kr translated label from CLS ILSVRC ImageNet
* image file(web), directory(command line)

---
