from django.shortcuts import render, redirect
import logging
from django.template import loader
from django.http.response import HttpResponse
from board.models import Board
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.views.decorators.csrf import csrf_exempt
from BoardEx.settings import PAGE_SIZE, PAGE_BLOCK


logger = logging.getLogger(__name__)

# Create your views here.
# logger.debug(msg)
# logger.info(msg)

# 글목록
def boardlist(request):
    # 데이터가 넘어올땐 get 방식 / post 방식
    # 데이터 출력 페이지라서 post로 할 필요 없음.?
    template = loader.get_template("boardlist.html");
    count = Board.objects.all().count()
    
    pagenum = request.GET.get("pagenum")
    if not pagenum :
        pagenum = "1"
    pagenum = int(pagenum)
    
    start = (pagenum -1) * int(PAGE_SIZE)          #( 3-1 )*10+1       20
    end = start + int(PAGE_SIZE)                          # 20 + 10             30
    
    if end > count :
        end = count
        
    dtos = Board.objects.order_by("-ref","restep")[start:end]
    
    number = count - (pagenum-1)*int(PAGE_SIZE)         # 50 - (2-1) *10 
    
    startpage = pagenum // PAGE_BLOCK * PAGE_BLOCK + 1  # 15//10*10+1 = 11
    if pagenum % PAGE_BLOCK == 0 :
        startpage -= PAGE_BLOCK
    endpage = startpage + PAGE_BLOCK - 1        # 11 + 10 - 1
    pagecount = count // PAGE_SIZE 
    
    if count % PAGE_SIZE > 0 :
        pagecount += 1
    if endpage > pagecount :
        endpage = pagecount
   
    pages = range(startpage, endpage+1)     
    
    context = {
        "count" : count,
        "dtos" : dtos,
        "pagenum":pagenum,
        "number" : number,
        "startpage" : startpage,
        "endpage" : endpage,
        "pageblock" : PAGE_BLOCK,
        "pagecount" : pagecount,
        "pages" : pages,
        }
    return HttpResponse(template.render(context,request))

# 글쓰기
@csrf_exempt
def writepro( request ) :
    #                        그룹화아이디    글순서    글레벨
    # 제목글                10               0           0
    # ㄴ 답글               10               1           1
    #    ㄴ 재답글          10               2           2  
    # ㄴ 나중에 쓴 답글    10               0           0 
    
    #                        그룹화아이디    글순서    글레벨
    # 제목글                10               0           0
    # ㄴ 답글               10               2           1
    #    ㄴ 재답글          10               3           2  
    # ㄴ 나중에 쓴 답글    10               1           1   
    
    #                        그룹화아이디    글순서    글레벨
    # 제목글                10               0           0
    # ㄴ 나중에 쓴 답글    10               1           1      
    # ㄴ 답글               10               2           1
    #    ㄴ 재답글          10               3           2  
    
    # 제목글     num ref restep relevel      X       <= 글목록 
    # 답변글     num ref restep relevel      0       <= 글보기
    if request.method == "GET": 
        ref = 1                         # 그룹화 아이디
        restep = 0                      # 글순서
        relevel = 0                     # 글레벨
        num = request.GET.get("num")
        if num == None :
            # 제목글인 경우
            try :
                # 글이 있는 경우
                maxnum = Board.objects.order_by("-num").values()[0]["num"]
                ref = maxnum + 1        # 그룹화  아이디 = 글번호 최대값 + 1
            except IndexError :
                # 글이 없는 경우
                ref = 1                        
        else :
            # 답변글인 경우    
            num = request.GET.get("num")
            ref = request.GET.get("ref")
            restep = request.GET.get("restep")
            relevel = request.GET.get("relevel")
            
            res = Board.objects.filter( restep__gt = restep and ref == ref )    # gt = greater than / gte >=
            for re in res :
                re.restep = int( re.restep ) + 1
                re.save()
            restep = int( restep ) + 1
            relevel = int( relevel ) + 1
              
        template = loader.get_template( "write.html" )
             
        context = {
            "num" : num,
            "ref" : ref,
            "restep" : restep,
            "relevel" : relevel,
            }
        return HttpResponse( template.render( context, request ) )
    else :
        num = Board.objects.all().count()
        if num == None :
            # 글이 없는 경우
            num = 1
        else : 
            # 글이 있는 경우
            num += 1
            
        dto = Board(
            num = num,
            writer = request.POST["writer"],
            subject = request.POST["subject"],
            passwd = request.POST["passwd"],
            content = request.POST["content"],
            readcount = 0,
            ref = request.POST["ref"],
            restep = request.POST["restep"],
            relevel = request.POST["relevel"],
            regdate = DateFormat(datetime.now()).format("Y-m-d"),
            ip = request.META.get("REMOTE_ADDR"),    
            );
            
        dto.save()
        return redirect("boardlist")

