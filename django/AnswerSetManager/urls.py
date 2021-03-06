"""Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.urls import path
from .views import PageList, AnswerPage, TestSetSiteAPIView, TestSetPageAPIView, ExtractorAPIView, EvaluationAPIView


app_name = 'answer_set_manager'
urlpatterns = [



    path('pages/<int:page_id>', PageList.as_view()),
    path('pages', PageList.as_view()),
    path('answers/<str:page_id>', AnswerPage.as_view()),
    path('answers/', AnswerPage.as_view()),

    path('answer-set', TestSetSiteAPIView.as_view()),

    path('test-set/pages', TestSetPageAPIView.as_view()),
    path('test-set/pages/<int:test_set_page_id>', TestSetPageAPIView.as_view()),
    path('test-set/<int:test_set_id>', TestSetSiteAPIView.as_view()),
    path('test-set/<int:test_set_id>/pages', TestSetPageAPIView.as_view()),
    path('test-set/<int:test_set_id>/pages/<int:test_set_page_ind>', TestSetPageAPIView.as_view()),

    path('test-set/sites', TestSetSiteAPIView.as_view()),
    # path('test-set/sites/<int:test_set_id>', AnswerSetAPIView.as_view()),

    path('extractors', ExtractorAPIView.as_view()),
    path('extractors/<int:extractor_id>', ExtractorAPIView.as_view()),

    path('evaluation/test-set/<int:test_set_id>/pages/<int:test_set_page_ind>', EvaluationAPIView.as_view()),

]
