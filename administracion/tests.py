from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP
from perfiles_usuario.models import Capturista
from familias.models import Familia
from estudios_socioeconomicos.models import Estudio
from .forms import UserForm, DeleteUserForm, FeedbackForm


class TestAdministracionUrls(TestCase):
    """Unit test suite for testing the views in the app: administracion.

    Test that the views for 'administracion' are correctly received as a response and that
    they use the correct template.
    """

    def setUp(self):
        thelma = User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero',
            first_name='Thelma', last_name='Amlet')
        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(thelma)
        self.client.login(username='thelma', password='junipero')

    def test_view_main_dashboard(self):
        """Unit Test: administracion.views.admin_main_dashboard.

        """
        test_url_name = 'administracion:main'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'administracion/dashboard_main.html')

    def test_view_users_dashboard(self):
        """Unit Test: administracion.views.admin_users_dashboard.

        """
        test_url_name = 'administracion:users'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'administracion/dashboard_users.html')


class TestUserForm(TestCase):
    """Basic Suite for testing UserForm.

    Test the basic purpose of the UserForm: that the user is actually created and
    that it has the proper group assigned to it.

    Attributes
    ----------
    valid_data_form : dict
        A dictionary containing the data necessary for the form, which is used in all the
        individual tests.
    """

    def setUp(self):
        """Setup the dictionary with data for feeding the form.

        """
        self.factory = RequestFactory()
        self.valid_data_form = {
            'username': 'raul',
            'first_name': 'raul',
            'last_name': 'arce',
            'email': 'elver@abc.com',
            'password': 'elver12312310'
        }
        self.thelma = User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero',
            first_name='Thelma', last_name='Thelmapellido')

    def test_valid_data_basic(self):
        """Test if the form assigns the proper group to a user.

        Test if the overriden save method inside UserForm correctly assigns
        the administrador group to the user we are creating.
        """
        data_form = self.valid_data_form.copy()
        data_form['rol_usuario'] = ADMINISTRADOR_GROUP
        request = self.factory.get('administracion:users')
        form = UserForm(data_form)
        self.assertTrue(form.is_valid())
        user = form.save(request=request)
        self.assertTrue(user.groups.filter(name=ADMINISTRADOR_GROUP).exists())

    def test_valid_data_capturista(self):
        """Test if the form creates the Capturista.

        Test if the overriden save method inside UserForm correctly creates the
        Capturista object when that role is selected.
        """
        data_form = self.valid_data_form.copy()
        data_form['rol_usuario'] = CAPTURISTA_GROUP
        request = self.factory.get('administracion:users')
        form = UserForm(data_form)
        self.assertTrue(form.is_valid())
        user = form.save(request=request)
        self.assertTrue(user.groups.filter(name=CAPTURISTA_GROUP).exists())
        self.assertTrue(Capturista.objects.filter(user=user).exists())

    def test_invalid_data(self):
        """Test if the form validates invalid data.

        Test if the Form is not valid if the role is missing.
        """
        data_form = self.valid_data_form.copy()
        form = UserForm(data_form)
        self.assertFalse(form.is_valid())


class TestDeleteUserForm(TestCase):
    """Basic Suite for testing DeleteUserForm.

    Test the basic purpose of the DeleteUserForm: that the user is actually deleted from database.

    Attributes
    ----------
    valid_data_form : dict
        A dictionary containing the data necessary for the form, which is used in all the
        individual tests.
    """

    def setUp(self):
        """Setup the dictionary with data for feeding the form.

        """
        self.thelma = User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero',
            first_name='Thelma', last_name='Thelmapellido')
        self.valid_data_form = {
            'user_id': str(self.thelma.pk)
        }

    def test_valid_data_basic(self):
        """Test if the form effectively deletes the user instance

        """
        data_form = self.valid_data_form.copy()
        form = DeleteUserForm(data_form)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(User.objects.count(), 0)
        try:
            test_user = User.objects.get(pk=self.valid_data_form['user_id'])
        except User.DoesNotExist:
            test_user = None
        self.assertEqual(test_user, None)

    def test_invalid_data(self):
        """Test if the form validates invalid data.

        """
        data_form = self.valid_data_form.copy()
        data_form['user_id'] = 'id falso'
        form = DeleteUserForm(data_form)
        self.assertFalse(form.is_valid())


class TestFeedBack(TestCase):
    """ Suite to test Feedback Form and related urls.

    """

    def setUp(self):
        test_username = 'thelma'
        test_password = 'junipero'
        self.admin = User.objects.create_user(
            username=test_username, email='juan@pablo.com', password=test_password,
            first_name='Thelma', last_name='Thelmapellido')
        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(self.admin)
        administrators.save()

        estebes = User.objects.create_user(
            username='estebes', email='juan@example.com', password='contrasena',
            first_name='Estebes', last_name='glez')
        capturista = Group.objects.get_or_create(name=CAPTURISTA_GROUP)[0]
        capturista.user_set.add(estebes)
        capturista.save()
        self.capturista = Capturista.objects.create(user=estebes)

        solvencia = 'No tienen dinero'
        estado = Familia.OPCION_ESTADO_SOLTERO
        localidad = Familia.OPCION_LOCALIDAD_JURICA
        f1 = Familia.objects.create(numero_hijos_diferentes_papas=1,
                                    explicacion_solvencia=solvencia,
                                    estado_civil=estado, localidad=localidad)

        self.study = Estudio.objects.create(capturista=self.capturista, familia=f1,
                                            status=Estudio.REVISION)

    def test_url(self):
        """ Check that the url for focus mode of the study exists.

        """
        self.client.login(username='thelma', password='junipero')
        test_url_name = 'administracion:focus_mode'
        response = self.client.get(reverse(test_url_name,
                                           kwargs={'study_id': self.study.id}), follow=True)
        self.assertEqual(200, response.status_code)

    def test_valid_form(self):
        """ Check that the form is valid with correct data.

        """
        form = FeedbackForm({'estudio': self.study.id,
                             'usuario': self.admin.id,
                             'descripcion': 'nooooo'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """ Check that the form is invalid with incorrect data.

        """
        form = FeedbackForm({'estudio': -1,
                             'usuario': self.admin.id,
                             'descripcion': 'nooooo'})
        self.assertFalse(form.is_valid())

    def test_change_status_admin(self):
        """ Check that the form changes the status of a study.

        When the admin submits feedback on a study, it should change to rejected.
        """
        form = FeedbackForm({'estudio': self.study.id,
                             'usuario': self.admin.id,
                             'descripcion': 'nooooo'})
        self.assertTrue(form.is_valid())
        form.save()
        status = Estudio.objects.get(id=self.study.id).status
        self.assertEqual(status, Estudio.RECHAZADO)

    def test_change_status_capturista(self):
        """ Check that the form changes the status of a study.

        When the capturista submits feedback on a study, it should change to revision.
        """
        self.study.status = Estudio.RECHAZADO
        self.study.save()
        form = FeedbackForm({'estudio': self.study.id,
                             'usuario': self.capturista.user.id,
                             'descripcion': 'siiiii'})
        self.assertTrue(form.is_valid())
        form.save()
        status = Estudio.objects.get(id=self.study.id).status
        self.assertEqual(status, Estudio.REVISION)
