from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import Player, Match
from rest_framework.decorators import api_view, permission_classes
from .forms import PlayerForm, LoginForm, RaceForm, MatchResultForm
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import authentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate


def home_page(request):
    return render(request, 'home.html')


def register_page(request):
    form = PlayerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login_page')
    
    context = {
		'form': form
	}
    return render(request, 'register.html', context)


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            pwd = form.cleaned_data['pwd']

            # 嘗試從資料庫中找到該使用者
            try:
                player = Player.objects.get(account=account)

                # 檢查密碼是否正確
                if player.check_password(player.id, pwd):  # 使用Player model中的check_password方法
                    # 生成JWT
                    refresh = RefreshToken.for_user(player)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)
                    
                    # 检查是否是 'reff.acc' 账号
                    if account == 'reff.acc':
                        response = redirect('reff_page')  # 跳转到 Reff.html
                    else:
                        response = redirect('personal_page', player_id=player.id)  # 跳转到个人页面

                    # 设置 JWT 到 cookies
                    response.set_cookie('access_token', access_token, httponly=True)
                    response.set_cookie('refresh_token', refresh_token, httponly=True)

                    return response  # 返回响应
                else:
                    # 密码错误，返回错误信息
                    return JsonResponse({'error': '密碼錯誤'}, status=401)
            except Player.DoesNotExist:
                # 帳號不存在，返回错误信息
                return JsonResponse({'error': '帳號不存在'}, status=404)
    else:
        form = LoginForm()

    # GET请求时渲染登录表单页面
    return render(request, 'login.html', {'form': form})



# class LoginAPIView(APIView):
#     # permission_classes = [permissions.AllowAny] 
#     queryset = Player.objects.all()

#     def get(self, request):
#         # 处理GET请求，例如返回登录页面或者登录状态
#         # return Response({'message': '请使用POST请求来登录'}, status=status.HTTP_200_OK)
#         form = LoginForm()
#         return render(request, 'login.html', {'form': form})
#     def get_queryset(self):
#             # 返回所有 Player 对象的查询集
#             return Player.objects.all()

#     def post(self, request):
#             # 使用request.data 处理JSON数据
#             account = request.data.get('account')
#             pwd = request.data.get('pwd')
            
#             if not account or not pwd:
#                 return Response({'error': '无效的输入'}, status=status.HTTP_400_BAD_REQUEST)
            
#             try:
#                 # 尝试从数据库中找到该用户
#                 player = Player.objects.get(account=account)
                
#                 # 检查密码是否正确
#                 if player.check_password(player.id, pwd):
#                     # 生成 JWT
#                     refresh = RefreshToken.for_user(player)
#                     access_token = str(refresh.access_token)
#                     refresh_token = str(refresh)

#                     response_data = {
#                         'player_id': player.id,
#                         'access_token': access_token,
#                         'refresh_token': refresh_token
#                     }

#                     # 返回 JSON 响应
#                     return Response(response_data, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'error': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
            
#             except Player.DoesNotExist:
#                 return Response({'error': '帐号不存在'}, status=status.HTTP_404_NOT_FOUND)











# def personal_page_view(request, player_id):
#     # permission_classes = [IsAuthenticated] 
#     player = get_object_or_404(Player, id=player_id)
#     return render(request, 'personal_page.html', {'player': player})



@permission_classes([permissions.IsAuthenticated])
def personal_page_view(request, player_id):
    # 获取 cookies 中的 access_token
    access_token = request.COOKIES.get('access_token')

    if not access_token:
        return JsonResponse({'error': '未登录，无法访问该页面'}, status=401)

    # 使用 JWTAuthentication 验证 token
    jwt_authenticator = JWTAuthentication()
    try:
        validated_token = jwt_authenticator.get_validated_token(access_token)  # 验证 token
        # user = jwt_authenticator.get_user(validated_token)  # 从 token 中获取用户
    except (InvalidToken, TokenError):
        return JsonResponse({'error': '无效的token，请重新登录'}, status=401)

    # 如果 token 有效，继续处理请求并获取对应的 Player 信息
    player = get_object_or_404(Player, id=player_id)
    matches = Match.objects.filter(player1=player.account) | Match.objects.filter(player2=player.account)
    # 渲染个人页面
    return render(request, 'personal_page.html', {'player': player, 'matches': matches})



# def race_page_view(request):
#     if request.method == 'POST':
#         form = RaceForm(request.POST)
#         if form.is_valid():
#             # 获取表单中的数据
#             match_time = form.cleaned_data['match_time']
#             player1 = form.cleaned_data['player1']
#             player2 = form.cleaned_data['player2']

#             # 保存比赛数据到数据库
#             match = Match.objects.create(match_time=match_time, player1=player1, player2=player2)
            
#             # 比赛成功保存后，跳转或返回确认信息
#             return HttpResponse('比賽已成功預約！')
#     else:
#         form = RaceForm()

#     # GET 请求时渲染表单
#     return render(request, 'race.html', {'form': form})





def race_page_view(request, player_id):
    # 获取当前提交表单的用户
    current_player = get_object_or_404(Player, id=player_id)

    if request.method == 'POST':
        form = RaceForm(request.POST)
        if form.is_valid():
            # 获取表单数据
            match_time = form.cleaned_data['match_time']
            player1_account = form.cleaned_data['player1']
            player2_account = form.cleaned_data['player2']

            # 保存比赛数据到数据库
            match = Match.objects.create(match_time=match_time, player1=player1_account, player2=player2_account)

            # 提交表单后，重定向回个人页面
            return redirect('personal_page', player_id=current_player.id)

    else:
        form = RaceForm()

    return render(request, 'race.html', {'form': form, 'player': current_player})






def reff_page_view(request):
    matches = Match.objects.all()

    # 将比赛信息传递给模板
    return render(request, 'reff.html', {'matches': matches})


def register_result_view(request, match_id):
    # 获取比赛
    match = get_object_or_404(Match, id=match_id)

    if request.method == 'POST':
        form = MatchResultForm(request.POST)
        if form.is_valid():
            # 获取表单数据
            winner_account = form.cleaned_data['winner']

            # 使用 account 字段找到比赛的胜者
            if winner_account == match.player1:
                winner = Player.objects.get(account=match.player1)
            elif winner_account == match.player2:
                winner = Player.objects.get(account=match.player2)
            else:
                return render(request, 'register_result.html', {
                    'form': form,
                    'match': match,
                    'error': '获胜者必须是参赛者之一'
                })

            # 更新比赛的胜者
            match.winner = winner_account
            match.save()

            # 更新胜者的 winCount
            winner.winCount += 1
            winner.save()

            # 更新所有玩家的排名
            update_player_rankings()

            # 返回成功页面或者重定向到裁判页面
            return redirect('reff_page')

    else:
        form = MatchResultForm()

    return render(request, 'register_result.html', {'form': form, 'match': match})


def update_player_rankings():
    # 获取所有玩家并按 winCount 降序排列
    players = Player.objects.all().order_by('-winCount')

    # 更新每个玩家的排名
    for index, player in enumerate(players, start=1):
        player.ranking = index
        player.save()
