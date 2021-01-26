#!/usr/bin/env python
# coding: utf-8
import requests
import requests_debugger
requests_debugger.set(output_format=requests_debugger.CURL, max_depth=0)
import locale
locale.setlocale( locale.LC_ALL, '' )




#basic tool to hit the estimate API
#only returns the response code and the response data
def lyft_check(start_lat, start_lng, end_lat, end_lng):
    url = 'https://www.lyft.com/api/costs?'
    data = {"start_lat": start_lat, 
            "start_lng" : start_lng, 
            "end_lat" : end_lat, 
            "end_lng" : end_lng}
    req = requests.get(url, params=data, allow_redirects=True)
    resp_code = req.status_code
    resp = req.json()
    return [resp_code, resp]




#more robutst tool with error checking 
def lyft_tests(request_lists):    
    for item in request_lists:
        error_expected = item[4]
        resp = lyft_check(item[0], item[1], item[2], item[3])
        resp_code = resp[0]
        resp_data = resp[1]
        #bad lat/long
        if resp_code == 400 and error_expected == True:
            print('error found as expected')
        #happy path for an estimate
        elif resp_code == 200 and error_expected == False:
            price_1 = locale.currency((resp_data['cost_estimates'][0]['estimated_cost_cents_min']) / 100)
            price_2 = locale.currency((resp_data['cost_estimates'][1]['estimated_cost_cents_max']) / 100)
            print('price is estimated between: ', price_1, ' and ', price_2, ' dollars')
        #invalid request (or a potential error)
        elif resp_code == 200 and error_expected == True:
            invalid_request = resp_data['cost_estimates'][0]['is_valid_estimate']
            if invalid_request == False:
                print('invalid request found as expected')
        #catch-all error message 
        else:
            raise Exception('===== ERROR: something unexpected happened =====')
            
            

#test cases
valid_request_1 = (37.4507006,-122.1478051, 37.7960832, -122.4220388, False)
invalid_request_1 = (37.4507006,-122.1478051, 37.1079276,-113.5787893, True) 
invalid_request_2 = (99999,-113.5787893, 37.1044767, -113.5794689, True)
invalid_request_3 = (37.1079276,99999, 37.1044767, -113.5794689, True)
invalid_request_4 = (37.1079276,-113.5787893,99999, -113.5794689, True)
invalid_request_5 = (37.1079276,-113.5787893, 37.1044767,99999, True)
invalid_request_6 = ('12k1ksk;', '12;3mdmdD', 'qwlekm', '1', True)

#combine the test cases into a single list
request_lists = [valid_request_1, 
                 invalid_request_1, 
                 invalid_request_2, 
                 invalid_request_3, 
                 invalid_request_4, 
                 invalid_request_5, 
                 invalid_request_6]
        
    
lyft_tests(request_lists)  
    
print('done')
