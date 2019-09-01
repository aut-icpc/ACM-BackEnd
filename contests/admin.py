from django.contrib import admin
from django.utils.html import format_html
from .models import ACM ,Image


class ACMContestAdmin(admin.ModelAdmin):
    # list_display_link = ('title', )
    list_display = ('title','show_problem',
    'show_final_ranking_onsite' ,'show_final_ranking_online','show_images' )
    # list_filter = ('title',)
    search_fields = [ 'title']
    
    def show_images(self, obj):
        return "".join(str([i.src for i in obj.images.all()]))
    show_images.short_description = "images"
    def show_problem(self, obj):
        return format_html("<a href='{url}'>{text}</a>", url=obj.problems , text="problems")
    show_problem.short_description = "problems"
    
    def show_final_ranking_onsite(self, obj):
        return format_html("<a href='{url}'>{text}</a>", url="//www.google.com", text="ranking onsite")
    show_final_ranking_onsite.short_description = " final ranking onsite"
   
    def show_final_ranking_online(self, obj):
        return format_html("<a href='{url}'>{text}</a>", url="//www.google.com", text="ranking online")
    show_final_ranking_online.short_description = " final ranking online"

    # def show_test_data(self, obj):
    #     return format_html("<a href='{url}'>{text}</a>", url="//www.google.com", text="test_data")
    # show_test_data.short_description = "test_data"

    # def show_judge_solution(self, obj):
    #     return format_html("<a href='{url}'>{text}</a>", url="//www.google.com", text="judje_solution")
    # show_judge_solution.short_description = "judge_solution"


admin.site.register(ACM, ACMContestAdmin)
admin.site.register(Image)


# class MoviesAdmin(admin.ModelAdmin):
#     list_display_link = ('title', 'runtime', 'director', 'vote_average')
#     list_display = ('title', 'runtime', 'director', 'vote_average')
#     list_filter = ('is_adult',)
#     search_fields = ['director__name', 'title']
#     raw_id_fields = ['casts', 'director', ]


# admin.site.register(Movie, MoviesAdmin)