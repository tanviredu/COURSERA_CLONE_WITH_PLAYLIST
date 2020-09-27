from django.shortcuts import render,HttpResponse
from App_Shop.models import Product
from App_Login.models import Video_Content
from django.contrib.auth.decorators import login_required

@login_required
def get_courses_for_user(request):
    current_user = request.user
    videos = Video_Content.objects.filter(user=current_user)
    if len(videos) > 0:
        for item in videos:
            #print(item.video_slug)
            user_videos = Product.objects.filter(slug=item.video_slug)
        print(user_videos)
        return render(request,"App_Video/course_list.html",{'user_videos':user_videos})
    else:
        return render(request,"App_Video/course_list.html")
    


@login_required
def course_stream(request,slug):
    video = Product.objects.filter(slug=slug)[0]
    return render(request,'App_Video/stream.html',{'video':video})