# -*- coding: utf-8 -*-
"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
import requests
import string
import sys

import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
import urllib.parse

from django.contrib.auth.models import User

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean, Dict, Float, List, Set, Field, ScopeIds
from xblock.fragment import Fragment

from django.utils.translation import ugettext as _
from django.template import Context, Template

from .utils import render_template, xblock_field_list
from django.conf import settings as DJANGO_SETTINGS
from openedx.core.djangoapps.site_configuration.models import SiteConfiguration
from mock import patch, MagicMock, Mock
from xblock.field_data import FieldData, DictFieldData
from xblock.runtime import Runtime

import logging
log = logging.getLogger(__name__)


class IframeWithAnonymousIDXBlock(XBlock):
    """
    XBlock displaying an iframe, with an anonymous ID passed in argument
    """

    # Fields are defined on the class. You can access them in your code as
    # self.<fieldname>.

    # URL format :
    # {iframe_url}/UserID

    # Hay que declarar estas variables aqui para luego poder utilizarlos en el HTML sin tener que pasarlos
    nomExamenes = ""
    tamExamenes = ""
    nombresAlum = ""
    entidadEDX = ""

    display_name = String(
        help=_("SMOWL"),
        display_name=_("Component Display Name"),
        # name that appears in advanced settings studio menu
        default=_("SMOWL RESULTS"),
        scope=Scope.user_state
    )

    smowlresults_url = String(
        display_name=_("SMOWL ACTIVATED"),
        help=_("PUBLISH to activate SMOWL"),
        default="",
        scope=Scope.settings
    )

    has_author_view = True

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def author_view(self, context=None):
        lms_base = SiteConfiguration.get_value_for_org(
            self.location.org,
            "LMS_BASE",
            DJANGO_SETTINGS.LMS_BASE
        )
        context = {
            'has_settings': self.check_settings(),
            'help_url': 'https://{}/{}'.format(lms_base, 'contact_form')
        }
        template = render_template('/templates/html/smowlresults-author.html', context)
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/smowlresults.css"))
        frag.initialize_js('IframeWithAnonymousIDXBlock')
        return frag

    def student_view(self, context=None):
        """
        The primary view of the SMOWLRESULTS, shown to students
        when viewing courses.
        """

        #runtime = TestRuntime(services={'field-data': DictFieldData({})})
        #block = IframeWithAnonymousIDXBlock(runtime, scope_ids=Mock(spec=ScopeIds))
        #parent = block.get_parent()

        #url_response = self.request.GET

        # student es la id del curso y sirve pa saber si es admin
        student_id = self.xmodule_runtime.anonymous_student_id
        user_id = self.scope_ids.user_id

        course_id = self.xmodule_runtime.course_id
        #usageID =  self.scope_ids.usage_id

        # usage es el codigo del curso mejor asi
        #usage5555 = self.scope_ids.usage_id

        idUnit2 = self.parent
        idUnit = str(idUnit2).split("@")[-1]
        #idUnit5 = "{0}".format(idUnit)

        if not self.check_settings():
            context = {
                'has_settings': False,
            }
            settings = {
                'has_settings': False
            }
        else:
            # Para sacar los ids de los alumnos
            url = DJANGO_SETTINGS.SMOWLRESULT_EDXUSERSACTIVITIESV2_URL

            # Este es el ID del curso que hay que dividir o si no es lo que se guarda en container
            idCurso = self.course_id

            #entityName3 = str(self.course_id).split(":")
            #entityName33 = entityName3[1]
            #entityName2 = str(entityName33).split("+")
            #entityName22 = entityName2[0]
            #entityName = str(entityName22)
            entityName = DJANGO_SETTINGS.SMOWL_ENTITY
            swlLicenseKey = DJANGO_SETTINGS.SMOWL_KEY

            payload = {'entity_Name': entityName,
                    'course_Container': idCurso, 'swlLicenseKey': swlLicenseKey}
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            data = urllib.parse.urlencode(payload).encode("utf-8")
            req = urllib.request.Request(url, data, headers)

            # Esta es la respuesta que se hace a edxUsersActivities para saber los ID de estudiantes
            #response = urllib.request.urlopen(req)

            with urllib.request.urlopen(req, data=data) as response:
                todoIds = response.read().decode()

            # De los IDs de estudiantes con la API sacamos los datos
            if todoIds == '0':
                tamExamenes2 = '0'
                examenes = 'a'
                nombre = ''
            elif todoIds == "":
                tamExamenes2 = '0'
                examenes = 'b'
                nombre = ''

            else:
                lista = todoIds.split("xSMOWL")
                nombres = lista[0]
                examenes = lista[1]

                sepExamenes = examenes.split(",")
                idNombres = nombres.split(",")
                tam = len(idNombres)
                tamExamenes2 = len(sepExamenes)

                m = "inicial"
                nombre = ""

                todoIds = 'hola1'

                for i in range(tam):
                    try:
                        user = User.objects.get(id=idNombres[i])
                        m = user.profile.name
                        nombre += ","+idNombres[i]+"."+m
                    except User.DoesNotExist:
                        pass

            # Datos personales del alumno como el username
            # id2=self.scope_ids.user_id
            nombre = nombre.replace(" ", "_")

            nombre = nombre.encode('utf-8')

            todoIds = todoIds.encode('utf-8')

            #new_smowlresults_url = "{0}={1}&course_CourseName={2}".format(self.smowlresults_url, student_id, course_id)
            new_smowlresults_url = "hola {0} ADDDDDDDDDDDDDDDDDDDDD {1} ".format(
                entityName, todoIds)

            # QUITAR para probar
            #self.display_name = new_smowlresults_url

            # En el context ponemos las variables que declaramos al principio del todo para poder usarlos en el HTML
            context = {
                'self': self,
                'location': str(self.location).split('@')[-1],
                'smowlresults_url': new_smowlresults_url,
                'nombresAlum': nombre,
                'entidadEDX': entityName,
                'swlLicenseKey':DJANGO_SETTINGS.SMOWL_KEY,
                'has_settings': True,
                'RESULTSCONTROLLER_URL':DJANGO_SETTINGS.SMOWLRESULT_RESULTSCONTROLLER_URL
            }
            settings = {
                'location': str(self.location).split('@')[-1],
                'nomExamenes': examenes,
                'tamExamenes': tamExamenes2,
                'has_settings': True
            }
        template = render_template('/templates/html/smowlresults.html', context)
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/smowlresults.css"))
        frag.add_javascript(self.resource_string(
            "static/js/src/smowlresults.js"))
        frag.initialize_js('IframeWithAnonymousIDXBlock', json_args=settings)
        return frag

    def studio_view(self, context=None):
        """
        The studio view of the SMOWLRESULTS, with form
        """
        frag = Fragment()
        frag.add_content(render_template(
            '/templates/html/smowlresults-edit.html'))
        frag.add_javascript(self.resource_string(
            "static/js/src/smowlresults-edit.js"))
        frag.initialize_js('IframeWithAnonymousIDXBlock')
        return frag

    def check_settings(self):
        return (
            hasattr(DJANGO_SETTINGS, 'SMOWLRESULT_EDXUSERSACTIVITIESV2_URL') and 
            hasattr(DJANGO_SETTINGS, 'SMOWL_KEY') and 
            hasattr(DJANGO_SETTINGS, 'SMOWLRESULT_RESULTSCONTROLLER_URL') and 
            hasattr(DJANGO_SETTINGS, 'SMOWL_ENTITY')
            )

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("IframeWithAnonymousIDXBlock",
             """
			 """),
        ]
