redirect_uri = 'https://127.0.0.1:9000/kakaocallback'
rest_api_key = '[당신의 api 키값을 입력하세요]'

get_authorize_url = 'https://kauth.kakao.com/oauth/authorize?client_id='+ rest_api_key +'&redirect_uri='+ redirect_uri +'&response_type=code&scope=talk_message,friends'
authorize_code = '[get_authorize_url에 접속한후, 리디렉팅된 url의 "code=" 이후의 값을 입력하세요]'
