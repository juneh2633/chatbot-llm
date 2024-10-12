import os

import requests

api_key = os.getenv("KAKAO_API_KEY")


def kakaomap(address):

    # 위치 정보를 사용하여 Kakao 지도 시각화
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey={api_key}&libraries=services"></script>
    </head>
    <body>
    <div id="map" style="width:100%;height:400px;"></div>
    <script>
        var mapContainer = document.getElementById('map'), // 지도를 표시할 div
            mapOption = {{
                center: new kakao.maps.LatLng(37.5665, 126.9780), // 기본 위치: 서울 시청
                level: 3 // 지도의 확대 레벨
            }};

        var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다.

        // 주소-좌표 변환 객체 생성
        var geocoder = new kakao.maps.services.Geocoder();

        // 주소로 좌표를 검색합니다.
        geocoder.addressSearch("{address}", function(result, status) {{
            // 정상적으로 검색이 완료됐으면
            if (status === kakao.maps.services.Status.OK) {{
                var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
                
                // 결과값으로 받은 위치를 지도에 마커로 표시합니다.
                var marker = new kakao.maps.Marker({{
                    map: map,
                    position: coords
                }});

                // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다.
                map.setCenter(coords);
            }}
        }});
    </script>
    </body>
    </html>
    """
    return html_code


def location_to_coordinate(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": address}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["meta"]["total_count"] > 0:
            first_result = data["documents"][0]["address"]
            latitude = first_result["y"]
            longitude = first_result["x"]
            return latitude, longitude
        else:
            return None, None
    else:

        return None, None
