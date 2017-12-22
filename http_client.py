import requests
import json
import datetime
import time
import geocoder
import glob
import base64

#url = "http://130.65.159.74/test"
data_to_send_dict = {}
images_list_file = []
camera_list = []
reg_station_id = ""

images = glob.glob("/home/ubuntu/Desktop/Usha/images/*jpeg")

print (images)
print ("Choose from the following options : ")
print ("1. Test")
print ("2. Register")
print ("3. Connect")
print ("4. Alert")
print ("5. Exit")

while True:
	select_option = input("Choose from the following options : ")

	headers = {'Content-type': 'application/json'}

	if select_option == 'Test':
		url = "http://130.65.159.74/test"
		data_to_send_dict = {"data":"test request"}
		r = requests.post(url, data=json.dumps(data_to_send_dict), headers=headers)
		print (r.content)
		
	if select_option == 'Register':
		url = "http://130.65.159.74/register"
		camera_list.append({"model":"Geo Vision GV-EDR4700-0F","type":"Action camera - 1440p","image_format":"JPEG","installation_position":"front-left"})
		date_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		desc = "This is a hotspot station, with "+str(len(camera_list))+" cameras "
		data_to_send_dict = {"station_type":"hotspot","cameras":camera_list,"registered_time": date_time,"description": desc}
		r = requests.post(url, data=json.dumps(data_to_send_dict), headers=headers)
		#print (r)
		#print (data_to_send_dict)
		temp_stat = json.loads(r.content)
		#print (temp_stat)
		reg_station_id = temp_stat["station_id"]
		#print (reg_station_id)
		print (r.content)
	
	if select_option == 'Connect':
		url = "http://130.65.159.74/connect"
		date_of_connection = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		location_hotspot = geocoder.google("Fremont,CA")
		#location_hotspot = geocoder.google("Milpitas,CA")
		#location_hotspot = geocoder.google("San Jose,CA")
		lat_lng = str((location_hotspot.latlng)[0]) + ", " + str((location_hotspot.latlng)[1])
		#print (lat_lng)
		#print (date_of_connection)
		#lng = (location_hotspot.latlng)[1]
		data_to_send_dict = {"station_id": reg_station_id,"connection_time" : date_of_connection ,"location": lat_lng}
		r = requests.post(url, data=json.dumps(data_to_send_dict), headers=headers)
		print (r.content)
	if select_option == "Alert":
		url = "http://130.65.159.74/alerting"
		if reg_station_id == "":
			reg_station_id = input("Enter station  ID :")
		date_of_connection = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		#location_hotspot = geocoder.google("Mountain View,CA")
		#location_hotspot = geocoder.google("Milpitas,CA")
		location_hotspot = geocoder.google("Fremont,CA")
		lat_lng = str((location_hotspot.latlng)[0]) + ", " + str((location_hotspot.latlng)[1])
		#print (lat_lng)
		#print (date_of_connection)
		#print (images)
		for file in images:
			#print ("In files")
		 	with open(file,"rb") as image_file:
				#print ("Inside open")
				encoded_string = "data:image/jpeg;base64," + base64.b64encode(image_file.read())
				images_list_file.append(encoded_string)
				encoded_string = ""
				#print (encoded_string)
		#print (len(images_list_file))
		#print (images_list_file)
		#lng = (location_hotspot.latlng)[1]
		data_to_send_dict = {"station_id": reg_station_id,"alerting_type":"IllegalDumpingAlert","alerting_time" : date_of_connection ,"location": lat_lng,"description":"This is an alert from a 			truck at San Jose","images":images_list_file}
		#print (data_to_send_dict)
		r = requests.post(url, data=json.dumps(data_to_send_dict), headers=headers)
		print (r.content)	

	if select_option == 'Exit':
		break 
		
