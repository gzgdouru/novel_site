from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.db.models import Q
import time

from .models import Novel, NovelCategory
from .utils import get_content, get_chapter_table
from .forms import SearchForm
from authors.models import Author
from operation.models import UserFavorite

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


class IndexView(View):
    '''
    首页
    '''
    def get(self, request):
        categorys = NovelCategory.objects.all()[:12]
        authors = Author.objects.all()[:8]
        novels = Novel.objects.filter(enable=True).order_by("-read_nums")[:8]

        return render(request, "index.html", context={
            "categorys" : categorys,
            "authors" : authors,
            "novels" : novels,
        })


class NovelListView(View):
    '''
    小说列表
    '''
    def get(self, request):
        all_novels = Novel.objects.filter(enable=True)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_novels, 5, request=request)
        novels = p.page(page)

        return render(request, "novel/novel-list.html", context={
            "novels": novels,
        })


class NovelDetaiView(View):
    '''小说详情页'''

    def get(self, request, novel_id):
        novel = get_object_or_404(Novel, pk=novel_id)
        relation_novels = Novel.objects.filter(category=novel.category, enable=True).exclude(id=novel.id).order_by("-read_nums")[:8]

        #获取最新章节
        chapterTable = get_chapter_table(novel_id)
        new_chapter = chapterTable.objects.filter(novel=novel).order_by("-chapter_index").first()

        has_fav = False
        if request.user.is_authenticated and UserFavorite.objects.filter(novel=novel, user=request.user).exists():
            has_fav = True

        return render(request, "novel/novel-detail.html", context={
            "novel" : novel,
            "relation_novels" : relation_novels,
            "new_chapter" : new_chapter,
            "has_fav": has_fav,
        })


class ChapterListView(View):
    '''
    章节列表
    '''
    def get(self, request, novel_id):
        novel = get_object_or_404(Novel, pk=novel_id)
        chapterTable = get_chapter_table(novel.id)
        new_chapters = chapterTable.objects.filter(novel=novel).order_by("-chapter_index")[:12]
        all_chapters = chapterTable.objects.filter(novel=novel).order_by("chapter_index")

        #阅读数+1
        novel.read_nums += 1
        novel.save()

        #排序
        sortby = request.GET.get("sort", "")
        if sortby:
            all_chapters = all_chapters.order_by("-chapter_index")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_chapters, 100, request=request)
        chapters = p.page(page)

        return render(request, "novel/chapter-list.html", context={
            "novel" : novel,
            "chapters" : chapters,
            "sortby" : sortby,
            "new_chapters" : new_chapters,
        })


class ChapterDetailView(View):
    '''
    章节详情
    '''
    def get(self, request, novel_id, chapter_id):
        novelObj = get_object_or_404(Novel, pk=novel_id)

        chapterTable = get_chapter_table(novelObj.id)
        chapterObj = get_object_or_404(chapterTable, pk=chapter_id)

        sortby = request.GET.get("sort", "")

        #取上一章节
        pre_chapter = chapterTable.objects.filter(novel_id=int(novel_id), chapter_index__lt=chapterObj.chapter_index).order_by("-chapter_index").first()
        if not pre_chapter: pre_chapter = chapterObj

        #取下一章节
        next_chapter = chapterTable.objects.filter(novel_id=int(novel_id), chapter_index__gt=chapterObj.chapter_index).order_by("chapter_index").first()
        if not next_chapter: next_chapter = chapterObj

        content = get_content(chapterObj.novel_id, chapterObj.chapter_index)
        if not content: content = "内容正在手打中, 请稍后..."

        return render(request, "novel/chapter-detail.html", context={
            "chapter" : chapterObj,
            "chapter_content" : content,
            "novel" : novelObj,
            "pre_chapter" : pre_chapter,
            "next_chapter" : next_chapter,
            "sortby" : sortby,
        })


class CategoryListView(View):
    '''
    分类列表
    '''
    def get(self, request):
        all_categorys = NovelCategory.objects.all()

        return render(request, "novel/category-list.html", context={
            "categorys" : all_categorys,
        })


class CategoryDetailView(View):
    '''
    分类详细
    '''
    def get(self, request, category_id):
        all_novels = Novel.objects.filter(category_id=category_id, enable=True)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_novels, 5, request=request)
        novels = p.page(page)

        return render(request, "novel/novel-list.html", context={
            "novels" : novels,
        })


class SearchView(View):
    '''
    小说搜索
    '''
    def post(self, request):
        keyword = request.POST.get("keyword", "")
        all_novels = Novel.objects.filter(Q(novel_name__icontains=keyword)|Q(author__name__icontains=keyword))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_novels, 5, request=request)
        novels = p.page(page)

        return render(request, "novel/novel-list.html", context={
            "novels" : novels,
        })
