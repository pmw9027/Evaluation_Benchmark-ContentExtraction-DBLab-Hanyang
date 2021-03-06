from Core.models import Site, Page, Answer, AnswerIndex, TestSet, Node, NodeName
from Extractor.models import ContentExtractor, Predict


from django.http import JsonResponse, FileResponse, HttpResponseNotFound, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from rest_framework.permissions import IsAuthenticated
from pathlib import Path
from rest_framework.request import Request
import json
from django.db import IntegrityError
from inspect import currentframe, getframeinfo


class TestSetPageAPIView(APIView):
    permission_classes = []

    def get(self, request, test_set_id=None, test_set_page_ind=None):
        if test_set_page_ind is not None:
            try:

                pages = TestSet.objects.get(id=test_set_id).pages.all()
                page = pages[test_set_page_ind]

            except TestSet.DoesNotExist as e:
                print(getframeinfo(currentframe()).lineno, e)
                return HttpResponseNotFound("No file")

            except Page.DoesNotExist as e:
                print(getframeinfo(currentframe()).lineno, e)
                return HttpResponseNotFound("No file")

            if not page.mht_file_path:
                print(getframeinfo(currentframe()).lineno, 'No MHTML file')
                return HttpResponseNotFound("No file")

            path = Path(page.mht_file_path)
            if path.is_file():
                file_reponse = FileResponse(open(path, 'rb'), content_type="message/rfc822")
                file_reponse['Content-Disposition'] = f'inline; filename="{page.id}.mhtml"'
                return file_reponse

            else:
                print(getframeinfo(currentframe()).lineno, 'No MHTML file')
                return HttpResponseNotFound("No file")

        else:
            pages = TestSet.objects.get(id=test_set_id).pages.all()

            if request.GET.get('index'):
                page = test_set_pages[int(request.GET.get('index'))].page
                if not page.mht_file_path:
                    return HttpResponseNotFound("No file")

                path = Path(page.mht_file_path)
                if path.is_file():
                    file_reponse = FileResponse(open(path, 'rb'), content_type="multipart/mixed")
                    file_reponse['Content-Disposition'] = f'inline; filename="{page.id}.mhtml"'
                    return file_reponse

            return JsonResponse({
                'code': 0,
                'data': list(pages.values())

            }, safe=False)

    def post(self, request: Request, test_set_id=None):
        _output = {}

        _data = request.data.copy()
        _data.pop('id')
        # _data['site_id'] = _data.pop('id')
        _nodes = _data.pop('nodes')
        _mhtml = _data.pop('mhtmlData')

        test_set = TestSet.objects.get(id=test_set_id)

        site, created = Site.objects.get_or_create(protocol=_data['protocol'], domain=_data['host'])
        site.name = _data['title'] if site.name is None else site.name
        site.save()

        try:
            page, created = Page.objects.get_or_create(**_data, site=site)

        except IntegrityError as e:
            print(e.args)

            return Response(_output)

        if created:
            test_set.pages.add(page)
            _nodes = json.loads(_nodes)

            for _node in _nodes:
                _node = json.loads(_node)

                node_name, created = NodeName.objects.get_or_create(node_name=_node.pop('node_name'))
                Node.objects.create(**_node, page=page, name=node_name)

            path = f"resources/{page.id}"
            if not os.path.exists(path):
                os.makedirs(path)

            with open(f"{path}/page.mhtml", 'wb+') as destination:
                destination.write(_mhtml.encode('ascii'))

            page.mht_file_path = f"{path}/page.mhtml"
            page.save()

        return Response(_output)


class TestSetSiteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, test_set_id=None):
        if test_set_id:

            # test_set_sites = TestSetSite.objects.filter(test_set_id=test_set_id).select_related('site')

            sites = TestSet.objects.get(id=test_set_id).sites.all()

            return JsonResponse({
                'code': 0,
                'data': list(sites.values())

            }, safe=False)

        else:
            test_sets = TestSet.objects.filter(creator=request.user).values('id', 'name', 'description')

            return JsonResponse({
                'code': 0,
                'data': list(test_sets)

            }, safe=False)


