from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

from forms import Submission_Common_Form, LinkForm, SnippetForm
from forms import LicenseForm,  PackageForm

from scipy_central.screenshot.forms import ScreenshotForm as ScreenshotForm
from scipy_central.screenshot.models import Screenshot as ScreenshotClass
from scipy_central.person.forms import Inline_Signin_Create_Form

import models

@login_required
def new_web_submission(request):
    """
    Users wants to submit a new item via the web.
    """
    if request.method == 'POST':

        all_valid = False
        basic_info = Submission_Common_Form(request.POST)
        sshot_form = ScreenshotForm(request.POST, request.FILES)
        if basic_info.is_valid() and sshot_form.is_valid():
            all_valid=True

        if all_valid:
            post = request.POST

            sub = models.Submission.objects.create(
                title = post['title'],
                sub_type = post['sub_type'],
                sub_license = post.get('license', None),
                summary = post['summary'],
                description = post.get('description', ''),
                screenshot = None,
                item_url = post.get('item_url', '')
            )

            # Process screenshot:
            sshot_name = '_raw_' + sub.slug + '__' + \
                                             request.FILES['screenshot'].name
            sshot = ScreenshotClass()
            sshot.img_file_raw.save(sshot_name,\
                            ContentFile(request.FILES['screenshot'].read()))
            sshot.save()
            sub.screenshot = sshot

            # Authors is a ManyToMany: add it *after* creating the instance
            sub.authors = [request.user]


            # TODO(KGD): add the tags
            #sub.tags = [....]

            # Save the submission
            sub.save()

            # Email user
            # TODO(KGD):
            extra_message = 'A confirmation email has been sent to you.'


            # Thank user
            return render_to_response('submission/thank-user.html',
                                      {'extra_message': extra_message})
                                                                             #context_instance=RequestContext(request))


        #if not(all_valid):
            #if request.user.is_authenticated():
                #inline_signin_or_create = False
            #else:
                #inline_signin_or_create = Inline_Signin_Create_Form(request.POST).as_ul()

            #return render_to_response('submission/new-submission.html',
                                      #{'common': common,
                                       #'inline_signin_or_create': inline_signin_or_create},
                                      #context_instance=RequestContext(request))

        #if request.user.is_authenticated():
            #inline_signin_or_create = False
        #else:
            #inline_signin_or_create = Inline_Signin_Create_Form().as_ul()


        #all_valid = common_form.is_valid() and \
                    #Inline_Signin_Create_Form().is_valid() and \
                    #request.user.is_authenticated()

        #if all_valid:
            ##sub_type = post['sub_type']

        #if sub_type == 'snippet':
            #response += SnippetForm().as_p()

        #elif sub_type == 'package':
            #response += PackageForm().as_p()
            #response += LicenseForm().as_p()

        #elif sub_type == 'link':
            #response += LinkForm().as_p()
        #else:



            #try:
                #data = form.cleaned_data
                #entry = Entry.new_from_title(title=data['title'],
                #                             entry_type=data['entry_type'],
                #                             owner=request.user
                #                             )
                #if entry.slug == 'new':
                #    raise IntegrityError()
                #entry.save()
                #return redirect(edit_entry, entry.slug)
            #except IntegrityError:
                # duplicate name
            #form.errors['title'] = [u'The title is already in use.']


    elif request.method == 'GET':

        #if not request.user.is_authenticated():
            #extra_info = ('<p>A user account is required to submit code to this '
                          #'site.')


            #t = loader.get_template('submission/new-submission.html')
            #c = RequestContext(request, {'extra_info': basic_info})
            #return HttpResponse(t.render(c), status=200)


        basic_info = Submission_Common_Form()

        t = loader.get_template('submission/new-submission.html')
        c = RequestContext(request, {'basic_info': basic_info})
        return HttpResponse(t.render(c), status=200)

def next_steps_HTML(request):
    """
    Returns the HTML necessary to complete the next steps of the submission,
    depending on which type of submission the user is making

    http://www.b-list.org/weblog/2006/jul/31/django-tips-simple-ajax-example-part-1/
    """
    if request.method != 'GET':
        return HttpResponse(status=400)

    sub_type = request.GET.get('sub_type', '')

    response = '<h3>Step 2: '
    if sub_type == 'snippet':
        response += 'Code snippet/recipe</h3>'
        response += SnippetForm().as_ul()

    elif sub_type == 'package':
        response += 'Code package/module</h3>'
        response += PackageForm().as_ul()
        response += LicenseForm().as_ul()

    elif sub_type == 'link':
        response += 'Link to external resources</h2>'
        response += LinkForm().as_ul()

    response += ScreenshotForm().as_ul()

    return HttpResponse(response, status=200)

def HTML_for_tagging(request):
    """ Returns HTML that handles tagging """
    response = '<h3>Step 3: Help categorize your submission</h3>'
    response+= ('<p>Please provide subject area labels and categorization '
                'tags to help other users when searching for your code.')

    return  HttpResponse(response, status=200)