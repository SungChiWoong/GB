import json
import os
import cv2
import webbrowser
import numpy as np


#yolo형식의 label을 coco형식으로 변환
def yolo2coco(image_dir_path, label_dir_path,save_file_name , is_normalized):
    k=h=1
    total = {}

    # make info
    info = {
            'data_description' : '수인사거리',
            'data_created' : 'yyyy-MM'
            }
    total['info'] = info

    # make licenses
    licenses_list = []
    licenses_0= {
            'id' : '1',
            'name' : 'globalbridge'
            }
    licenses_list.append(licenses_0)

    ''' if you want to add licenses, copy this code
    licenses_1 = {
        'id': '2',
        'name': 'your_name',
        'url': 'your_name'
    }
    licenses_list.append(licenses_1)
    '''

    total['licenses'] = licenses_list

    # make categories
    category_list = []
    class_0 = {
            'id':  0,
            'name' : 'person'
            }
    class_1 = {
            'id':  1,
            'name' : 'car'
            }
    class_2 = {
            'id':  2,
            'name' : 'mortorbike'
            }
    class_3 = {
            'id':  3,
            'name' : 'bus'
            }
    class_4 = {
            'id':  4,
            'name' : 'truck'
            }
    category_list.append(class_0)
    category_list.append(class_1)
    category_list.append(class_2)
    category_list.append(class_3)
    category_list.append(class_4)

    '''
    # if you want to add class
    class_1 = {
            'id':  2,
            'name' : 'defect',
            'supercategory' : 'None'
            }
    category_list.append(class_1)
    '''
    total['categories'] = category_list

    # make yolo to coco format

    # get images
    image_list = os.listdir(image_dir_path)
    print('image length : ', len(image_list))
    label_list = os.listdir(label_dir_path)
    print('label length : ',len(label_list))

    image_dict_list = []
    count = 0
    for image_name in image_list :
        print("h",h)
        img = cv2.imread(image_dir_path+image_name)
        image_dict = {
                'id' : count,
                'file_name' : image_name,
                'width' : img.shape[1],
                'height' : img.shape[0],
                'license' : 1, # put correct license
                }
        image_dict_list.append(image_dict)
        count += 1
        h+=1
    total['images'] = image_dict_list

    # make yolo annotation to coco format
    label_dict_list = []
    image_count = 0
    label_count = 0
    for image_name in image_list :
        print(k)
        img = cv2.imread(image_dir_path+image_name)
        label = open(label_dir_path+image_name[0:-4] + '.txt','r')
        if not os.path.isfile(label_dir_path + image_name[0:-4] + '.txt'): # debug code
            print('there is no label match with ',image_dir_path + image_name)
            return
        while True:
            line = label.readline()
            if not line:
                break
            class_number, center_x,center_y,box_width,box_height = line.split()
            # should put bbox x,y,width,height
            # bbox x,y is top left

            if is_normalized :
                center_x =  int(float(center_x) * int(img.shape[1]))
                center_y = int(float(center_y) * int(img.shape[0]))
                box_width = int(float(box_width) * int(img.shape[1]))
                box_height = int(float(box_height) * int(img.shape[0]))
                top_left_x = center_x - int(box_width/2)
                top_left_y = center_y - int(box_height/2)

            if not is_normalized : #yolo2coco
                center_x = float(center_x)*img.shape[1]
                center_y = float(center_y)*img.shape[0]
                box_width = float(box_width)*img.shape[1]/2
                box_height = float(box_height)*img.shape[0]/2

                bbox_first=int(center_x-box_width)
                bbox_seceond=int(center_y-box_height)
                bbox_third=int(box_width*2)
                bbox_fourth=int(box_height*2)

            elif is_normalized=='kitti2coco':
                center_x = float(center_x)*img.shape[1]
                center_y = float(center_y)*img.shape[0]
                box_width = float(box_width)*img.shape[1]/2
                box_height = float(box_height)*img.shape[0]/2

                bbox_first=int(center_x-box_width)
                bbox_seceond=int(center_y-box_height)
                bbox_third=int(box_width*2)
                bbox_fourth=int(box_height*2)

            bbox_dict = []
            bbox_dict.append(bbox_first)
            bbox_dict.append(bbox_seceond)
            bbox_dict.append(bbox_third)
            bbox_dict.append(bbox_fourth)

            # segmetation dict : 8 points to fill, x1,y1,x2,y2,x3,y3,x4,y4
            segmentation_list_list = []
            segmentation_list= []
            segmentation_list.append(bbox_dict[0])
            segmentation_list.append(bbox_dict[1])
            segmentation_list.append(bbox_dict[0] + bbox_dict[2])
            segmentation_list.append(bbox_dict[1])
            segmentation_list.append(bbox_dict[0]+bbox_dict[2])
            segmentation_list.append(bbox_dict[1]+bbox_dict[3])
            segmentation_list.append(bbox_dict[0])
            segmentation_list.append(bbox_dict[1] + bbox_dict[3])
            segmentation_list_list.append(segmentation_list)

            label_dict = {
                    'id' : label_count,
                    'image_id' : image_count,
                    'bbox' : bbox_dict
                    }
            label_dict_list.append(label_dict)
            label_count += 1
        label.close()
        image_count += 1
        k+=1

    total['annotations'] = label_dict_list

    with open(save_file_name,'w',encoding='utf-8') as make_file :
        json.dump(total,make_file, ensure_ascii=False,indent='\t')