# 글보기
def detail( request ) :
    num = request.GET.get( "num" )
    pagenum = request.GET.get( "pagenum" )
    number = request.GET.get("number")
    template = loader.get_template( "detail.html" )
    
    dto = Board.objects.get( num = num )
    
    dto.readcount += 1
    dto.save()
    
    context = {
        "dto" : dto,
        "pagenum" : pagenum,
        "number" : number,
        }
    return HttpResponse( template.render( context, request ) )
    
# 글삭제
@csrf_exempt
def deletepro( request ) :
    if request.method == "GET": 
        num = request.GET.get( "num" )
        pagenum = request.GET.get( "pagenum" )
        template = loader.get_template( "delete.html" )
        context = {
            "num" : num,
            "pagenum" : pagenum,
            }
        return HttpResponse( template.render( context, request ) )
    else :     
        num = request.POST["num"]
        pagenum = request.POST["pagenum"]
        passwd = request.POST["passwd"]
        
        dto= Board.objects.get( num = num )
        
        # 비밀번호가 다르다    -    delete.html    
        if passwd != dto.passwd :
            template = loader.get_template( "delete.html" )
            context = {
                "num":num,
                "pagenum":pagenum,
                "msg" : "입력하신 비밀번호가 다릅니다.",
                }
            return HttpResponse( template.render( context, request ) )  
        
        # 비밀번호가 같다    -    boardlist.html
        else :
            dto.subject="삭제된 글입니다."
            dto.readcount = -1
            dto.save()
            return redirect( "boardlist" )

# 글수정    
@csrf_exempt
def modifypro(request):
    if request.method == "GET":     
        num = request.GET.get("num")
        pagenum = request.GET.get("pagenum")
        number = request.GET.get("passwd")
        template = loader.get_template("modify.html")
        context={
            "num" : num,
            "pagenum" : pagenum,
            "number" : number,
            }
        return HttpResponse(template.render(context, request))
    
    else :
        num = request.POST["num"]
        subject = request.POST["subject"]
        content = request.POST["content"]
        passwd = request.POST["passwd"]    
        dto = Board.objects.get(num=num)        # num 이 num 인애의 정보를 다 받아옴
        
        dto.subject = subject
        dto.content= content
        dto.passwd = passwd
        
        dto.save()
        
        return redirect("boardlist")

@csrf_exempt
def modifyview(request):
    num=request.POST["num"]
    pagenum = request.POST["pagenum"]
    number= request.POST["number"]
    passwd = request.POST["passwd"]   
    
    dto = Board.objects.get(num=num)
    
    if passwd == dto.passwd :
        template = loader.get_template("modifyview.html")
        context = {
            "num" : num,
            "pagenum" : pagenum,
            "number" : number,
            "dto" : dto,
            }
    else : 
        template = loader.get_template("modify.html")
        context = {
            "msg" : "비밀번호가 다릅니다",
            "pagenum" : pagenum,
            "number" : number,
            "msg" : "비밀번호가 다릅니다"
            }
        
    
    return HttpResponse( template.render(context , request) )

