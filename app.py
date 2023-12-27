from flask import Flask, render_template, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션을 위한 시크릿 키

# 가상의 전체 지점 데이터
locations = {
    'location1': {'name': '벚꽃이 만개하길', 'stamp': False},
    'location2': {'name': '토끼가 잘 자라길', 'stamp': False},
    'location3': {'name': '읍성이 빛나길', 'stamp': False}
}

@app.route('/')
def index():
    user_stamps = session.get('stamps', [])
    return render_template('mystamps.html', locations=locations, user_stamps=user_stamps)

@app.route('/stamp_external/<location_id>')
def stamp_external(location_id):
    # 외부에서 호출되었을 때 해당 지점에 대한 스탬프 찍기
    if location_id in locations:
        # 이미 해당 지점의 스탬프를 가지고 있는지 확인
        user_stamps = session.get('stamps', [])
        if location_id not in user_stamps:
            locations[location_id]['stamp'] = True

            # 세션에 스탬프 정보 저장
            session['stamps'] = user_stamps + [location_id]

            return 'Stamp added successfully!'

        return f'You already have the stamp for {locations[location_id]["name"]}'

    return 'Invalid location'

@app.route('/stamp/<location_id>')
def stamp_location(location_id):
    # 각 지점에 대한 스탬프 찍기
    if location_id in locations:
        user_stamps = session.get('stamps', [])

        # 이미 해당 지점의 스탬프를 가지고 있는지 확인
        if location_id not in user_stamps:
            # 해당 지점에 대한 스탬프 찍기
            locations[location_id]['stamp'] = True

            # 세션에 스탬프 정보 저장
            session['stamps'] = user_stamps + [location_id]

            # 스탬프를 찍은 지점에 대한 페이지 렌더링
            location_name = locations[location_id]['name']
            return render_template('stamp_location.html', location_name=location_name)

        return f'You already have the stamp for {locations[location_id]["name"]}'

    return 'Invalid location'

   
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
