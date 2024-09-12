from django import forms
from .models import Player  

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'account', 'pwd']  # 指定要使用的字段
        labels = {
            'name': '選手名稱',
            'account': '帳號',
            'pwd': '密碼'
        }
        widgets = {
            'pwd': forms.PasswordInput(),  # 密码字段使用密码输入控件
        }

    
class LoginForm(forms.Form):
    account = forms.CharField(label='Account', max_length=20)
    pwd = forms.CharField(label='Password', widget=forms.PasswordInput())

class RaceForm(forms.Form):
    match_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), 
        label='比賽時間'
    )
    player1 = forms.CharField(max_length=100, label='參賽者 1')
    player2 = forms.CharField(max_length=100, label='參賽者 2')

class MatchResultForm(forms.Form):
    winner = forms.CharField(max_length=100, label="比賽勝者")