def kitti2coco(image_dir_path, label_dir_path,save_file_name , is_normalized):
    k=h=1
    total = {}

    # make info
    info = {
            "description": "",
            "url": "",
            "version": "",
            "year": 2017,
            "contributor": "",
            "data_created": "2020-04-14 01:45:18.567988"
            }
    total['info'] = info

    # make licenses
    licenses_list = []
    licenses_0= {
            "id": "1",
			"name": "your_name",
			"url": "your_name"
            }
    licenses_list.append(licenses_0)

    ''' if you want to add licenses, copy this code
    licenses_1 = {
        'id': '2',
        'name': 'your_name',
        'url': 'your_name'
    }
    licenses_list.append(licenses_1)
    '''

    total['licenses'] = licenses_list

    # make categories
    category_list = []
    class_0 = {
            'id':  1,
            'name' : 'bus',
            "supercategory": "None"
            }
    class_1 = {
            'id':  2,
            'name' : 'bus_45',
            "supercategory": "None"
            }
    class_2 = {
            'id':  3,
            'name' : 'car',
            "supercategory": "None"
            }
    class_3 = {
            'id':  4,
            'name' : 'mortorbike',
            "supercategory": "None"
            }
    class_4 = {
            'id':  5,
            'name' : 'person',
            "supercategory": "None"
            }
    class_5 = {
            'id':  6,
            'name' : 'truck',
            "supercategory": "None"
            }
    class_6 = {
            'id':  7,
            'name' : 'truck_45t',
            "supercategory": "None"
            }
    category_list.append(class_0)
    category_list.append(class_1)
    category_list.append(class_2)
    category_list.append(class_3)
    category_list.append(class_4)
    category_list.append(class_5)
    category_list.append(class_6)

    '''
    # if you want to add class
    class_1 = {
            'id':  2,
            'name' : 'defect',
            'supercategory' : 'None'
            }
    category_list.append(class_1)
    '''
    total['categories'] = category_list

    # make yolo to coco format

    # get images
    image_list = os.listdir(image_dir_path)
    print('image length : ', len(image_list))
    label_list = os.listdir(label_dir_path)
    print('label length : ',len(label_list))

    image_dict_list = []
    count = 0
    for image_name in image_list :
        print(h)
        img_array = np.fromfile(image_dir_path+image_name,np.uint8)
        img = cv2.imdecode(img_array,cv2.IMREAD_COLOR)
        image_dict = {
                'id' : count,
                'file_name' : image_name,
                'width' : img.shape[1],
                'height' : img.shape[0],
                "date_captured": "2020-04-14 -1:45:18.567975",
                'license' : 1, # put correct license
                "coco_url": "",
	        "flickr_url": ""
                }
        image_dict_list.append(image_dict)
        count += 1
        h+=1
    total['images'] = image_dict_list


    # make yolo annotation to coco format
    label_dict_list = []
    image_count = 0
    label_count = 0
    for image_name in image_list :
        print(k)
        img_array = np.fromfile(image_dir_path+image_name,np.uint8)
        img = cv2.imdecode(img_array,cv2.IMREAD_COLOR)
        label = open(label_dir_path+image_name[0:-4] + '.txt','r')
        if not os.path.isfile(label_dir_path + image_name[0:-4] + '.txt'): # debug code
            print('there is no label match with ',image_dir_path + image_name)
            return
        while True:
            line = label.readline()
            if not line:
                break
            class_number,_ ,_ ,_ ,top_left_x,top_left_y,bottom_right_x,bottom_right_y,_ ,_ ,_ ,_ ,_ ,_ ,_ = line.split()
            # should put bbox x,y,width,height
            # bbox x,y is top left

            # if is_normalized :
            #     center_x =  int(float(center_x) * int(img.shape[1]))
            #     center_y = int(float(center_y) * int(img.shape[0]))
            #     box_width = int(float(box_width) * int(img.shape[1]))
            #     box_height = int(float(box_height) * int(img.shape[0]))
            #     top_left_x = center_x - int(box_width/2)
            #     top_left_y = center_y - int(box_height/2)
            if not is_normalized : #kitti2coco
                # box_width = float(box_width)*img.shape[1]/2
                # box_height = float(box_height)*img.shape[0]/2

                bbox_first=float(top_left_x)
                bbox_seceond=float(top_left_y)
                bbox_third=float(bottom_right_x)-bbox_first
                bbox_fourth=float(bottom_right_y)-bbox_seceond

            bbox_dict = []
            bbox_dict.append(bbox_first)
            bbox_dict.append(bbox_seceond)
            bbox_dict.append(bbox_third)
            bbox_dict.append(bbox_fourth)


            # segmetation dict : 8 points to fill, x1,y1,x2,y2,x3,y3,x4,y4
            segmentation_list_list = []
            segmentation_list= []
            segmentation_list.append(bbox_dict[0])
            segmentation_list.append(bbox_dict[1])
            segmentation_list.append(bbox_dict[0] + bbox_dict[2])
            segmentation_list.append(bbox_dict[1])
            segmentation_list.append(bbox_dict[0]+bbox_dict[2])
            segmentation_list.append(bbox_dict[1]+bbox_dict[3])
            segmentation_list.append(bbox_dict[0])
            segmentation_list.append(bbox_dict[1] + bbox_dict[3])
            segmentation_list_list.append(segmentation_list)
            class_name={}
            class_name['bus']=0
            class_name['bus_45']=1
            class_name['car']=2
            class_name['motorbike']=3
            class_name['person']=4
            class_name['truck']=5
            class_name['truck_45t']=6
            label_dict = {
                    'id' : label_count,
                    'image_id' : image_count,
                    'category_id' : class_name[class_number]+1,
                    'iscrowd' : 0,
                    'bbox' : bbox_dict,
                    'area' : int(bbox_dict[2] * bbox_dict[3])
                    }
            label_dict_list.append(label_dict)
            label_count += 1
        label.close()
        image_count += 1
        k+=1

    total['annotations'] = label_dict_list

    with open(save_file_name,'w',encoding='utf-8') as make_file :
        json.dump(total,make_file, ensure_ascii=False,indent='\t')


if __name__ == '__main__':
    try:
        floder_path="C:/scr/darknet/car/val/"
        image_dir_path = floder_path+'image/'
        label_dir_path = floder_path+'label/'
        save_file_name = floder_path+'kind_val.json'
        is_normalized = False
        #is_normalize=['yolo2coco',yolo2kitti','kitti2yolo']
        # if you want to add more licenses or classes
        # add in code
        kitti2coco(image_dir_path, label_dir_path, save_file_name,is_normalized)
        url = 'https://192.168.1.5:5001/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%22pZgjECg3Lb2aNM6RQczluuejLS0DT77wSReluHbbtsKU4UDWeWnJIfmvKGNNCGGV%22&payload={"text":"완료되었습니다."}'
        webbrowser.open(url)
    except Exception as e:
        print(str(e))
        url = 'https://192.168.1.5:5001/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%22pZgjECg3Lb2aNM6RQczluuejLS0DT77wSReluHbbtsKU4UDWeWnJIfmvKGNNCGGV%22&payload={"text":"' + str(e) + '"}'
        webbrowser.open(url)