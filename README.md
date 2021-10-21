# boardproject
프리온보딩 벡엔드 코스 과제


## 1. 구현한 방법과 이유에 대한 간략한 내용
- python & django framework 활용한 CRUD 게시판 작업 : django는 완성된 다양한 작업을 제공해주므로 선택하여 사용.
- 한 endpoint, view를 이용하여 POST, GET, PUT, DELETE(게시글에 필요한 내용) 구현

## 2. 자세한 실행 방법(endpoint 호출방법)
- modeling 시 member, board로 나눠 모델 제작. -> member는 회원가입 jwt, bcrypt를 활용한 인증 인가 작업 시행, member의 id를 FK로 하여 board에 author 설정
- view 작업 중 POST, GET, PUT, DELETE 메서드 활용. json 통해 불러오기 통해 값 설정 및 출력
- decorator.py를 활용하여 user 및 auth check 통해 유저 토큰 활용. 게시글 CRUD 시 유저 인증 인가 지속.

## 3. api 명세(request/response 서술 필요)
```
class BoardView(View):

# CREATE
    @user_check
    def post(self, request):
        data = json.loads(request.body)
        title = data['title']
        content = data['content']
        author = request.member
        board_post = Board.objects.create(
            title=title,
            content=content,
            author=author
        )
        return JsonResponse({'message' : 'SUCCESS'}, status=201)


# READ+Pagination
    @user_check
    def get(self, request):
        postings = Board.objects.all()
        page = int(request.GET.get('p', 1))
        paginator = Paginator(postings, 5)
        boards = paginator.get_page(page)
        result = []

        for posting in boards:
            my_dict = {
                'title' : posting.title,
                'content' : posting.content,
                'author' : posting.author.name
            }
            result.append(my_dict)
        return JsonResponse({'result' : result}, status=201)

# UPDATE
    @user_check
    def put(self, request):
        data = json.loads(request.body)
        member_id = request.member.id
        postings = Board.objects.get(author=member_id)
        postings.title = data.get('title')
        postings.content = data.get('content')
        postings.save()
        return JsonResponse({'message' : 'SUCCESS'}, status=201)

# DELETE
    @user_check
    def delete(self, request):
        member_id = request.member.id
        postings = Board.objects.filter(author=member_id)
        postings.delete()
        return JsonResponse({'message': 'SUCCESS'}, status=201)
```
