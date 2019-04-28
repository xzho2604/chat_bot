import requests

# lifx light bulb
LIGHT_CONTROL_URL = 'https://api.lifx.com/v1/lights'
token= 'cd237f1ec08865524355931f57b751628ab29c93d9fb6ad553d2691010fa0ff8'
BUILT_IN_COLOR = {'white', 'red', 'orange', 'yellow', 'cyan', 'green', 'blue', 'purple', 'pink'}


# get light control request headers
def get_light_request_header(token):
    headers = {
        "Authorization": "Bearer %s" % token
    }
    return headers


def light_control(power):
    headers = get_light_request_header(token)
    print("Myheader", headers)
    data = {}
    data['power'] = power

    response = requests.put(LIGHT_CONTROL_URL + '/all/state', data=data, headers=headers)
    res_status = response.status_code

    return res_status

#light_control("on")
