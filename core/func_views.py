# def registerview(request):
#     fm = RegisterForm()
#     context = {
#         'form' : fm
#     }
#     if request.method == 'POST':
#         fm = RegisterForm(data=request.POST)
#         if fm.is_valid():
#             fm.save()
#             messages.add_message(request,messages.SUCCESS,'Account created successfully')
#             return redirect('signin')
#     return render(request, 'authentication/register.html', context)

# def signinview(request):
#     fm = LoginForm()
#     context = {
#         'form' : fm
#     }
#     if request.method == 'POST':
#         fm = LoginForm(data=request.POST)
#         if fm.is_valid():
#             username = fm.cleaned_data['username']
#             password = fm.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_authenticated:
#                     login(request, user)
#                     messages.add_message(request,messages.SUCCESS,'Logged in as '+username)
#                     return redirect('home')
#         messages.add_message(request,messages.ERROR,'Invalid username or password')
#         return redirect('signin')
#     return render(request, 'authentication/signin.html' , context)

# def signoutview(request):
#     logout(request)
#     messages.add_message(request,messages.SUCCESS,'Loggedout')
#     return redirect('home')

# def forgotpwdview(request):
#     context = {
#         'form' : IdentifyForm()
#     }
#     if request.method == 'POST':
#         fm = IdentifyForm(request.POST)
#         if fm.is_valid():
#             email = fm.cleaned_data['email']
#             if UserModel.objects.filter(email=email).exists():
#                 username = UserModel.objects.get(email=email).username
#                 encode = urlsafe_base64_encode(force_bytes(username))
#                 return redirect('/reset_password/'+encode)
#             return redirect('signin')
#     return render(request, 'authentication/identify.html',context)

# def resetpwdview(request,username):

#     username = force_str(urlsafe_base64_decode(username))
#     user = UserModel.objects.get(username=username)
#     context = {
#         'form' : SetPasswordForm(user=user)
#     }
#     if request.method == 'POST':
#         fm = SetPasswordForm(data=request.POST,user=user)
#         if fm.is_valid():
#             fm.save()
#             return redirect('signin')
#         return redirect('home')
#     return render(request,'authentication/resetpwd.html',context)