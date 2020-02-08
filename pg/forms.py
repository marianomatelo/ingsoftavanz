from django import forms
from django.forms import HiddenInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class UserRegisterForm(UserCreationForm):

    email = forms.EmailField()

    rol = forms.ChoiceField(
        choices=(
            ('1', "Admin"),
            ('2', "Director de carrera"),
            ('3', "Docente"),
            ('4', "Evaluador"),
            ('5', "Especialista")
        ),
        widget=forms.Select,
        initial='1',
        required=True,
        help_text="Seleccione su rol"
    )

    class Meta:
        model = User
        fields = ['rol', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.rol = self.cleaned_data["rol"]
        if commit:
            user.save()
        return user


class keyForm(forms.Form):

    clave_multifactor = forms.CharField(help_text="Se ha enviado la clave multifactor a su email", required=True)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('clave_multifactor', css_class='input-xlarge'),
        FormActions(
            Submit('save_changes', 'Run', css_class="btn-primary"),
            # Submit('cancel', 'Cancel'),
        )
    )

    def __init__(self, *args, **kwargs):
        super(keyForm, self).__init__(*args, **kwargs)


class planEstudioForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=30)
    cargaHorariaTotal = forms.CharField(label='carga Horaria Total', max_length=30)
    resolucionConeau = forms.CharField(label='Resolucion de la CONEAU', max_length=30)
    resolucionMinEdu = forms.CharField(label='Resolucion del Min de Edu', max_length=30)
    resolucionRectoral = forms.CharField(label='Resolucion Rectoral', max_length=30)
