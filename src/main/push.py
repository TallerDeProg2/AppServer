from pyfcm import FCMNotification

api_key = 'AAAAaxCakgY:APA91bG4JlqQn6YhGAoPck1_moeHW4PxUWiPxnjEmxqfbVLTCVk7Wfn6fOq7AR7b_zPBF0oR9ln-d1maLH5ZoqbFea0eEl0O10RHUYyljyztqkwJEq46kZwVgKgt377PwVH00pjR87i4'

push_service = FCMNotification(api_key="<api-key>")

# OR initialize with proxies

proxy_dict = {
    "http": "http://127.0.0.1",
    "https": "http://127.0.0.1",
}
push_service = FCMNotification(api_key="<api-key>", proxy_dict=proxy_dict)

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

registration_id = "<device registration_id>"
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                           message_body=message_body)

print
result

# Send to multiple devices by passing a list of ids.
registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
message_title = "Uber update"
message_body = "Hope you're having fun this weekend, don't forget to check today's news"
result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,
                                              message_body=message_body)

print
result