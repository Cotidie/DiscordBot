# TODO

- [x] token.0 등 중요한 정보 DB로 옮기기
- [x] bot.__get_token 등 static 함수 helper 모듈로 재정의
- [ ] scraper의 url 연결 실패 대처
- [x] slash command 적용 => [링크](https://discord-py-slash-command.readthedocs.io/en/latest/quickstart.html)
- [x] DB Collection의 필드명이 변경되면 코드 수정이 번거롭다. 통합할 방법을 찾아야 한다.
        => 관계 파일: db.py, format.py
- [ ] 오늘의미션 저장 개수가 1000개 이상이면 절반 삭제하도록 관리
- [ ] 오늘의미션 개별문서를 날짜별로 통합
- [ ] 매일 자정 오늘의미션 명령어 수행
- [ ] 접두사, 접미사 같은 문자열 통일하는 함수
- [ ] 패치노트 보여주기 명령어
- [ ] Formatter의 순환 import 문제. 구조 수정 필요
- [ ] ResourceManager 메소드 모두 static으로 제공
- [ ] Syncronize_raid_time => 동기화 전 비우기