class PageList(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []

    def get(self, request, page_id=None):
        _output = {}
        user = request.user

        if page_id is None:

            answers = Answer.objects.filter(checker=user).values_list('page_id')
            web_pages = Page.objects.filter(mht_file_path__isnull=False).exclude(id__in=[answer[0] for answer in answers],)

            print(web_pages.query)

            web_pages = web_pages.values('id', 'url')

            _output['data'] = [entry for entry in web_pages]

            # _output = serializers.serialize("json", web_page)
            response = JsonResponse(_output, safe=False)

            return response

        else:
            page = Page.objects.get(id=page_id)
            from pathlib import Path

            if page.mht_file_path:
                path = Path(page.mht_file_path)
                if path.is_file():
                    file_reponse = FileResponse(open(path, 'rb'), content_type="message/rfc822")
                    file_reponse['Content-Disposition'] = f'inline; filename="{page_id}.mhtml"'
                    return file_reponse
                else:
                    return HttpResponseNotFound("No file")

            else:
                return HttpResponseNotFound("No file")

    def post(self, request, page_id=None):
        _output = {}

        test_set_site = TestSetSite.objects.get(id=request.POST.get('id'))

        page = Page.objects.get_or_create(site=test_set_site.site, url=request.POST.get('url'), title=request.POST.get('title'))
        test_set_page = TestSetPage.objects.create(page=page, test_set_site=test_set_site)

        path = f"resources/{page.id}"
        if not os.path.exists(path):
            os.makedirs(path)

        with open(f"{path}/page.mhtml", 'wb+') as destination:
            destination.write(request.POST.get('mhtmlData').encode('ascii'))

        page.mht_file_path = f"{path}/page.mhtml"
        page.save()

        _output = {

        }

        return Response(_output)


class AnswerPage(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []

    def get(self, request, page_id=None):
        _output = {}
        user = request.user

        if page_id is None:

            objts = Answer.objects.all()

            if request.GET.get('mine'):
                objts = Answer.objects.filter(answer_checker=user)
            web_page = objts.values('answer_number')
            _output['data'] = [entry for entry in web_page]
            response = JsonResponse(_output, safe=False)
        else:

            try:
                answer = Answer.objects.get(page_id=page_id, answer_checker=user)
                answer_indexes = AnswerIndex.objects.filter(answer=answer)

                _output['data'] = [answer_index.answer_index for answer_index in answer_indexes]

                response = JsonResponse(_output, safe=False)

            except ObjectDoesNotExist:
                response = JsonResponse(_output, safe=False)

        return response

    def post(self, request, page_id=None):
        _output = {}

        # if form.is_valid():
        if page_id is None:

            return HttpResponseNotFound("The form ")
        else:
            user = request.user
            obj, created = Answer.objects.get_or_create(page_id=page_id, checker=user)

            if request.POST.getlist('indices[]'):
                answers = request.POST.getlist('indices[]')
            else:
                answers = []
            if created:

                obj.save()
            else:

                obj.save()
                answer_indexes = AnswerIndex.objects.filter(answer=obj)
                answer_indexes.delete()

            for _index in answers:
                answer = AnswerIndex(answer=obj, answer_index=_index)
                answer.save()

            return Response(_output)


class ExtractorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, extractor_id=None):

        if extractor_id:
            predicts = Predict.objects.filter(content_extractor_id=extractor_id)

            test_set_sites = TestSetSite.objects.all()
            if request.GET.get('test_set_id'):
                test_set_sites.filter(test_set__id=request.GET.get('test_set_id'))

            values = test_set_sites.values_list('id')
            test_set_pages = TestSetPage.objects.filter(test_set_site__id__in=values).select_related('page')

            if request.GET.get('index'):
                page = test_set_pages[int(request.GET.get('index'))].page

            predict = predicts.filter(page=page)

            return JsonResponse({
                'data': model_to_dict(predict) if predict.exists() else None

            })

        else:
            instances = ContentExtractor.objects.all()

            return JsonResponse({
                'data': [model_to_dict(instance) for instance in instances]

            }, safe=False)

    def post(self, request, extractor_id=None):

        _output = {'code': 0}
        if extractor_id:
            page_id = request.data.pop('page_id')
            predict = Predict.objects.create(content_extractor_id=extractor_id, page_id=page_id, readable=request.data.pop('readable'))

            if predict.readable:
                try:
                    predict.indices.add(Node.objects.get(hyu=request.data.pop('content'), page_id=page_id))
                except Node.DoesNotExist:

                    predict.delete()
                    return Response(_output)

            return Response(_output)
        else:
            pass


class EvaluationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, test_set_id=None, test_set_page_ind=None):

        page = TestSet.objects.get(id=test_set_id).pages.all()[test_set_page_ind]

        return JsonResponse({
            'data': {
                'answers': [] if len(page.predict_set.all()) == 0 else [i.hyu for i in page.answer_set.first().indices.all()],
                'predicts': [] if len(page.predict_set.all()) == 0 else {i.content_extractor.id: [j.hyu for j in i.indices.all()] for i in page.predict_set.all()}
            }
        }, safe=False)

    def post(self, request, test_set_id=None, test_set_page_ind=None):
        page = TestSet.objects.get(id=test_set_id).pages.all()[test_set_page_ind]

        for key in request.data:
            for dic in request.data[key]:
                try:
                    page.predict_set.get(content_extractor_id=key).performanceevaluationresult_set.create(**dic)
                except IntegrityError as e:
                    print(getframeinfo(currentframe()).lineno, e)

        return Response({

        })




