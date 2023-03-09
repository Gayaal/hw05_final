from django import forms

from posts.models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Текст поста',
            'group': 'Группа поста',
        }
        help_texts = {
            'text': 'Введите сюда содержимое поста',
            'group': 'Выберите группу, если хотите',
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = ()
        self.fields['group'].empty_label = 'Выберите группу, если желаете 🙂'

    def clean_text(self) -> str:
        post_text = self.cleaned_data['text']
        forbidden_words = ('блин', 'фига', 'гугл')
        for word in forbidden_words:
            if word in post_text.lower():
                raise forms.ValidationError(f'Слово {word} запрещено')
        return post_text


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Текст комментария'}
        help_texts = {'text': 'Введите сюда комментарий'}

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs[
            'placeholder'
        ] = 'Введите сюда комментарий'
