from django.contrib import admin
from .models import ACM 

class ACMContestAdmin(admin.ModelAdmin):
    list_display_link = ('title', 'problems', 'final_ranking_onsite', 'final_ranking_online', 'test_data', 'judge_solution')
    list_display = ('title', 'problems', 'final_ranking_onsite', 'final_ranking_online', 'test_data', 'judge_solution' )
    # list_filter = ('title',)
    search_fields = ['title']
    # raw_id_fields = ['casts', 'director', ]


admin.site.register(ACM, ACMContestAdmin)


# class MoviesAdmin(admin.ModelAdmin):
#     list_display_link = ('title', 'runtime', 'director', 'vote_average')
#     list_display = ('title', 'runtime', 'director', 'vote_average')
#     list_filter = ('is_adult',)
#     search_fields = ['director__name', 'title']
#     raw_id_fields = ['casts', 'director', ]


# admin.site.register(Movie, MoviesAdmin)