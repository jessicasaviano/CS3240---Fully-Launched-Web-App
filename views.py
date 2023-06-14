from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from home.models import Class, Profile, StudySession, DiscussionBoard
import requests, json
from home.forms import StudySessionForm

# Create your views here.


def index(request):
    return render(request, 'home.html')


def onboarding(request):
    foundClasses = []
    curUser = request.user.Profile
    enrolled_classes = list(curUser.classes.all())
    if (request.method == "POST") and not (request.POST.get('dept').upper() == "") and not (request.POST.get('classNum') == ""):
        responseURL = "http://luthers-list.herokuapp.com/api/dept/" + request.POST.get('dept').upper() + "/?format=json"
        response_API = requests.get(responseURL)
        responseAPIText = response_API.text
        responseAPIJson = json.loads(responseAPIText)
        for foundClass in responseAPIJson:
            if (foundClass["catalog_number"] == request.POST.get('classNum')):
                classInfo = []
                classInfo.append(foundClass["instructor"]['name'])
                classInfo.append(foundClass["description"])
                classInfo.append(foundClass["meetings"][0]['days'])
                classInfo.append(foundClass["meetings"][0]['start_time'][:5].replace(".",":"))
                classInfo.append(foundClass["meetings"][0]['end_time'][:5].replace(".",":"))
                classInfo.append(foundClass["meetings"][0]['facility_description'])
                classInfo.append(foundClass["component"])
                foundClasses.append(classInfo)
    return render(request, 'onboarding.html', {'classes': foundClasses, 'department': request.POST.get('dept'), 'catalog_number':request.POST.get('classNum'), 'enrolledclasses': enrolled_classes})

def addClass(request):
    user = request.user.Profile
    className = request.GET.get('department') + " " + request.GET.get('catalogNum')
    newClass = Class.objects.get_or_create(class_name=className,department=request.GET.get('department'), catalog_number = request.GET.get('catalogNum'), instructor=request.GET.get('instr'), description=request.GET.get('desc'), days=request.GET.get('days'), start_time=request.GET.get('start'), end_time=request.GET.get('end'), location=request.GET.get('loc'), component=request.GET.get('comp'))
    user.classes.add(newClass[0])
    user.classesSet=True
    user.save()
    return redirect('setClasses')

def Friend(request):
    foundFriends = []
    user = request.user.Profile
    friend_list = list(user.friendsList.all())
    if request.POST.get('friendz'):
        foundUsers = Profile.objects.all().filter(user__username__contains = request.POST.get('friendz'))
        print(foundUsers)
        currentFriends = user.friendsList.all()
        for profile in foundUsers:
            if profile not in currentFriends:
                if not profile == user:
                    foundFriends.append(profile)
    return render(request, 'friends.html', {'friends': foundFriends, 'friendz':request.POST.get('friendz'), 'username' : request.POST.get('username'),'found': friend_list })


def makeFriend(request):
    user = request.user.Profile
    newFriend = Profile.objects.all().filter(user__username = request.GET.get('username'))
    user.friendsList.add(newFriend[0].id)
    user.save()
    return redirect('getFriends')



def setPreferences(request):
    user = request.user.Profile
    print(request.POST)
    user.favorite_location = request.POST.get('favorite_location')
    user.in_person = request.POST.get('in_person')
    user.cramming = request.POST.get('cramming')
    user.preferencesSet=True
    user.save()
    return redirect('setBio')

def getPreferencesPage(request):
    user = request.user.Profile
    if not(user.classesSet):
        return redirect('setClasses')
    return render(request, 'detailed_onboarding.html')


def setBio(request):
    user = request.user.Profile
    print(request.POST)
    user.year = request.POST.get('year')
    user.school = request.POST.get('school')
    user.major = request.POST.get('major')
    user.about_you = request.POST.get('about_you')
    user.bioSet = True
    user.save()
    return redirect('dashboard')

def getBioPage(request):
    user = request.user.Profile
    if not(user.classesSet):
        return redirect('setClasses')
    return render(request, 'bio_onboarding.html')

def getProfile(request):
    user = request.user.Profile
    user.name = request.POST.get('name')
    user.year = request.POST.get('year')
    if not(user.preferencesSet):
        return redirect('setPreferences')
    return render(request, 'profiles.html')


def dashboard(request):
    user = request.user.Profile
    if not(user.classesSet):
        return redirect("setClasses")
    if not(user.preferencesSet):
        return redirect("setPreferences")
    if not(user.bioSet):
        return redirect("setBio")
    else:
        curUser = request.user.Profile
        enrolled_classes = list(curUser.classes.all())
        friend_list = list(curUser.friendsList.all())
        return render(request, 'dashboard.html', {'enrolledclasses': enrolled_classes, 'in_person': curUser.in_person, 'cramming': curUser.cramming, 'favorite_location': curUser.favorite_location, 'found': friend_list})

def viewClasses(request):
    foundClasses = Class.objects.all()
    return render(request, 'classes_view.html', {'classes': foundClasses})

def viewClass(request, pk):
    curClass = Class.objects.all().filter(id = pk)[0]
    return render(request, 'class_view.html', {'classID': curClass.id,'className': curClass.class_name, 'classInstructor': curClass.instructor, 'classDescription': curClass.description, "classDays": curClass.days, "classStartTime": curClass.start_time, 'classEndTime': curClass.end_time, 'classLocation': curClass.location, 'classType': curClass.component})

def viewStudySessions(request):
    foundSessions = StudySession.objects.all()
    return render(request, 'groups_view.html', {'sessions': foundSessions})

def setDiscussionPage(request, pk):

    if request.method == 'GET':
        user = request.user.Profile
        user.message = request.GET.get('message')
        user.date = request.GET.get('date')

        return render(request, 'group_view.html')
    if request.method == 'POST':
        curSes = StudySession.objects.all().filter(id=pk)[0]
        user = request.user.Profile
        newBoard = DiscussionBoard(message= curSes, sender=user, date=request.POST.get('date'))
        newBoard.save()
        disKey = newBoard.id
        user.save()
        return redirect('viewStudySession', pk)

def viewStudySession(request, pk):
    curSession = StudySession.objects.all().filter(id = pk)[0]
    messages = list(curSession.messagess.all())
    print(curSession)
    print(messages)
    return render(request, 'group_view.html', {'foundSession':curSession, 'messages': messages})



def createStudySession(request,pk):
    if request.method == 'GET':
        context = {}
        context['form'] = StudySessionForm()
        return render(request, "create_study_session.html", context)
    if request.method == 'POST':
        curClass = Class.objects.all().filter(id = pk)[0]
        curUser = request.user.Profile
        newStudySession = StudySession(associatedClass = curClass, organizer=curUser, location=request.POST.get('location'), startTime=request.POST.get('startTime'), endTime = request.POST.get('endTime'), description = request.POST.get('description'), title = request.POST.get('title'))
        newStudySession.save()
        sessionKey = newStudySession.id
        return redirect('viewStudySession', sessionKey)









def joinStudySession(request,pk):
    curSession = StudySession.objects.all().filter(id = pk)[0]
    curUser = request.user.Profile
    curSession.save()
    return redirect('viewStudySession', pk)


def leaveStudySession(request,pk):
    curSession = StudySession.objects.all().filter(id = pk)[0]
    curUser = request.user.Profile
    curSession.attendees.remove(curUser)
    curSession.save()
    return redirect('viewStudySession', pk)




