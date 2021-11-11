from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment
import random

User.objects.all().delete()
Category.objects.all().delete()

user_ujin = User.objects.create_user(username='ujin', email='ujin@yandex.ru', password='qwe123123')
user_max = User.objects.create_user(username='max', email='max@yandex.ru', password='qwe123123')

author_ujin = Author.objects.create(user=user_ujin)
author_max = Author.objects.create(user=user_max)

category_gaming = Category.objects.create(name="Игры")
category_music = Category.objects.create(name="Музыка")
category_cinema = Category.objects.create(name="Кино")
category_IT = Category.objects.create(name="IT")

text_article_cinema = """Что-то восхваляющее Дюну"""
text_article_gaming_music = """Очередной дабстеп"""
text_news_IT = """Ругаем Рокстар за убийство атмосферы наших любимых игр"""

article_ujin = Post.objects.create(author=author_ujin, post_type=Post.article,
                                   title="Дюна, годный фильм или же трейлер длительностью в 155 минут?",
                                   text=text_article_cinema)
article_max = Post.objects.create(author=author_max, post_type=Post.article, title="Подборка свежих треков для игр",
                                  text=text_article_gaming_music)
news_max = Post.objects.create(author=author_max, post_type=Post.news,
                               title="Состоялся релиз Grand Theft Auto: The Trilogy", text=text_news_IT)

PostCategory.objects.create(post=article_ujin, category=category_gaming)
PostCategory.objects.create(post=article_ujin, category=category_cinema)
PostCategory.objects.create(post=article_max, category=category_music)
PostCategory.objects.create(post=news_max, category=category_IT)

comment1 = Comment.objects.create(post=article_ujin, user=author_max.user, text="Вильнёв гений")
comment2 = Comment.objects.create(post=article_max, user=author_ujin.user, text="Опять дабстеп")
comment3 = Comment.objects.create(post=news_max, user=author_max.user, text="Я не буду за это платить")
comment4 = Comment.objects.create(post=news_max, user=author_ujin.user, text="Я тоже)")

list_for_like = [article_ujin,
                 article_max,
                 news_max,
                 comment1,
                 comment2,
                 comment3,
                 comment4]

for i in range(100):
    random_obj = random.choice(list_for_like)
    if random.randint(0, 1) % 2:
        random_obj.like()
    else:
        random_obj.dislike()

rating_johny = (sum([post.rating * 3 for post in Post.objects.filter(author=author_ujin)])
                + sum([comment.rating for comment in Comment.objects.filter(user=author_ujin.user)])
                + sum([comment.rating for comment in Comment.objects.filter(post__author=author_ujin)]))
author_ujin.update_rating(rating_johny)

rating_tommy = (sum([post.rating * 3 for post in Post.objects.filter(author=author_max)])
                + sum([comment.rating for comment in Comment.objects.filter(user=author_max.user)])
                + sum([comment.rating for comment in Comment.objects.filter(post__author=author_max)]))
author_max.update_rating(rating_tommy)

best_author = Author.objects.all().order_by('-rating')[0]

print("Лучший автор")
print("username:", best_author.user.username)
print("Рейтинг:", best_author.rating)
print("")

best_article = Post.objects.filter(post_type=Post.article).order_by('-rating')[0]
print("Лучшая статья")
print("Дата:", best_article.creation_date)
print("Автор:", best_article.author.user.username)
print("Рейтинг:", best_article.rating)
print("Заголовок:", best_article.title)
print("Превью:", best_article.preview())
print("")

print("Комментарии к ней")
for comment in Comment.objects.filter(post=best_article):
    print("Дата:", comment.creation_date)
    print("Автор:", comment.user.username)
    print("Рейтинг:", comment.rating)
    print("Комментарий:", comment.text)
    print("")
