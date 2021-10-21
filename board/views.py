import json

from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Board
from member.models import Member
from utils.decorators import auth_check, user_check

class BoardView(View):
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

    @user_check
    def put(self, request):
        data = json.loads(request.body)
        member_id = request.member.id
        postings = Board.objects.get(author=member_id)
        postings.title = data.get('title')
        postings.content = data.get('content')
        postings.save()
        return JsonResponse({'message' : 'SUCCESS'}, status=201)
    @user_check
    def delete(self, request):
        member_id = request.member.id
        postings = Board.objects.filter(author=member_id)
        postings.delete()
        return JsonResponse({'message': 'SUCCESS'}, status=201)