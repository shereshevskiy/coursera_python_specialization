import requests
import time
from collections import Counter


def calc_age(uid, token="c3656bf6c3656bf6c3656bf6f5c30fe069cc365c3656bf69fbc16ec0a33e2cc73b2c44c"):
    current_year = time.localtime().tm_year

    user_id = uid
    url_for_id = f'https://api.vk.com/method/users.get?v=5.71&access_token={token}&user_ids={user_id}'
    r = requests.get(url_for_id)
    id_ = str(r.json()['response'][0]['id'])
    url_for_friends = f'https://api.vk.com/method/friends.get?v=5.71&access_token={token}&user_id={id_}&fields=bdate'
    friends_request = requests.get(url_for_friends)
    friends_request_json = friends_request.json()
    friends_response = friends_request_json["response"]
    friends_items = friends_response["items"]

    id_yearofbirth = {item["id"]: int(item["bdate"].split(".")[2])
                      for item in friends_items if ("bdate" in item) and (len(item["bdate"].split(".")) == 3)}

    id_age = {item: current_year - id_yearofbirth[item] for item in id_yearofbirth}
    ages_list = list(id_age.values())

    counter = Counter(ages_list)
    counted = counter.most_common()
    sorted_counted = sorted(counted, key=lambda x: (x[1], -x[0]), reverse=True)

    return sorted_counted


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
