from django import forms
from django.forms import HiddenInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from pg.models import Dataset_Meta, Daemon


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['username', 'email','phone_no','password1', 'password2']


class MessageForm(forms.Form):

    dataset = forms.ChoiceField(choices=[])

    model = forms.ChoiceField(
        choices=(
            ('1', "XGBoost: Extreme Gradient Boosting"),
            ('2', "MLP: Multi Layer Perceptron"),
            ('3', "LSTM: Long Short Term Memory Neural Network"),
            ('4', "LR: Linear Regression"),
            ('5', "SVM: Support Vector Machine"),
            ('6', "ARIMA: AutoRegressive Integrated Moving Average")
        ),
        widget=forms.RadioSelect,
        initial='1',
        required=False,
        help_text="Choose model"
    )

    cleaning_method = forms.ChoiceField(
        choices=(
            ('1', "Don't Clean & Don't Smooth"),
            ('2', "Clean & Smooth"),
            ('3', "Clean"),
            ('4', "Smooth")
        ),
        widget=forms.RadioSelect,
        initial='1',
        required=False,
        help_text="Choose cleaning method"
    )

    scaling_method = forms.ChoiceField(
        choices=(
            ('1', "Don't Scale"),
            ('2', "Min Max (0-1)"),
            ('3', "Standard")
        ),
        widget=forms.RadioSelect,
        initial='1',
        required=False,
        help_text="Choose how to scale the variables"
    )

    training_method = forms.ChoiceField(
        choices=(
            ('1', "Bayesian Optimization"),
            ('2', "Grid Search"),
            ('3', "Fine Tune")
        ),
        widget=forms.RadioSelect,
        initial='1',
        required=False,
        help_text="Choose how to tune hyperparameters for the model"
    )

    # XGBoost
    gamma = forms.IntegerField(help_text="[0,∞] Minimum loss reduction required to make a further partition on a leaf node of the tree. The larger gamma is, the more conservative the algorithm will be.", required=False)
    max_depth = forms.IntegerField(help_text="[0,∞] Maximum depth of a tree. Increasing this value will make the model more complex and more likely to overfit.", required=False)
    subsample = forms.FloatField(help_text="(0,1] Subsample ratio of the training instances. Setting it to 0.5 means that XGBoost would randomly sample half of the training data prior to growing trees. and this will prevent overfitting. Subsampling will occur once in every boosting iteration.", required=False)
    min_child_weight = forms.IntegerField(help_text="[0,∞] Minimum sum of instance weight (hessian) needed in a child. If the tree partition step results in a leaf node with the sum of instance weight less than min_child_weight, then the building process will give up further partitioning. In linear regression task, this simply corresponds to minimum number of instances needed to be in each node. The larger min_child_weight is, the more conservative the algorithm will be.", required=False)
    max_delta_step = forms.IntegerField(help_text="[0,∞] Maximum delta step we allow each leaf output to be. If the value is set to 0, it means there is no constraint. If it is set to a positive value, it can help making the update step more conservative. Usually this parameter is not needed, but it might help in logistic regression when class is extremely imbalanced. Set it to value of 1-10 might help control the update.", required=False)
    colsample_bytree = forms.IntegerField(help_text="(0, 1] Is the subsample ratio of columns when constructing each tree. Subsampling occurs once for every tree constructed.", required=False)
    eta = forms.FloatField(help_text="[0,1] Step size shrinkage used in update to prevents overfitting. After each boosting step, we can directly get the weights of new features, and eta shrinks the feature weights to make the boosting process more conservative.", required=False)

    run_description = forms.CharField(help_text="Enter a description for the run", required=True)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        'dataset',
        'model',
        'cleaning_method',
        'scaling_method',
        'training_method',

        # XGBoost
        'max_depth',
        'gamma',
        'subsample',
        'min_child_weight',
        'max_delta_step',
        'colsample_bytree',
        'eta',

        Field('run_description', css_class='input-xlarge'),
        FormActions(
            Submit('save_changes', 'Run', css_class="btn-primary"),
            # Submit('cancel', 'Cancel'),
        )
    )

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['dataset'].choices = [(x.pk, x.description) for x in Dataset_Meta.objects.all()]



class UploadsForm(forms.Form):

    name = forms.CharField(help_text="Enter a dataset name", required=True)

    description = forms.CharField(help_text="Enter a description", required=True)

    problem = forms.ChoiceField(
        choices=(
            ('1', "Regression"),
            ('2', "Classification")
        ),
        widget=forms.RadioSelect,
        initial='1',
        required=False
    )

    frequency = forms.ChoiceField(
        choices=(
            ('1', "Monthly"),
            ('2', "Weekly"),
            ('3', "Daily"),
            ('4', "Hourly"),
            ('5', "Minutes"),
        ),
        initial='5',
        required=False
    )

    file = forms.FileField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        'name',
        'description',
        'problem',
        'frequency',
        'file',

        FormActions(
            Submit('save_changes', 'Upload', css_class="btn-primary"),
            # Submit('cancel', 'Cancel'),
        )
    )

    def __init__(self, *args, **kwargs):
        super(UploadsForm, self).__init__(*args, **kwargs)


class AnalyzerForm(forms.Form):

    run = forms.ChoiceField(choices=[])

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        'run',

        FormActions(
            Submit('save_changes', 'Analyze', css_class="btn-primary"),
            # Submit('cancel', 'Cancel'),
        )
    )

    def __init__(self, *args, **kwargs):
        super(AnalyzerForm, self).__init__(*args, **kwargs)
        self.fields['run'].choices = [(x.pk, x.pk) for x in Daemon.objects.filter(status='finished').order_by('pk')]